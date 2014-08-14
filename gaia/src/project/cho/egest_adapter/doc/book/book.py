from gaia.gift.gift25 import meta
from project.cho.egest_adapter.doc.document_error import SourceDataMissing

class Book:
    def meta_publication_subtitle(self):
        try:
            self.log.enter()

            publication_subtitle = self.source_xml_dict['/chapter/citation/%s/titleGroup/fullSubtitle' % self.content_type()]
            if publication_subtitle is not None:
                return meta.publication_subtitle(publication_subtitle)
            else:
                return None  # it's an optional element
        finally:
            self.log.exit()

    def meta_publication_title(self):
        try:
            self.log.enter()

            xpath = '/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()
            publication_title = self.source_xml_dict[xpath]
            if publication_title is not None:
                return meta.publication_title(publication_title)
            else:
                raise SourceDataMissing('titleGroup/fullTitle', xpath=xpath)
        finally:
            self.log.exit()
