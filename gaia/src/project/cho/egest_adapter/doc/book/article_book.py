from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.conference_series.article_conference_series import ArticleConferenceSeries
from project.cho.egest_adapter.doc.document_error import SourceDataMissing
from gaia.gift.gift25 import meta, gift_doc
from project.cho.egest_adapter.doc.book.book import Book
from project.cho.egest_adapter.doc.review_foreign_press.review_foreign_press import ReviewForeignPress
from project.cho.egest_adapter.doc.journal.journal import Journal


class ArticleBook(Book, ArticleConferenceSeries):  # left to right order important!
    FEED_GROUP = ChoFeedGroup.ARTICLE

    def gift_doc_document_metadata(self, document_instance):
        self.log.enter()
        gift_doc_document_metadata_list = []

        meta_document_ids = self.meta_document_ids(document_instance)
        if meta_document_ids is not None:
            gift_doc_document_metadata_list.append(meta_document_ids)

        meta_bibliographic_ids = self.meta_bibliographic_ids_psmid_isbn_issn(document_instance)
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

        meta_document_titles = self.meta_document_titles(document_instance)
        if meta_document_titles is not None:
            gift_doc_document_metadata_list.append(meta_document_titles)

        meta_publication_title = self.meta_publication_title()
        if meta_publication_title is not None:
            gift_doc_document_metadata_list.append(meta_publication_title)

        meta_publication_subtitle = self.meta_publication_subtitle()
        if meta_publication_subtitle is not None:
            gift_doc_document_metadata_list.append(meta_publication_subtitle)

        meta_languages = self.meta_languages(document_instance)
        if meta_languages is not None:
            gift_doc_document_metadata_list.append(meta_languages)

        meta_ocr_confidence = self.meta_ocr_confidence(document_instance)
        if meta_ocr_confidence is not None:
            gift_doc_document_metadata_list.append(meta_ocr_confidence)

        meta_authors = self.meta_authors(document_instance)
        if meta_authors is not None:
            gift_doc_document_metadata_list.append(meta_authors)

        meta_editors = self.meta_editors()
        if meta_editors is not None:
            gift_doc_document_metadata_list.append(meta_editors)

        meta_descriptive_indexing = self._meta_descriptive_indexing(document_instance)
        if meta_descriptive_indexing is not None:
            gift_doc_document_metadata_list.append(meta_descriptive_indexing)

        meta_source_institution = self.meta_source_institution()
        if meta_source_institution is not None:
            gift_doc_document_metadata_list.append(meta_source_institution)

        meta_holding_institution = self.meta_holding_institution()
        if meta_holding_institution is not None:
            gift_doc_document_metadata_list.append(meta_holding_institution)

        meta_source_citation_group = self.meta_source_citation_group()
        if meta_source_citation_group is not None:
            gift_doc_document_metadata_list.append(meta_source_citation_group)

        product_content_type = self._product_content_type()
        if product_content_type is not None:
            gift_doc_document_metadata_list.append(product_content_type)

        self.log.exit()

        return gift_doc.document_metadata(*gift_doc_document_metadata_list)

    def _meta_descriptive_indexing(self, document_instance):
        return self.meta_descriptive_indexing(document_instance, '14186620', 'Monograph')

    def gift_doc_node_metadata(self, article):
        try:
            self.log.enter()

            args = []

            args.append(meta.descriptive_indexing(
                meta.indexing_term(
                    meta.term(
                        'PUB_SEG_TYPE',
                        'Atlas',
                        '14242630',
                        'Article')
                    )
                )
            )

            volumne_number = self.source_xml_dict['/chapter/citation/%s/volumeGroup/volumeNumber' % self.content_type()]
            if volumne_number is not None:
                args.append(meta.volume_number(volumne_number))

            '''
            For Refugee Survey (PSMID beginning with cho_rsxx) should not have an issue number.
            For Weekly Review of Foreign Press (PSMID beginning with cho_rfpx) should always have an issue number.
            For Journals, /chapter/page/article/@type="article" must have an issue number. Any other article type is optional.
            '''
            page_article_is_on, article_index_on_page = self._find_page_article_on(article)
            issue_number_xpath = '/chapter/page[%s]/article[%s]/articleInfo/issueNumber' % (page_article_is_on, article_index_on_page)
            issue_number = self.source_xml_dict[issue_number_xpath]
            if isinstance(self, ReviewForeignPress):
                if issue_number is not None:
                    args.append(meta.issue_number(issue_number))
                else:
                    raise SourceDataMissing('issueNumber', issue_number_xpath=issue_number_xpath)
            elif isinstance(self, Journal):
                article_type = self.source_xml_dict['/chapter/page[%s]/article[%s]/@type' % (page_article_is_on, article_index_on_page)]
                if article_type == 'article':
                    if issue_number is not None:
                        args.append(meta.issue_number(issue_number))
                    else:
                        raise SourceDataMissing('issueNumber')

            pagination_args = []
            pagination_args.append(meta.total_pages(self.total_pages_of_article(article)))

            meta_begin_page, meta_end_page = self._meta_range(article)

            range_args = []

            if meta_begin_page is not None:
                range_args.append(meta.begin_page(meta_begin_page))

            # we can only have an end-page if there is a begin-page
            if meta_begin_page is not None and meta_end_page is not None:
                range_args.append(meta.end_page(meta_end_page))

            if len(range_args) > 0:
                meta_ranges = meta.ranges(
                    meta.range(*range_args)
                    )
                pagination_args.append(meta_ranges)

            args.append(gift_doc.pagination_group(
                gift_doc.pagination(
                    *pagination_args
                    )
                )
            )

            return gift_doc.node_metadata(
                *args
                )
        finally:
            self.log.exit()
