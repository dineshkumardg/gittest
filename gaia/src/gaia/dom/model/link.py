import copy
from gaia.dom.model.dom_object import _DomObject

class _Link(_DomObject):
    ''' This is a link to any other media (the "target" of this link).
        If the target is not specified, this is a plain "information only" link.

        For example:
            an mp3 file for this document
            the text of another article within this document
            a page in another document
            an article in another document, 
            a specific page of an article in another document
    '''
    
    def __init__(self, dom_id, dom_name, info, source, target):
        _DomObject.__init__(self, dom_id, dom_name, info)
        
        self.source = source
        self.target = target

        # We copy some data into the info object to make it available _just_ via the info dict (eg for the web app)
        self.info.update({'_source': source})
        self.info.update({'_target': target})

    def __str__(self):
        info = copy.copy(self.info)
        del info ['_source']
        del info ['_target']
        return _DomObject. __str__(self, info=info)

class AssetLink(_Link):
    ''' This is a link to an asset in this Item.

        For example: an mp3 file that represents this whole document.

        The source of the link defaults to "this whole document", but may optionally
        have a more specifically defined "source" (ie chunk and/or page where the reference originates from).
    '''
    def __init__(self, dom_id, dom_name, info, asset_fname, source={}):
        # assets may or may not have a source whcih is more specific than "this document"
        target={'asset_fname': asset_fname}
        _Link.__init__(self, dom_id, dom_name, info, source, target)

    @property
    def asset_fname(self):
        return self.target['asset_fname']

class DocumentLink(_Link):
    ' This is an external link to a document (and possibly a page and/or chunk within that document) '
    
    def __init__(self, dom_id, dom_name, info, source, target):
        ''' The source is a dictionary with 2 keys: chunk and page.
            The target is a dictionary with 3 keys: document, chunk and page.

            These should point to the *dom_id* (not dom_name) of the expected target.

            At least one should be set, and others can be set to None.
            (if a target has no document, it's an internal link?)
        
            eg:
             target = {'document': 'cho_iaxx_1000_000_000'],
                       'page':' 7'],
                       'chunk': '27'], 
        '''
        _Link.__init__(self, dom_id, dom_name, info, source, target)
