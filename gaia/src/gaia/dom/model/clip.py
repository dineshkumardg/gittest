from gaia.dom.model.dom_object import _DomObject
import copy

class Clip(_DomObject):
    ''' This is like one torn-out piece of one paper page.

        No info means that the clip spans the whole page. (?)
    '''

    def __init__(self, dom_id, dom_name, page_id, info):
        _DomObject. __init__(self, dom_id, dom_name, info)
        self.page_id = page_id

        self.info.update({'_page_id': page_id})

    def __str__(self):
        info = copy.copy(self.info)
        del info ['_page_id']

        return _DomObject. __str__(self, info=info, page_id=self.page_id)
