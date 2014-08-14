import os
from gaia.log.log import Log
from StringIO import StringIO
from lxml import etree
from document_error import GiftValidationError, InvalidXmlError
from gaia.dom.document_error import InvalidXmlSchema
import gc


class DocumentInstances:
    ' create a list of gift document instances using the doc-instance builders provided. '
    def __init__(self, config, source_xml_dict, builders, extra_args):
        self.log = Log.get_logger(self)
        self.config = config
        self.source_xml_dict = source_xml_dict
        self.builders = builders
        self.extra_args = extra_args

        self.gift_xsd = os.path.join(os.path.dirname(__file__), '../../../../cengage/gift/feed.xsd')
        try:
            # to check if the schema - .xsd is fine
            self.schema = etree.XMLSchema(file = self.gift_xsd)
        except etree.XMLSchemaParseError, e:
            raise InvalidXmlSchema(self.gift_xsd, e)

    def document_instances(self):
        ' return document-instance strings grouped by ChoFeedGroup '
        docs = {}   # a dictionary of group: doc-instances
        for builder_class in self.builders:
            builder = builder_class(self.config, self.source_xml_dict, self.extra_args)
            group = builder_class.FEED_GROUP

            if not group in docs:
                docs[group] = []

            document_instances = builder.document_instances()

            for document_instance in document_instances:
                self._validate(document_instance)
                collected = gc.collect()
                self.log.info('gc validation collected %d objects' % collected)

            docs[group].extend(document_instances)
        return docs

    def _validate(self, document_instance):
        self.log.enter()  

        # we have to validate off <gold:feed/>
        feed_header = '''<gold:feed xmlns:essay="http://www.gale.com/goldschema/essay" xmlns:gold="http://www.gale.com/gold" xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc" xmlns:dir="http://www.gale.com/goldschema/dir" xmlns:vault-link="http://www.gale.com/goldschema/vault-linking" xmlns:meta="http://www.gale.com/goldschema/metadata" xmlns:table="http://www.gale.com/goldschema/table" xmlns:xatts="http://www.gale.com/goldschema/xatts" xmlns:index="http://www.gale.com/goldschema/index" xmlns:mla="http://www.gale.com/goldschema/mla" xmlns:media="http://www.gale.com/goldschema/media" xmlns:tt="http://www.w3.org/ns/ttml" xmlns:list="http://www.gale.com/goldschema/list" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:etoc="http://www.gale.com/goldschema/etoc" xmlns:verse="http://www.gale.com/goldschema/verse" xmlns:pres="http://www.gale.com/goldschema/pres" xmlns:pub-meta="http://www.gale.com/goldschema/pub-meta" xmlns:shared="http://www.gale.com/goldschema/shared" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:math="http://www.w3.org/1998/Math/MathML" id="PSM-CHOA_20130724_005">'''
        #feed_body = ''
        feed_body = document_instance
        feed_footer = '''  <gold:metadata><gold:feed-type>PSM</gold:feed-type><gold:document-schema>gift_document.xsd</gold:document-schema><gold:schema-version>2.5</gold:schema-version><gold:document-id-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value</gold:document-id-path><gold:document-mcode-path>//gift-doc:document/gift-doc:metadata/gift-doc:document-metadata/meta:mcode</gold:document-mcode-path><gold:number-of-documents>1</gold:number-of-documents><gold:feed-status>New-Replace</gold:feed-status></gold:metadata></gold:feed>'''
        feed = feed_header + feed_body + feed_footer

        try:
            # to check if the doc_instance - xml validates the schema .xsd
            xml_doc = etree.parse(StringIO(feed))
            self.schema.assertValid(xml_doc)

        except etree.XMLSyntaxError, e:
            self.log.info(e)
            raise InvalidXmlError(error=e)  # doc-inst is not well formed
        except etree.DocumentInvalid, e:
            self.log.info(e)
            raise GiftValidationError(missing=e)  # doc-inst does not validate against XSD

        self.log.exit()
