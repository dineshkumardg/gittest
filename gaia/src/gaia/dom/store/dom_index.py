import gaia.dom.index.models
from django.db import transaction
from gaia.error import GaiaErrors
#from gaia.utils.errors_mixin import ErrorsMixin
from gaia.dom.document_error import DocumentError
from gaia.dom.store.dom_store_error import DomStoreError


class _DomIndex:
    # Using the ErrorsMixin would be nice but causes problems in dom_store init with  an error like:
    # TypeError: unbound method __init__() must be called with ErrorsMixin instance as first argument (got DomStore instance instead)
    # using super introduces other requirements (signature-matching) which means I'm leaving it for now! :(
    #def __init__(self):
        #ErrorsMixin.__init__(self)

    @transaction.commit_on_success  #should we be doing this?
    def add_item(self, item):
        ' Add a new item. If there was one already, then it is replaced, and the old one is also returned (as "superceded"). '
        self._log.enter('_DomIndex', item=item) # Note: we need the _DomIndex string as this gets printed as WebBox.add_item()! :(

        document = item.document()

        item_index, superceded_item_index = self._index_item(document)
        document_index = self._index_document(document, item_index)
        page_map = self._index_pages(item, document_index)
        self._index_chunks(item, document_index, page_map)
        #self._index_clips(item) #TODO
        self._index_asset_links(item, document_index)
        self._index_document_links(item, document_index)

        self._log.exit('_DomIndex', item=item)

        return item_index, superceded_item_index

    def delete_item(self, item):
        item.delete()

    @staticmethod
    def document_index(item_index):
        ' return a Document (index) for an Item (index). '
        #TODO: catch errors?
        document_index = gaia.dom.index.models.Document.objects.get(item=item_index)
        return document_index

    @staticmethod
    def mark_item_changed(item_index_id):
        #item_index = gaia.dom.index.models.Item(id=item_index_id)
        item_index = gaia.dom.index.models.Item.objects.get(id=item_index_id)
        item_index.has_changed = True
        item_index.save()
        return item_index

    def _index_item(self, document):
        ''' return a new item.
            if there was already one in the index, it is also returned as the superceded item.
        '''
        # should return 1 or 0 objects
        existing_items = gaia.dom.index.models.Item.objects.filter(dom_id=document.dom_id, dom_name=document.dom_name).order_by('-id')  # same item might be re-ingested multiple times
        if len(existing_items) > 0:
            superceded = existing_items[0]
        else:
            superceded = None
        # TODO/NOTE: models.Item.save() currently handles this transparently too. Shold probably remove that save method(?) REVIEW

        item_index = gaia.dom.index.models.Item(dom_id=document.dom_id, dom_name=document.dom_name)  # Note: item uses Document ids
        item_index.save()
        return item_index, superceded

    def _index_document(self, document, item_index):
        #TODO: catch errors?
        document_index = gaia.dom.index.models.Document(dom_id=document.dom_id, dom_name=document.dom_name, item=item_index)
        document_index.save()
        return document_index

    def _index_pages(self, item, document_index):
        #TODO: catch errors?
        pages = item.pages()

        page_map = {}   # map dom_id to Page() (so that we can resolve references to page's dom_ids to db entries)
        for page in pages:
            page_index = gaia.dom.index.models.Page(dom_id=page.dom_id, dom_name=page.dom_name, document=document_index)
            page_index.save()
            page_map[page.dom_id] = page_index

        return page_map

    def _index_chunks(self, item, document_index, page_map):
        #TODO: catch errors
        chunks = item.chunks()
        errors = []

        for chunk in chunks:
            chunk_index = gaia.dom.index.models.Chunk(dom_id=chunk.dom_id, dom_name=chunk.dom_name, document=document_index, is_binary=chunk.is_binary)
            chunk_index.save()  # Note: have to save before adding many-to-many realationships

            # TODO; HERE chunk.clip_ids, page_ids: resolve and add??
            for page_dom_id in chunk.page_ids:
                try:
                    page_index = page_map[page_dom_id]
                    chunk_index.pages.add(page_index)
                except KeyError, e:
                    # collect all errors together.
                    errors.append(DocumentError('An article references a page which does not exist!', article_id=chunk.dom_id, article_name=chunk.dom_name, page_reference=page_dom_id))

        if errors:
            raise GaiaErrors(*errors)


    def _index_clips(self, item):
        #TODO!
        print "dom_store._index_clips(): TODO ***********************"
        return #*************************************

        # this is probably something like this...... TODO! (CHO doesn't have clips?)
        #TODO: catch errors
        #clips = item.clips()

        #for clip in clips:
            #clip = gaia.dom.index.models.Clip(dom_id=clip.dom_id, dom_name=clip.dom_name, page=page)   # TODO: where do we get page from???? clip.page_dom_id???
            #clip.save()

    def _index_asset_links(self, item, document_index):
        links = item.asset_links()

        for link in links:
            link = gaia.dom.index.models.AssetLink(dom_id=link.dom_id, dom_name=link.dom_name, document=document_index, asset_fname=link.asset_fname)
            link.save()

    def _index_document_links(self, item, document_index):
        links = item.document_links()

        for link in links:
            source_chunk_dom_id = link.source.get('chunk', None)
            source_page_dom_id  = link.source.get('page',  None)

            if source_chunk_dom_id:
                source_chunk_indexes = gaia.dom.index.models.Chunk.objects.filter(document=document_index, dom_id=source_chunk_dom_id)

                if len(source_chunk_indexes) > 1:
                    raise DomStoreError('Trying to add links into DomStore index and failed as there is more than one chunk matching a link target!', chunks=source_chunk_indexes)
                elif len(source_chunk_indexes) == 0:
                    raise DomStoreError('Trying to add links into DomStore index and NO MATCH for target_chunk!', source_chunk_dom_id=source_chunk_dom_id)
                else:
                    source_chunk_index = source_chunk_indexes[0]
            else:
                source_chunk_index = None

            if source_page_dom_id:
                source_page_indexes = gaia.dom.index.models.Page.objects.filter(document=document_index, dom_id=source_page_dom_id)

                if len(source_page_indexes) > 1:
                    raise DomStoreError('Trying to add links into DomStore index and failed as there is more than one page matching a link target!', pages=source_page_indexes)
                elif len(source_page_indexes) == 0:
                    raise DomStoreError('Trying to add links into DomStore index and NO MATCH for target_page!', source_page_dom_id=source_page_dom_id)
                else:
                    source_page_index = source_page_indexes[0]
            else:
                source_page_index = None

            # These 3 are plain strings...
            target_item  = link.target.get('document', None) # NOTE (item vs document): This is correct: we are using the document name as an item name in the DOM Model.
            target_chunk = link.target.get('chunk',    None)
            target_page  = link.target.get('page',     None)

            link = gaia.dom.index.models.DocumentLink(dom_id=link.dom_id, dom_name=link.dom_name, document=document_index)
            
            # Note: all of the following are optional...
            if  source_chunk_index:
                link.chunk = source_chunk_index
            
            if source_page_index:
                link.page = source_page_index

            if target_item:
                link.unresolved_target_item = target_item

            if target_chunk:
                link.unresolved_target_chunk = target_chunk

            if target_page:
                link.unresolved_target_page = target_page

            link.save()

    # friend Methods...
    @staticmethod
    def _get_live_index(item): # TODO TEST
        ''' a convenience method to JUST get an index for the LIVE version of an item.
        '''
        existing_items = gaia.dom.index.models.Item.objects.filter(dom_id=item.dom_id, dom_name=item.dom_name, is_live=True)  # should return 1 or 0 objects
        if len(existing_items) != 1:
            raise DomStoreError('Looking up a live index for an item failed!', item=item, number_of_matching_items_in_index=len(existing_items))

        return existing_items[0]
