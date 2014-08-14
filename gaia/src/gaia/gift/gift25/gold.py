from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker
from lxml.builder import ElementMaker


class _Gold(HyphenElementMaker):
    def __init__(self, **kwargs):
        ElementMaker.__init__(self, namespace='http://www.gale.com/gold', nsmap={'gold' : 'http://www.gale.com/gold', }, **kwargs)

def metadata(_feed_type, _document_schema, _schema_version, _document_id_path, _document_mcode_path, _number_of_documents, _feed_status):
    return _metadata(
        feed_type(_feed_type),
        document_schema(_document_schema),
        schema_version(_schema_version),
        document_id_path(_document_id_path),
        document_mcode_path(_document_mcode_path),
        number_of_documents(str(_number_of_documents)),
        feed_status(_feed_status)
        )

E = _Gold()
_metadata = E.metadata
feed_type = E.feed_type
document_schema = E.document_schema
schema_version = E.schema_version
document_id_path = E.document_id_path
document_mcode_path = E.document_mcode_path
number_of_documents = E.number_of_documents
feed_status = E.feed_status
document_instance = E.document_instance
