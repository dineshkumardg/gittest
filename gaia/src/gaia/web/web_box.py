import os
from cengage.asset_id.asset_id_service import AssetIdService 
from gaia.error import GaiaError
from gaia.utils.try_cmd import try_cmd, CommandError
from gaia.utils.import_class import import_class
from gaia.dom.store.dom_store import DomStore
import gaia.search.index
import gaia.search.query
from qa.models import Item
from qa.qa_link import QaLink
from qa.models import MissingFinalId

class WebBox(DomStore):
    ''' Storage of Items for use by web apps (like an inbox for the web).

        The WebBox is a domstore plus:
            it manages a search index beside the domstore.
            final_ids (asset ids) are allocated for QA use.

        Files are grouped by item_name sub-folders
        When image assets are added, they may optionally 
        be replicated in another format (eg tiff to png)

    '''
    def __init__(self, config):
        DomStore.__init__(self, config.WEB_ROOT)
        self.config = config

        # Note: this is done at this point and in this way to avoid a circular import-dependency
        self.search_adapter_class = import_class(config.search_adapter_class_name)  
        self.fid_service = AssetIdService() # a "final_id" service (could parameterise via config later if required.)

    def item_index(self, item): # TODO test
        ' return the Index (ie database) object for a pre-existing, live item '
        # This must be here to return a qa.models.Item (not a dom store version).
        return Item.objects.get(dom_id=item.dom_id, dom_name=item.dom_name, is_live=True) # should only ever be one match!

    def change_item_info(self, item_index, doc_info_changes, page_info_changes, chunk_info_changes):    # @override
        # Note: 
        # doc_info_changes might look like this:
        # {u'cho_iaxx_2010_7771_001_0001': {u'/chapter/metadataInfo/sourceLibrary/libraryName': u'TUSHHouse'}}

        DomStore.change_item_info(self, item_index, doc_info_changes, page_info_changes, chunk_info_changes)

        # do a brute force "replace" of all of the search data (ie a full uodate rather than a fine-granined change).
        self._log.debug('*Replacing* search info with changed data')
        self._update_search_item(item_index, doc_info_changes, page_info_changes, chunk_info_changes)

    def _add_item(self, item, item_index_id, superceded_item_index_id):
        ''' add an item after decorating the page info with web-box image urls,
            and updating chunk info with the page and clip refs.

            Also update the (web/analysis) search index,
            and allocate final_ids (asset ids).
        '''
        self._decorate_page_info_with_thumbnails(item, item_index_id)
        self._add_search_item(item, item_index_id)

        if superceded_item_index_id:
            self._delete_search_item(superceded_item_index_id)
            self._reallocate_final_ids(item_index_id, superceded_item_index_id)
        else:
            self._allocate_final_ids(item_index_id)

    def _decorate_page_info_with_thumbnails(self, item, item_index_id):
        item_url = self._item_url(item.dom_id, item_index_id)

        for page in item.pages():
            fname = page.info['_asset_fname']
            page_name = os.path.splitext(fname)[0]   # remove the extension

            img_url = '%s/%s.%s' % (item_url, page_name, self.config.web_image_ftype)
            thumb_url = '%s/%s_thumbnail.%s' % (self._item_url(item.dom_id, item_index_id), page_name, self.config.web_image_ftype)

            page.info.update({'_img_url': img_url, '_thumb_url': thumb_url})

    def _add_search_item(self, item, item_index_id):
        ''' Add (or replace) item data to Search Server for Global Analysis
        '''
        self._log.enter()
        item_index = Item.objects.get(pk=item_index_id)
        search_server = gaia.search.index.Index(self.config.search_server)
        search_adapter = self.search_adapter_class(item, item_index)

        for search_object in search_adapter.get_search_objects():
            info = search_object.search_info

            chunk_dom_id = info['_dom_id']
            chunk_index = item_index.chunk(chunk_dom_id)

            # link to one of the pages for this chunk (note that we're not ordering here, so might not be the first one) (will usually work though)
            # could order by dom_id, but is this the right thing to do? (TODO: review)
            chunk_page1 = chunk_index.pages.all()[0]

            qa_link = QaLink(item_index_id, chunk_index.id, chunk_page1.id)
            qa_link.decorate_info(info)

            search_server.add(search_object)

        self._log.exit()

    def _delete_search_item(self, item_index_id):
        ' Remove all entries for an Item from the Search Server '
        self._log.enter()

        item_index = Item.objects.get(pk=item_index_id)
        search_server = gaia.search.index.Index(self.config.search_server)

        for chunk_index in item_index.chunks():
            search_id = self.search_adapter_class.search_id(item_index.dom_id, item_index_id, chunk_index.dom_id)
            search_server.delete(search_id)

        self._log.exit()

    def _update_search_item(self, item_index, doc_info_changes, page_info_changes, chunk_info_changes):
        ' Update entries for an Item in the Search Server '
        # Note: 
        # doc_info_changes might look like this:
        # {u'cho_iaxx_2010_7771_001_0001': {u'/chapter/metadataInfo/sourceLibrary/libraryName': u'TUSHHouse'}}
        self._log.enter()

        search_server = gaia.search.index.Index(self.config.search_server)
        search_query = gaia.search.query.Query(self.config.search_server, search_collection=self.config.project_code)

        for chunk_index in item_index.chunks():
            search_id = self.search_adapter_class.search_id(item_index.dom_id, item_index.id, chunk_index.dom_id)

            search_object = search_query.get(search_id) # get old data
            if search_object is not None:  # solr might be empty!
                self.search_adapter_class.update_search_object(search_object, doc_info_changes, page_info_changes, chunk_info_changes) # update the data
                search_server.add(search_object)            # put the modified data

        self._log.exit()

    def add_asset(self, asset, item_name, version_id):
        ''' put an asset (for an item) into this container.
        
            If it's an image, then convert it into multiple sizes
            (and possibly change the file type too)
        '''
        DomStore.add_asset(self, asset, item_name, version_id)

        if asset.is_image():
            
            item_dir = self._item_dir(item_name, version_id)
            in_fpath = asset.fpath

            out_fpath = os.path.join(item_dir, '%s.%s' % (asset.fbase, self.config.web_image_ftype))
            self._convert_image(in_fpath, out_fpath)

            out_fpath = os.path.join(item_dir, '%s_thumbnail.%s' % (asset.fbase, self.config.web_image_ftype))
            self._convert_image(in_fpath, out_fpath, resize='128x128')

    def _convert_image(self, in_fpath, out_fpath, resize=None):
        self._log.debug('... converting image from "%s" to "%s" (resize="%s")' % (in_fpath, out_fpath, resize))
        if resize:
            #cmd = ['/usr/bin/convert',  in_fname, '-resize', '128x128', out_fname]   # TODO: config option!..
            cmd = [self.config.convert_fpath, in_fpath, '-resize', resize, '-strip', out_fpath]  # without the strip the resize image can be almost as large as the original
        else:
            cmd = [self.config.convert_fpath, in_fpath, out_fpath]

        try:
            try_cmd(*cmd)
        except CommandError, e:
            self._log.error('*** Error when attempting to convert "%s" to "%s": %s' % (in_fpath, out_fpath, str(e)))
            raise GaiaError('Could not convert image "%s" to "%s" (err="%s")' % (in_fpath, out_fpath, str(e)))   # TODO change err type!...

    def _allocate_final_ids(self, item_index_id):
        self._log.enter()
        item_index = Item.objects.get(pk=item_index_id)

        fid = self.fid_service.get()
        document = item_index.document()
        document.set_final_id(fid)

        for page_index  in item_index.pages():
            fid = self.fid_service.get()
            page_index.set_final_id(fid)
        
        for chunk_index  in item_index.chunks():
            fid = self.fid_service.get()
            chunk_index.set_final_id(fid)

        # TODO: clips and links: are these required?... ASK JAMES/SARAH **** IMPORTANT & URGENT! => are these distinct gift objects/retrievable items?
        #for clip_index  in item_index.clips(): # TODO: no clips() method yet!...
            #fid = self.fid_service.get()
            #clip_index.set_final_id(fid)

        #for link_index  in item_index.links():
            #fid = self.fid_service.get()
            #link_index.set_final_id(fid)
        self._log.exit()

    def _reallocate_final_ids(self, item_index_id, superceded_item_index_id):
        ''' The old asset ids should be transferred if the new item looks "like" the old one.

            Any parts that look the same as the old item (have the same dom_id) will
            get the old final_id, anything eelse will get a fresh final_id.

            Note: unfortualtely dom_names are not unique, so dom_id is the only thing we can rely on.
            Note that there is NO GUARANTEE that 2 things with the same dom_id are _really_ the same thing!
        '''
        self._log.enter()
        old_item = Item.objects.get(pk=superceded_item_index_id)

        new_item = Item.objects.get(pk=item_index_id)
        new_document = new_item.document()

        # A: copy the document final_id
        try:
            fid = old_item.document().get_final_id()    # can fail (only if previous allocation failed)
            self._log.info('FINAL_ID: copying from old to new document final_id', fid=fid)
            new_document.set_final_id(fid)
        except MissingFinalId, e:
            fid = self.fid_service.get()
            self._log.warning('FINAL_ID: allocating a NEW document final_id (old document was MISSING_FINAL_ID)', fid=fid, new_document_dom_id=new_document.dom_id)
            new_document.set_final_id(fid)

        # B: look through all the new pages, and if the dom_id is in the old pages,
        # copy the final_id. If any are remaining unset, allocate a fresh one.
        old_pages = old_item.pages()
        new_pages = new_item.pages()
        old = {page.dom_id: page for page in old_pages}
        new = {page.dom_id: page for page in new_pages}

        for new_page in new_pages:
            if new_page.dom_id in old:
                try:
                    fid = old[new_page.dom_id].get_final_id()
                    self._log.info('FINAL_ID: copying from old to new page final_id', fid=fid, page_dom_id=new_page.dom_id)
                except MissingFinalId, e:
                    fid = self.fid_service.get()
                    self._log.warning('FINAL_ID: allocating a NEW page final_id (old page was MISSING_FINAL_ID)', fid=fid, new_page_dom_id=new_page.dom_id)

                new_page.set_final_id(fid)
                del new[new_page.dom_id]

        for new_page_dom_id in new:
            fid = self.fid_service.get()
            self._log.info('FINAL_ID: allocating a NEW page final_id (new page that wasn\'t in old item)', fid=fid, new_page_dom_id=new_page_dom_id)
            new[new_page_dom_id].set_final_id(fid) 

        # C: do the same (as pages) with chunks.
        old_chunks = old_item.chunks()
        new_chunks = new_item.chunks()
        old = {chunk.dom_id: chunk for chunk in old_chunks}
        new = {chunk.dom_id: chunk for chunk in new_chunks}

        for new_chunk in new_chunks:
            if new_chunk.dom_id in old:
                try:
                    fid = old[new_chunk.dom_id].get_final_id()
                    self._log.info('FINAL_ID: copying from old to new chunk final_id', fid=fid, chunk_dom_id=new_chunk.dom_id)
                except MissingFinalId, e:
                    fid = self.fid_service.get()
                    self._log.warning('FINAL_ID: allocating a NEW chunk final_id (old chunk was MISSING_FINAL_ID)', fid=fid, new_chunk_dom_id=new_chunk.dom_id)

                new_chunk.set_final_id(fid)
                del new[new_chunk.dom_id]

        for new_chunk_dom_id in new:
            fid = self.fid_service.get()
            self._log.info('FINAL_ID: allocating a NEW chunk final_id (new chunk that wasn\'t in old item)', fid=fid, new_chunk_dom_id=new_chunk_dom_id)
            new[new_chunk_dom_id].set_final_id(fid) 

        # Note: clips and links are not required (for CHO).
        self._log.exit()
