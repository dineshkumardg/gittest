from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker
from lxml.builder import ElementMaker


class _Etoc(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self,
                              namespace='http://www.gale.com/goldschema/etoc',
                              nsmap={'etoc' : 'http://www.gale.com/goldschema/etoc', },
                              **kwargs)

E = _Etoc()
document = E.document
etoc_unique_id = E.etoc_unique_id
