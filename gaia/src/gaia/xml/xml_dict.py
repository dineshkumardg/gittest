from lxml import etree
from gaia.error import GaiaCodingError
from gaia.log.log import Log


class XmlDict:
    ''' Access an XML eTree as a (limited) dictionary.

        Keys are xpaths addressing nodes OR attributes.
        Values are the values of those nodes (eg a node's text or an attribute's value).
        If there are multiple nodes, a list of all of them is returned as the value.

        Values can be get or set.
    '''

    def __init__(self, _etree):
        self._etree = _etree
        self._log = Log.get_logger(self)

    def _val(self, node):
        #if nodes[0].is_text:   #??? doesn't work!
        if isinstance(node, etree._Element):
            if node.text == None:
                return None
            value = unicode(node.text)
        else:   # if isinstance(nodes[0], etree._ElementStringResult): (for attributes)
            if node == None:
                return None
            value = unicode(node)

        # either we have an empty (self-closing) node or a node with empty text contents
        if len(value) == 0:
            return None

        return value

    def __getitem__(self, xpath):
        ''' return the value of the xpath expression as a unicode string
            (or None if not present).

            Note: if there are multiple matches, a LIST will be returned.

            Use more explicit addressing to avoid this please:
            this is a safe default, eg
                '/book/title[1]' instead of just
                '/book/title'

            Note: this is a NoneDict not a normal dict (ie does NOT raise KeyError)
        '''
        try:
            nodes = self._etree.xpath(xpath)

            if len(nodes) == 0:
                return None
            elif len(nodes) == 1:
                return self._val(nodes[0])  # NOTE: string/unicode (NOT a list)
            else:
                return [self._val(node) for node in nodes]  # NOTE: returns a LIST

        except etree.XPathEvalError, e:
            raise GaiaCodingError('XmlDict.getitem() failed: Problem with xpath', xpath=xpath, error=e)

    def __setitem__(self, xpath, value):
        ''' Set the value of a node (or attribute) using the xpath as a key.
        '''
        attr = None

        try:
            if '@' in xpath:
                xpath, attr = xpath.split('@')  # we expect only one attribute (at the end)
                xpath = xpath[:-1]  # strip the trailing slash

            nodes = self._etree.xpath(xpath)

            if len(nodes) == 0:
                raise GaiaCodingError('Tried to set an xpath that does not exist.', xpath=xpath)  # Note: *not* a KeyError as it should be.
            elif len(nodes) > 1:
                self._log.warning('XmlDict.setitem(): only setting first of MULTIPLE NODE MATCHES', xpath=xpath, value=value)

            if isinstance(nodes[0], etree._Element):  # is_text
                if attr:
                    nodes[0].attrib[attr] = value
                else:
                    nodes[0].text = value
                # Note: could change all nodes here if we wanted? spec??
                # TODO...
            else:   # if isinstance(nodes[0], etree._ElementStringResult): (for attributes)
                nodes[0] = value  # ??

        except etree.XPathEvalError, e:
            raise GaiaCodingError('XmlDict.setitem() failed: Problem with xpath', xpath=xpath, error=e)
