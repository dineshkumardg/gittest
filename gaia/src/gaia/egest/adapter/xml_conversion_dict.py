
from gaia.xml.cached_xml_dict import CachedXmlDict
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter


class XmlConversionDict(CachedXmlDict):
    ''' For conversion, we don't want to see _IS_ABSENT_ markers, we
        need None instead.
    '''
    def __getitem__(self, xpath):
        val = CachedXmlDict.__getitem__(self, xpath)
        if val == GaiaDomAdapter.MISSING_FIELD_VALUE:
            return None
        else:
            return val
