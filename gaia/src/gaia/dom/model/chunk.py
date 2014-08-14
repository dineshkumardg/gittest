import copy
from gaia.error import GaiaCodingError
from gaia.dom.model.dom_object import _DomObject

class Chunk(_DomObject):
    ''' This is something like an article in a newspaper (or a chapter in a book; or a section of a magazine?).
    
        Chunks appear on Pages indirectly via Clips.
        In Chatham house, there are no clips, so we're linking directly to Page Ids.
        This needs review: TODO
    '''

    def __init__(self, dom_id, dom_name, info, page_ids, clip_ids=None, is_binary=False):
        if not clip_ids and not page_ids:
            raise GaiaCodingError('A Gaia DOM Chunk requires either clip_ids or page_ids; both cannot be empty!')

        _DomObject. __init__(self, dom_id, dom_name, info)

        self.page_ids = page_ids
        self.clip_ids = clip_ids    # Not sure about clip_ids and/or page_ids, but we'll go with this for now/Chatham House.
        # Probably should derive the page_ids from the clip_ids (when provided)...? (see below)
        # self.chunk_refs = chunk_refs # TODO??: links to other chunks?? eg binary chunks: Illustrations, diagrams wihtin the article, etc?..
        self.is_binary = is_binary

        # We copy some data into the info object to make it available _just_ via the info dict (eg for the web app)
        self.info.update({'_page_ids': page_ids, '_clip_ids': clip_ids, '_is_binary': is_binary})

    def __str__(self):
        info = copy.copy(self.info)
        del info ['_page_ids']
        del info ['_clip_ids']
        del info ['_is_binary']

        return _DomObject. __str__(self, info=info, page_ids=self.page_ids, clip_ids=self.clip_ids, is_binary=self.is_binary)
