from lxml import etree
from gaia.error import GaiaError, GaiaErrors
from gaia.dom.document_error import InvalidXmlSchema, InvalidXml

class XmlParseError(GaiaError):
    pass

class _Schema:
    _schema_class = None # override this

    @classmethod
    def validate(cls, xml_fpath, xsd_fpath):
        ' validate an xml file against a schema '
        try:
            _etree = etree.parse(xml_fpath)
        except etree.XMLSyntaxError, e:
            raise XmlParseError(xml_file=xml_fpath, error=e)
           
        try:
            schema = cls._schema_class(file=xsd_fpath)
        except etree.XMLSchemaParseError, e:
            raise InvalidXmlSchema(xsd_fpath, e)
        
        valid = schema.validate(_etree)
        
        if not valid:
            raise cls._validation_errors(schema, xsd_fpath, xml_fpath)
       
    @classmethod
    def _validation_errors(cls, schema, xsd_fpath, xml_fname):
        errors = schema.error_log.filter_from_errors()
        _errors = []
        for err in errors:
            validation_err = InvalidXml(xml_fname, xsd_fpath, err.line, err.message)
            _errors.append(validation_err)
            
        return GaiaErrors(*_errors)
       
class Xsd(_Schema):
    _schema_class = etree.XMLSchema

class Dtd(_Schema):
    _schema_class = etree.DTD
