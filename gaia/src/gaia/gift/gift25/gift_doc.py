from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker
from lxml.builder import ElementMaker


class _GiftDoc(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self,
                              namespace='http://www.gale.com/goldschema/gift-doc',
                              nsmap={'gift-doc' : 'http://www.gale.com/goldschema/gift-doc', },
                              **kwargs)

E = _GiftDoc()
document_titles = E.document_titles
node_metadata = E.node_metadata
document = E.document
metadata = E.metadata
body = E.body
document_metadata = E.document_metadata
pagination_group = E.pagination_group
pagination = E.pagination
