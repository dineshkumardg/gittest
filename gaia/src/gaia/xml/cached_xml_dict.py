from lxml import etree
from gaia.error import GaiaCodingError
from gaia.xml.xml_dict import XmlDict

class _NormalisedXpath:
    @staticmethod
    def normalise(xml_etree, xpath):
        ' make sure that anything that needs a [1] has a [1] in a path segment. '
        try:
            parts = xpath.split('/')

            for length in range(0, len(parts)):
                if length == 0 and parts[0] == '':
                    xpath = '/' # make sure we join a slash at the front! (string.join() is a bit annoying! :( )
                else:
                    xpath = '/'.join(parts[:length+1])

                    if not xpath.endswith(']'):               # we only care about unqualified paths
                        parts[length] = parts[length] + '[1]' # use the qualified form ALWAYS in these cases

            return xpath

        except etree.XPathEvalError, e:
            raise GaiaCodingError('CachedXmlDict: Problem with invalid xpath', xpath=xpath, error=e)

class CachedXmlDict(XmlDict):
    ''' A read-only XmlDict with a read-thru cache

        On initialisation, pass in a set of dicts with xpaths:value to set the contents of the cache.
    '''

    def __init__(self, _etree, *cache_dicts):
        XmlDict.__init__(self, _etree)
        self._cache = {}

        for cache_dict in cache_dicts:
            for xpath, val in cache_dict.items():
                norm_xpath = _NormalisedXpath.normalise(_etree, xpath)
                #print "INIT:      xpath=", xpath
                #print "INIT: norm_xpath=", norm_xpath
                self._cache[norm_xpath] = val

    def __getitem__(self, xpath):
        try:
            norm_xpath = _NormalisedXpath.normalise(self._etree, xpath)
            #print "GET :      xpath=", xpath
            #print "GET : norm_xpath=", norm_xpath
            return self._cache[norm_xpath]

        except KeyError, e: # cache miss
            return XmlDict.__getitem__(self, xpath) # or norm_xpath? shouldn't make a difference.

    def __setitem__(self, xpath, value):
        raise GaiaCodingError('CachedXmlDict.setitem() called, but this class is READ ONLY! ')
