from project.cho.egest_adapter.doc.journal.journal import Journal
from project.cho.egest_adapter.doc.book.article_book import ArticleBook
from project.cho.egest_adapter.doc.document_error import DocumentError,\
    SourceDataMissing
from gaia.gift.gift25 import meta


class ArticleJournal(Journal, ArticleBook):
    def _meta_descriptive_indexing(self, document_instance):
        return self.meta_descriptive_indexing(document_instance, '21819391', 'Journal')

    def _related_doc_display_link(self, display_link, doc_ref=None):
        return "Link to unpublished version in Meetings and Speeches"

    def _get_two_isbns(self):
        self.log.enter()

        # there can be upto two isbn's, but both must be a different length
        isbn_lengths = self.source_xml_dict['/chapter/metadataInfo/isbn/@length']
        isbns = self.source_xml_dict['/chapter/metadataInfo/isbn']

        self._validate_isbns(isbns, isbn_lengths)

        isbn0 = None
        isbn1 = None

        if isbns is not None:
            if isinstance(isbn_lengths, basestring):
                isbn0 = isbns
            else:
                if len(isbn_lengths) == 2:
                    if isbn_lengths[0] == isbn_lengths[1]:
                        raise DocumentError("2 isbn's with same length!", isbns=isbn_lengths)

                isbn0 = isbns[0]
                isbn1 = isbns[1]

        return isbn0, isbn1

    def get_a_single_isbn(self, document_instance):
        self.log.enter()
        return self.source_xml_dict['/chapter/page/article[%s]/articleInfo/isbn' % document_instance], None

    def meta_bibliographic_ids_psmid_isbn_issn(self, document_instance):  # needs to which article its onn
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            if psmid is None:
                raise SourceDataMissing('PSMID')

            isbn0, isbn1 = self.get_a_single_isbn(document_instance)
            if isbn0 is None:
                isbn0, isbn1 = self._get_two_isbns()

            issn = self.source_xml_dict['/chapter/metadataInfo/issn']
            #  take the 8 numbers and put a dash in-between the 4th and 5th number i.e. 1234-5678
            if issn is not None and len(issn) == 8:
                issn = issn[0:4] + '-' + issn[4:]

            if psmid is not None:
                return meta.bibliographic_ids(
                    'PSM',
                    psmid,
                    'isbn',
                    isbn0,
                    'isbn',
                    isbn1,
                    'issn',
                    issn
                    )
            # else None get's returned
        except TypeError, e:
            raise SourceDataMissing(missing='isbn, issn. ' + str(e))
        finally:
            self.log.exit()
