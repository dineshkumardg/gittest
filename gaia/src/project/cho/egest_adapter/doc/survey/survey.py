from project.cho.egest_adapter.doc.document import Document
from project.cho.egest_adapter.doc.document_error import McodeMissing, McodeDuplicate


class Survey:
    def __init__(self, config, source_xml_dict, extra_args):
        Document.__init__(self, config, source_xml_dict, extra_args)
        self.asset_id_chunk_dict = {}

    def mcode_dict(self, lookup_key):  # TODO refactor commonality?
        mcode = MCodes.objects.filter(psmid=lookup_key)
        if len(mcode) == 0:
            raise McodeMissing('Tried to release an item, but we do not yet have an MCode for this item', psm_id=lookup_key)
        if len(mcode) > 1:
            raise McodeDuplicate('Tried to release an item, but found more than 1 mcode in the database', psm_id=lookup_key)
        return  mcode[0].mcode