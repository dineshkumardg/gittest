from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.conference_series.parent_conference_series import ParentConferenceSeries
from project.cho.egest_adapter.doc.book.book import Book
from gaia.gift.gift25 import gift_doc


class ParentBook(Book, ParentConferenceSeries):
    FEED_GROUP = ChoFeedGroup.ISSUE

    def gift_doc_document_metadata(self):
        try:
            self.log.enter()
            gift_doc_document_metadata_list = []

            meta_document_ids = self.meta_document_ids()
            if meta_document_ids is not None:
                gift_doc_document_metadata_list.append(meta_document_ids)

            meta_bibliographic_ids = self.meta_bibliographic_ids_psmid_isbn_issn()
            if meta_bibliographic_ids is not None:
                gift_doc_document_metadata_list.append(meta_bibliographic_ids)

            meta_mcode = self.meta_mcode()
            if meta_mcode is not None:
                gift_doc_document_metadata_list.append(meta_mcode)

            meta_publication_date = self.meta_publication_date()
            if meta_publication_date is not None:
                gift_doc_document_metadata_list.append(meta_publication_date)

            meta_record_admin_info = self.meta_record_admin_info()
            if meta_record_admin_info is not None:
                gift_doc_document_metadata_list.append(meta_record_admin_info)

            meta_publication_title = self.meta_publication_title()
            if meta_publication_title is not None:
                gift_doc_document_metadata_list.append(meta_publication_title)

            meta_languages = self.meta_languages()
            if meta_languages is not None:
                gift_doc_document_metadata_list.append(meta_languages)

            meta_ocr_confidence = self.meta_ocr_confidence()
            if meta_ocr_confidence is not None:
                gift_doc_document_metadata_list.append(meta_ocr_confidence)

            meta_authors = self.meta_authors()
            if meta_authors is not None:
                gift_doc_document_metadata_list.append(meta_authors)

            meta_editors = self.meta_editors()
            if meta_editors is not None:
                gift_doc_document_metadata_list.append(meta_editors)

            meta_descriptive_indexing = self.meta_descriptive_indexing()
            if meta_descriptive_indexing is not None:
                gift_doc_document_metadata_list.append(meta_descriptive_indexing)

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()
