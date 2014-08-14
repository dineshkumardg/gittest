from project.cho.egest_adapter.doc.document_error import SourceDataMissing, DocumentError
from project.cho.egest_adapter.doc.document import Document
from gaia.gift.gift25 import meta
from project.cho.hard_coded_mcodes import HardCodedMCodes


class Meeting(Document):
    def meta_mcode(self):
        return meta.mcode(HardCodedMCodes.mcode_from_psmid(self.psmid()))

    def __init__(self, config, source_xml_dict, extra_args):
        Document.__init__(self, config, source_xml_dict, extra_args)

    def file_size(self, fname, fname_extension):
        # fname might OR might not (!) have a filename extension - this has been confirmed by Sarah Neate.
        try:
            # try with no file extension on fname
            return self.extra_args['file_size']['%s.%s' % (fname, fname_extension)]
        except KeyError, e:
            # try with a filename extension on fname
            self.log.debug(fname=fname, fname_extension=fname_extension)
            try:
                return self.extra_args['file_size']['%s' % fname]
            except KeyError, e:
                raise DocumentError('unable to lookup file_size from extra_args', fname=fname, fname_extension=fname_extension)

    def fname(self):
        return 'PSM-%s-%s-%s_%s.xml' % (self.config.content_set_name, self.creation_date(), self.psmid(), self.fname_type)

    def psmid(self):
        try:
            self.log.enter()
            return self.source_xml_dict['/chapter/metadataInfo/PSMID']
        finally:
            self.log.exit()

    def publication_segment_type(self):
        value = self.source_xml_dict['/chapter/page/article/@type']

        # support multiple articles
        if isinstance(value, basestring):
            article_type = value
        else:
            article_type = value[0]  # we're only interested in the first

        if article_type == 'article':
            return 'Article'
        else:
            raise SourceDataMissing('article/@type')
