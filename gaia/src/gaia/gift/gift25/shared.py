from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker
from lxml.builder import ElementMaker


class _Shared(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self, namespace='http://www.gale.com/goldschema/shared', nsmap={'shared' : 'http://www.gale.com/goldschema/shared', }, **kwargs)

E = _Shared()
media = E.media
