from qa.qa_link import QaLink
from gaia.search.search_object import SearchObject
from gaia.search.adapter.search_adapter import SearchAdapter

class _ChunkSearchObject(SearchObject):

    def __init__(self, dom_item, item_index, dom_chunk, chunk_index, doc_info): 
        # TODO: review: duplication of search_id and qa_link information/usage.
        search_id = self.search_id(str(dom_item.dom_id), str(item_index.id), str(dom_chunk.dom_id))   # for display and a unique search key
        search_info = {}

        for xpath in doc_info:
            self._set_doc_info(search_info, doc_info, xpath)

        for xpath in dom_chunk.info:
            self._set_chunk_info(search_info, dom_chunk.info, xpath)

        page_ids = dom_chunk.page_ids
        if page_ids:
            first_page_index_id = page_ids[0]
        else:
            first_page_index_id = None

        qa_link = QaLink(item_index.id, chunk_index.id, first_page_index_id)
        
        SearchObject.__init__(self, search_id, search_info, qa_link)

    def __str__(self):
        return 'ChunkSearchObject(search_id="%s", search_info="%s")' % (self.search_id, self.search_info)

    def __repr__(self):
        return self.__str__()

    @classmethod
    def search_id(cls, item_dom_id, item_index_id, chunk_dom_id): 
        # TODO: review: duplication of search_id and qa_link information/usage.
        return '%s|%s|%s' % (item_dom_id, item_index_id, chunk_dom_id)   # a unique search key within the index

    @classmethod
    def _from_search_id(cls, search_id): 
        ' do a "reverse" of the search_id '
        item_dom_id, item_index_id, chunk_dom_id = search_id.split('|')
        return item_dom_id, item_index_id, chunk_dom_id

    @classmethod
    def _set_doc_info(cls, search_info, doc_info, xpath):
        search_key = xpath.split('/')[-1]
        search_info['doc_' + search_key] = doc_info[xpath]  #  doc prefix? TODO (OR .. #Note: chunk info deliberatley OVERRIDES doc_info with the same name (especially note: "title").

    @classmethod
    def _set_chunk_info(cls, search_info, chunk_info, xpath):
        # ignore some internal things (because these will break due to multiple-values) but allow others such as _is_binary
        if not xpath in ['_clip_ids', '_link_ids', '_page_ids']:
            search_key = xpath.split('/')[-1]
            search_info[search_key] = chunk_info[xpath]

    @classmethod
    def update(cls, search_object, doc_info_changes, page_info_changes, chunk_info_changes): 
        ' A convenience method to update a search object with supplied item-changes '
        # Note: 
        # doc_info_changes might look like this:
        # {u'cho_iaxx_2010_7771_001_0001': {u'/chapter/metadataInfo/sourceLibrary/libraryName': u'TUSHHouse'}}

        search_info = search_object.search_info
        search_id = search_object.search_id
        item_dom_id, item_index_id, chunk_dom_id = cls._from_search_id(search_id)

        # Note that the changes are indexed by doc/chunk/page, so we only want the info that's relevant to this search object
        doc_updates = doc_info_changes.get(item_dom_id, {})  # Note: item_dom_id == document_dom_id
        chunk_updates = chunk_info_changes.get(chunk_dom_id, {})

        for xpath in doc_updates:
            cls._set_doc_info(search_info, doc_updates, xpath)

        for xpath in chunk_updates:
            cls._set_chunk_info(search_info, chunk_updates, xpath)


class ChunkSearchAdapter(SearchAdapter):
    ''' An adapter to search Gaia DOM Chunk data.

        This implementation uses the last part of an xpaths as a search key
        and collapses document with chunk info into each search object.

        WARNING: This is only usable if there are no name clashes in this
        trailing part of the xpath!

        This is a default adapter that _may_ be useful for _some_ projects.
        In general, you will need a project-specific adapter: PLEASE NOTE.
    '''

    def __init__(self, dom_item, item_index):
        self.item = dom_item
        self.item_index = item_index

    def get_search_objects(self):
        doc_info = self.item.document().info
        index_chunks = self.item_index.chunks()
        dom_chunks = self.item.chunks()

        chunk_pairs = []
        for chunk_index in index_chunks:
            for dom_chunk in dom_chunks:
                if str(dom_chunk.dom_id) == str(chunk_index.dom_id):    # TODO: review: str() shouldn't be reqd?...
                    chunk_pairs.append((chunk_index, dom_chunk))
                    break

        objs = []
        for chunk_index, dom_chunk in chunk_pairs:
            objs.append(_ChunkSearchObject(self.item, self.item_index, dom_chunk, chunk_index, doc_info))

        return objs

    @classmethod
    def update_search_object(self, search_object, doc_info_changes, page_info_changes, chunk_info_changes):
        ''' Update info in search object with any relevant changes
        '''
        _ChunkSearchObject.update(search_object, doc_info_changes, page_info_changes, chunk_info_changes)

    @classmethod
    def search_id(cls, item_dom_id, item_index_id, chunk_dom_id): 
        # TODO: review: duplication of search_id and qa_link information/usage.
        return _ChunkSearchObject.search_id(item_dom_id, item_index_id, chunk_dom_id)
