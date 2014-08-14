from lxml.builder import ElementMaker
from gaia.gift.gift25 import gold
from gaia.gift.gift25.hyphen_element_maker import attr, HyphenElementMaker
from lxml import etree
from test_utils.sorted_dict import sorted_dict


class _GoldFeedWrapper(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self,
              namespace='http://www.gale.com/gold',
              nsmap=sorted_dict({
                    'dir' : 'http://www.gale.com/goldschema/dir',
                    'essay' : 'http://www.gale.com/goldschema/essay',
                    'etoc' : 'http://www.gale.com/goldschema/etoc',
                    'gift-doc' : 'http://www.gale.com/goldschema/gift-doc',
                    'gold' : 'http://www.gale.com/gold',
                    'index' : 'http://www.gale.com/goldschema/index',
                    'list' : 'http://www.gale.com/goldschema/list',
                    'math' : 'http://www.w3.org/1998/Math/MathML',
                    'media' : 'http://www.gale.com/goldschema/media',
                    'meta' : 'http://www.gale.com/goldschema/metadata',
                    'mla' : 'http://www.gale.com/goldschema/mla',
                    'pres' : 'http://www.gale.com/goldschema/pres',
                    'pub-meta' : 'http://www.gale.com/goldschema/pub-meta',
                    'shared' : 'http://www.gale.com/goldschema/shared',
                    'table' : 'http://www.gale.com/goldschema/table',
                    'tt' : 'http://www.w3.org/ns/ttml',
                    'vault-link' : 'http://www.gale.com/goldschema/vault-linking',
                    'verse' : 'http://www.gale.com/goldschema/verse',
                    'xatts' : 'http://www.gale.com/goldschema/xatts',
                    'xlink' : 'http://www.w3.org/1999/xlink',
                    'xsi' : 'http://www.w3.org/2001/XMLSchema-instance',
                    }),
              **kwargs)

E = _GoldFeedWrapper()
wrapper = E.feed


class FeedWrapper:
    ''' Split the Gift Feed Wrapper into 2 strings "header" and "footer'
        to support writing large feed files.
    '''

    def __init__(self, number_of_documents, feed_id, is_indexed):
        ''' feed_id is any unique id (I think)
        '''
        self.is_indexed = is_indexed
        self.number_of_documents = str(number_of_documents)
        marker = '_x_DI_x_'  # document-instances replace this

        if self.is_indexed:
            feed_type = 'PSM'
        else:
            feed_type = 'NOINDEX'

        feed = wrapper(
            attr('id', feed_id),
            attr('{%s}schemaLocation' % 'http://www.w3.org/2001/XMLSchema-instance', '..\\..\\..\\..\\..\\GIFT\\feed_schemas\\feed.xsd'),  # RE: https://mailman-mail5.webfaction.com/pipermail/lxml/2010-March/005346.html
            marker,
            gold.metadata(
                    feed_type,
                    'gift_document.xsd',
                    '2.5',  # schema_version
                    '//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value',
                    '//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode',
                    self.number_of_documents,
                    'New-Replace',  # always this on Ocean, and for us on LST
                )
            )

        # This is a naff way of doing this, but good enough.
        self._header, self._footer = etree.tostring(feed, pretty_print=True).split(marker, 1)  # allow us to have open and close tag off marker

        self._header = '<?xml version="1.0" encoding="UTF-8"?>' + self._header

    def header(self):
        return self._header

    def footer(self):
        return self._footer
