from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.meeting.page_meeting import PageMeeting
from project.cho.egest_adapter.doc.report.report import Report
from gaia.gift.gift25 import gift_doc


class PageReport(Report, PageMeeting):
    FEED_GROUP = ChoFeedGroup.MEETING_PAGE

    def gift_doc_document_metadata(self, document_instance):
        try:
            self.log.enter()
            gift_doc_document_metadata_list = []

            meta_document_ids = self.meta_document_ids(document_instance)
            if meta_document_ids is not None:
                gift_doc_document_metadata_list.append(meta_document_ids)

            meta_bibliographic_ids = self.meta_bibliographic_ids_psmid()
            if meta_bibliographic_ids is not None:
                gift_doc_document_metadata_list.append(meta_bibliographic_ids)

            meta_mcode = self.meta_mcode()
            if meta_mcode is not None:
                gift_doc_document_metadata_list.append(meta_mcode)

            meta_record_admin_info = self.meta_record_admin_info()
            if meta_record_admin_info is not None:
                gift_doc_document_metadata_list.append(meta_record_admin_info)

            meta_document_titles = self.meta_document_titles()
            if meta_document_titles is not None:
                gift_doc_document_metadata_list.append(meta_document_titles)

            meta_publication_title = self.meta_publication_title()
            if meta_publication_title is not None:
                gift_doc_document_metadata_list.append(meta_publication_title)

            meta_descriptive_indexing = self.meta_descriptive_indexing()
            if meta_descriptive_indexing is not None:
                gift_doc_document_metadata_list.append(meta_descriptive_indexing)

            meta_folio = self.meta_folio(document_instance)
            if meta_folio is not None:
                gift_doc_document_metadata_list.append(meta_folio)

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()