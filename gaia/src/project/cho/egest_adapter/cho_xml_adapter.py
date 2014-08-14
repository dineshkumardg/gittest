import os
import gc
from gaia.utils.lock import Lock, LockError
from gaia.utils.gaia_folder import GaiaFolder
from gaia.utils.work_area import WorkArea
from gaia.egest.adapter.xml_conversion_dict import XmlConversionDict
from project.cho.egest_adapter.doc.doc_factory import DocFactory
from project.cho.egest_adapter.doc_box import DocBox
from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.feed.feed_file  import FeedFile
from qa.models import DocumentFinalId
from gaia.egest.adapter.egest_adapter import EgestAdapterError, EgestAdapter
from gaia.error import GaiaError
from qa.models import Item
from gaia.dom.model.item import ItemIncompleteWarning


class XmlExportError(EgestAdapterError):
    pass


class ChoXmlAdapter(EgestAdapter):
    platform_name = 'lst' # @override

    def _extra_conversion_args(self, item, item_index):
        ''' CHO requires a few things in conversion beyond the plain xml:

            1. file sizes for asssets
            2. asset ids ("final_ids")
            3. links to other ("related") documents
        '''
        args = {'file_size': {},
                'asset_id': {},
                'item_folder_name': '%s_%s' % (item.dom_name, str(item_index.id)), # to ensure uniqueness, we add the "version" to the item name
                'illustrations': [chunk for chunk in item.chunks() if chunk.is_binary],
                'related_documents': [], 
               }
        for asset in item.binary_assets():
            args['file_size'][asset.fname] = os.path.getsize(asset.fpath)   # size in bytes

        args['asset_id']['document'] = item_index.document().get_final_id()

        args['asset_id']['pages'] = {}
        for page in item_index.pages():
            args['asset_id']['pages'][page.dom_id] = page.get_final_id()

        args['asset_id']['chunks'] = {}
        for chunk in item_index.chunks():
            args['asset_id']['chunks'][chunk.dom_id] = chunk.get_final_id()  # in conversion this is overridden by CHOA-1074

        for link in item.document_links():
            link_index = item_index.document_link(link.dom_id)
            target_chunk_index = link_index.target_chunk

            if target_chunk_index is  None:
                raise ItemIncompleteWarning()  # we shouldn't be able to release something that is incomplete

            target_article_asset_id = self.related_document_final_id(target_chunk_index, link)
            args['related_documents'].append((link.info, target_article_asset_id))  # Note: link.info contains source xpaths

        return args

    def related_document_final_id(self, target_chunk_index, link):
        ''' anything that points to a relatedDocument cho_meet needs to use the cho_meet document assetId, not a chunk! '''

        target_dom_id = target_chunk_index.document.dom_id  # i.e. cho_meet_1922_0000_000_0000
        final_asset_id = None

        if target_dom_id.startswith('cho_meet'):
            self.log.info('using asset id of document not the chunk')

            target_id = target_chunk_index.document.id 
            document_final_ids = DocumentFinalId.objects.filter(document=target_id)[0]
            final_asset_id = document_final_ids.final_id
        else:
            self.log.debug('using asset id of chunk - aligning with chunk defined in CHOA-1074')

            # was:
            # final_asset_id = target_chunk_index.get_final_id()
            #
            # but due to http://jira.cengage.com/browse/CHOA-1074 got replaced with... 
            target_psmid = link.target['document']
            target_chunk_id =  link.target['chunk']
            target_item = Item.objects.filter(is_live=True, dom_name=target_psmid).get()
            target_chunks = target_item.chunks()

            chunks= {}
            for chunk in target_chunks:
                chunks[chunk.dom_id] = chunk.get_final_id()

            ordered_keys_of_chunks = sorted(chunks.iterkeys())
            correct_asset_key = ordered_keys_of_chunks[ int(target_chunk_id) - 1]  # offset by 1 as array starts at 0
            final_asset_id = chunks[correct_asset_key]

            i = 1
            for key in ordered_keys_of_chunks:
                self.log.info('%s = %s = %s' % (i, key, chunks[key]))
                i += 1

        self.log.debug(final_asset_id=final_asset_id, gdom_asset_id= target_chunk_index.get_final_id())
        return final_asset_id

    def _make_feed_lock(self):
        ' grab a lock to keep out other workers '
        # TODO: this needs revising to work across machines!
        lock_period = 1 * 60 * 60 # 1 hour in seconds
        lock_fpath = os.path.join(self.config.egest_working_dir, '_make_feed_lock.txt')
        self._lock = Lock(lock_fpath, lock_period)
        self.log.info('FEED LOCK: acquired')

    def _make_feed_unlock(self):
        self._lock.unlock()
        self.log.info('FEED LOCK: released')

    def is_ready_for_transfer(self, transfer_prep_dir): # @override
        ''' start sending if there is 1.5Gb of data ready
            and no-one else is trying the same thing at the same time.
            (this stops workers from clashing and fighting over the work!)
        '''
        # First see if we can do anything
        try:
            self.log.enter()

            try:
                self._make_feed_lock()
            except LockError, e:
                return False    # someone else is already doing this, so leave them to it!

            # check to see if we have enough data
            doc_inst_folder_size = GaiaFolder.size(transfer_prep_dir)
            self.log.info(doc_inst_folder_size=doc_inst_folder_size, transfer_batch_size=self.config.transfer_batch_size)

            if doc_inst_folder_size > self.config.transfer_batch_size:
                return True # ready to make a new feed
            else:
                self._make_feed_unlock()
                return False    # not ready yet
        finally:
            self.log.exit()

    def _convert(self, source_xml_dict, transfer_prep_dir, **extra_args):
        ''' Read the source_xml_dict and create output files, ready for
            transfer, in transfer_prep_dir (must *not* be any extra files!)class XmlExportError(EgestAdapterError):
    pass

            For CHO, we use the transfer_prep_dir as a DocBox.
            (this is part of STAGE 1)
        '''
        self.log.enter()
        doc_box = DocBox(transfer_prep_dir)

        document_instance_generator = DocFactory.create(self.config, source_xml_dict, extra_args)
        docs = document_instance_generator.document_instances()     # dict of group: doc-instance string

        for group in docs: # write docs to transfer_prep_dir ....
            item_name = extra_args['item_folder_name']  # note: this is item + version

            doc_box.lock(item_name, group)

            i = 1
            for doc_instance_str in docs[group]:
                asset_fname = 'doc_instance_%02d' % i   # a random, unique name
                asset = doc_box.new_asset(asset_fname, item_name, group, is_binary=False)
                asset.write(doc_instance_str)
                asset.close()
                i += 1
            
            doc_box.unlock(item_name, group)

        self.log.exit()

    def _make_feed_files(self, transfer_prep_dir, out_dir):
        ''' Look in the transfer_prep_dir and prepare anything 
            that is 'ready to go' in the out_dir

            For CHO, we gather together any groups of document instances
            by ChoFeedGroup and make them into distinct feed files.
        '''
        self.log.info(transfer_prep_dir=transfer_prep_dir, out_dir=out_dir)

        doc_box = DocBox(transfer_prep_dir, lock_mins=60)   # give us 1hr (60 mins) to do this.
        transfer_item_names = doc_box.transfer_item_names() # these are "transfer-item" names == "item-name_version"
        real_item_names = doc_box.real_item_names()

        # Hmm.. this might be a bad idea: egest_workers will easily clash?... TODO: review/redesign? :(
        # good enough for now: it'll at least do something (in the absence of specs! :( ).
        for group in ChoFeedGroup.groups():
            transfer_items_in_group = []
            real_items_in_group = []

            for item_name in transfer_item_names:
                if not doc_box.exists(item_name, group):    # select only items which have doc instances in this group
                    continue

                try: # lock as many items in this group as we can...
                    doc_box.lock(item_name, group)
                    transfer_items_in_group.append(item_name)
                    real_items_in_group.append(real_item_names[item_name])
                except LockError, e:
                    pass    # we would expect that some items are locked (eg being added by another worker), so this is normal.

            if transfer_items_in_group:
                # make feed files from doc instances...
                # TUSH: TODO: maybe add an info asset in the docbox with (pickled?) doc-instance info in it (mcodes, asset ids, object types? Yukky.. :( )
                assets = []
                for item_name in transfer_items_in_group:
                    assets.extend(doc_box.assets(item_name, group)) # collect together all the document instances from all the items
                            
                is_indexed = ChoFeedGroup.is_indexed(group)

                # make one feed file for this group
                feed_file = FeedFile(assets, is_indexed, real_items_in_group, group)
                feed_file.write(out_dir)

                # clean up the doc box
                for item_name in transfer_items_in_group:
                    doc_box.delete_item(item_name, group)
                    # Note: doc_box.unlock(item_name, group) # implicit (is not required as the folder's no longer there!)

    def egest(self, transfer_prep_dir, item, item_index, release_type, *item_changes):
        self.log.enter(item=item)

        try:
            if release_type == 'xml' or release_type == 'both':
                xml_asset = item.xml_asset()
                if xml_asset == None:
                    raise XmlExportError('No XML asset found for item "%s": CANNOT EXPORT!' % item.dom_name)

                tree = item._get_dom_adapter()._etree  # to preserve RAM avoid creating another tree - i.e. tree = etree.parse(xml_asset.fpath) 
                source_xml_dict = XmlConversionDict(tree, *item_changes)

                extra_args = self._extra_conversion_args(item, item_index)
                self._convert(source_xml_dict, transfer_prep_dir, **extra_args)

                collected = gc.collect()
                self.log.info('gc egest.end collected %d objects' % collected)

                # du -cb /GAIA/cho/egest_working_dir | grep total
                if self.is_ready_for_transfer(transfer_prep_dir):
                    self.log.info('make feed files START')
                    work_area = WorkArea(self.config, 'egest_flush_'+self.platform_name)
                    self._make_feed_files(transfer_prep_dir, work_area.path)
                    self._transfer(work_area.ls())
                    work_area.remove()
                    self._make_feed_unlock()
                    self.log.info('make feed files END :-)')

        except GaiaError, e:
            self.log.exit('FAILED', err=e)
            raise EgestAdapterError('Failed to transfer files to an export platform', error=e)

        self.log.exit()

    def flush(self, transfer_prep_dir):
        self.log.enter()
        try:
            self._make_feed_lock()
        except LockError, e:
            self.log.exit('Feed locked, so quitting (assuming someone else has coincidentally made a flushed feed-file.')
            return # someone else is already doing this, so leave them to it!

        work_area = WorkArea(self.config, 'egest_flush_'+self.platform_name)
        self._make_feed_files(transfer_prep_dir, work_area.path)

        self._transfer(work_area.ls())
        work_area.remove()

        self._make_feed_unlock()    # we've finished making the feed; let other workers have a go.
        self.log.exit()
