from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.meeting.mega_meeting import MegaMeeting
from project.cho.egest_adapter.doc.report.report import Report
from gaia.gift.gift25 import meta, essay, shared, media, vault_link, gift_doc
from project.cho.egest_adapter.doc.document_error import SourceDataMissing, DocumentError
from gaia.gift.gift25.hyphen_element_maker import attr


class MegaReport(Report, MegaMeeting):
    FEED_GROUP = ChoFeedGroup.MEETING_MEGA

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

            meta_document_titles = self.meta_document_titles()
            if meta_document_titles is not None:
                gift_doc_document_metadata_list.append(meta_document_titles)

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

            meta_source_institution = self.meta_source_institution()
            if meta_source_institution is not None:
                gift_doc_document_metadata_list.append(meta_source_institution)

            meta_holding_institution = self.meta_holding_institution()
            if meta_holding_institution is not None:
                gift_doc_document_metadata_list.append(meta_holding_institution)

            meta_source_citation_group = self.meta_source_citation_group()
            if meta_source_citation_group is not None:
                gift_doc_document_metadata_list.append(meta_source_citation_group)

            meta_product_content_type = self.meta_product_content_type()
            if meta_product_content_type is not None:
                gift_doc_document_metadata_list.append(meta_product_content_type)

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()

    def essay_container_divs(self):
        try:
            self.log.enter()

            number_of_pages = int(self.total_pages())
            div_list = []

            for page in range(1, number_of_pages + 1):
                div_list.append(self.essay_divs_from_page(page))

            div_container = essay.div_container(
                'Body text',
                '14214508',
                'Atlas',
                div_list
                )

            return div_container
        finally:
            self.log.exit()

    def essay_divs_from_page(self, page):
        try:
            self.log.enter()
            contents_list = []

            complex_meta_list = []

            page_id_number_xpath = '/chapter/page[%s]/pageImage' % page
            page_id_number = self.source_xml_dict[page_id_number_xpath]

            if page_id_number is None or len(page_id_number) < 5:
                raise SourceDataMissing('articlePage number', page_id_number_xpath=page_id_number_xpath)
            else:
                page_id_number = page_id_number[-4:len(page_id_number)]
                complex_meta_list.append(meta.page_id_number(unicode(page_id_number)))

            # effectively the article path has some info, and separately, so does this path
            source_page = self.source_xml_dict['/chapter/page[%s]/sourcePage' % page_id_number.lstrip('0')]
            if source_page is not None:
                complex_meta_list.append(meta.folio(
                    meta.start_number(source_page)
                    )
                )

            contents_list.append(
                essay.complex_meta(
                    *complex_meta_list
                    )
                )

            # find all pgref_value's that = page we're on 
            for text_clip in self.page_article_textclip_pgrefs:
                if int(text_clip['pgref_value']) == page:
                    contents_list.append(
                        self.essay_p(text_clip['page_index'], text_clip['article_index'], text_clip['textclip_index'])
                        )

            sequence = page_id_number

            width_xpath = '/chapter/page[%s]/pageImage/@width' % page
            width = self.source_xml_dict[width_xpath]
            if width is None:
                raise SourceDataMissing('pageImage/@width', width_xpath=width_xpath)

            height_xpath = '/chapter/page[%s]/pageImage/@height' % page
            height = self.source_xml_dict[height_xpath]
            if height is None:
                raise SourceDataMissing('pageImage/@height', height_xpath=height_xpath)

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % page]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % page]
            if where.endswith('.jpg'):
                where = where[:-4]

            contents_list.append(shared.media(
                media.image(
                    data_type='jpeg',
                    height=height,
                    width=width,
                    image_type='page view',
                    layout='single',
                    color_mode='color',
                    folio=folio,
                    sequence=sequence,
                    vault_link=vault_link.vault_link(
                        _link_type='external',
                        _action='point',
                        where_path=where)
                    ),
                    *self._media_images(page)
                )
            )

            asset_id = self.asset_id(page)
            if asset_id is None:
                raise DocumentError('No Asset Id', page=page)

            where = '//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id
            contents_list.append(
                vault_link.vault_link(
                    _link_type='external',
                    term_id='21902636',
                    term_source='Atlas',
                    _category='DVI page',
                    _action='point',
                    where_path=where,
                    _target='ancestor::gift-doc:document'
                    )
                )

            return essay.div(
                'Page',
                '21922233',
                'Atlas',
                elements=contents_list
                )
        finally:
            self.log.exit()

    def _media_images(self, page):
        # find all illustrations for this page 

        try:
            self.log.enter()

            illustrations_on_page_article = []

            if self.page_article_illustration_pgrefs is not None:
                for page_article_illustration_pgref in self.page_article_illustration_pgrefs:
                    if int(page_article_illustration_pgref['illustration_pgref']) == page:
                        illustrations_on_page_article.append(self.shared_media_illustration_image(page_article_illustration_pgref))

            return illustrations_on_page_article
        finally:
            self.log.exit()

    def meta_product_content_type(self):
        try:
            self.log.enter()

            product_content_type = 'Pamphlets and Reports'

            return meta.product_content_type(
                attr('type', 'CHO'),
                product_content_type
                )
        finally:
            self.log.exit()

    def meta_publication_title(self):
        return meta.publication_title(
            'Chatham House Pamphlets and Reports'
            )

    def meta_source_institution(self):
        return meta.source_institution(
            'Chatham House',
            'London',
            self.copyright_statement(),
            )

    def meta_source_citation_group(self):
        try:
            self.log.enter()

            source_citations = []

            meta_publication_date = self.meta_publication_date()
            if meta_publication_date is not None:
                source_citations.append(meta_publication_date)

            meta_standard_ids = self.meta_standard_ids()
            if meta_standard_ids is not None:
                source_citations.append(meta_standard_ids)

            meta_publisher = self.meta_publisher()
            if meta_publisher is not None:
                source_citations.append(meta_publisher)

            meta_edition = self.meta_edition()
            if meta_edition is not None:
                source_citations.append(meta_edition)

            meta_edition_statement = self.meta_edition_statement()
            if meta_edition_statement is not None:
                source_citations.append(meta_edition_statement)

            meta_place_of_publication = self.meta_place_of_publication()
            if meta_place_of_publication is not None:
                source_citations.append(meta_place_of_publication)

            meta_imprint = self.meta_imprint()
            if meta_imprint is not None:
                source_citations.append(meta_imprint)

            meta_series_info = self.meta_series_info()
            if meta_series_info is not None:
                source_citations.append(meta_series_info)

            meta_content_date = self.meta_content_date()
            if meta_content_date is not None:
                source_citations.append(meta_content_date)

            return meta.source_citation_group(
                meta.source_citation(
                    attr('type', 'DVI monograph'),
                    *source_citations
                    )
                )
        finally:
            self.log.exit()

    def meta_standard_ids(self):  # TODO refactor commonality of isbn / issn in this class?
        try:
            self.log.enter()

            standard_ids = []

            isbns = self.source_xml_dict['/chapter/metadataInfo/isbn']
            if isbns is not None:
                isbn_lengths = self.source_xml_dict['/chapter/metadataInfo/isbn/@length']
                self._validate_isbns(isbns, isbn_lengths)
                if isinstance(isbns, basestring):
                    meta_isbn = meta.id(attr('type', 'isbn'), meta.value(isbns))
                    standard_ids.append(meta_isbn)
                else:
                    for isbn in isbns:
                        meta_isbn = meta.id(attr('type', 'isbn'), meta.value(isbn))
                        standard_ids.append(meta_isbn)

            issn = self.source_xml_dict['/chapter/metadataInfo/issn']
            if issn is not None and len(issn) == 8:
                issn = issn[0:4] + '-' + issn[4:]
                meta_issn = meta.id(attr('type', 'issn'), meta.value(issn))
                standard_ids.append(meta_issn)

            if isbns is not None or issn is not None:
                return meta.standard_ids(*standard_ids)
            else:
                return None
        finally:
            self.log.exit()

    def meta_publisher(self):
        try:
            self.log.enter()

            publisher_xpath = '/chapter/citation/%s/imprint/imprintPublisher' % self.content_type()
            publisher = self.source_xml_dict[publisher_xpath]
            if publisher is None:
                raise SourceDataMissing('imprintPublisher', publisher_xpath=publisher_xpath)
            else:
                return meta.publisher(publisher)
        finally:
            self.log.exit()

    def meta_place_of_publication(self):
        try:
            self.log.enter()

            place_of_publication = self.source_xml_dict['/chapter/citation/%s/publicationPlace/publicationPlaceComposed' % self.content_type()]
            if place_of_publication is None:
                return None
            else:
                return meta.place_of_publication(place_of_publication)
        finally:
            self.log.exit()

    def meta_imprint(self):
        try:
            self.log.enter()

            imprint_xpath = '/chapter/citation/%s/imprint/imprintFull' % self.content_type()
            imprint = self.source_xml_dict[imprint_xpath]
            if imprint is None:
                raise SourceDataMissing('imprintFull', imprint_xpath=imprint_xpath)

            place_of_publication = self.source_xml_dict['/chapter/citation/%s/publicationPlace/publicationPlaceCity' % self.content_type()]
            if place_of_publication is None:
                place_of_publication = ''
            else:
                place_of_publication += ': '
            publisher = self.source_xml_dict['/chapter/citation/%s/imprint/imprintPublisher' % self.content_type()]

            place_of_publication_publisher = '%s%s' % (place_of_publication, publisher)

            year = self.source_xml_dict['/chapter/citation/%s/pubDate/year' % self.content_type()]
            composed = year

            if year is None:
                year_xpath = '/chapter/citation/%s/pubDate/irregular' % self.content_type()
                year = self.source_xml_dict[year_xpath]
                if year is None:
                    raise SourceDataMissing('year', year_xpath=year_xpath)

            manufacturer = self.source_xml_dict['/chapter/citation/%s/imprint/imprintManufacturer' % self.content_type()]
            if manufacturer is None:
                manufacturer = ''
            else:
                manufacturer = ', %s' % manufacturer

            composed = '%s%s' % (year, manufacturer)

            imprint_composed = '%s, %s' % (place_of_publication_publisher, composed)
            return meta.imprint(
                meta.imprint_composed(imprint_composed)
                )
        finally:
            self.log.exit()

    def meta_edition(self):
        try:
            self.log.enter()

            edition_number = self.source_xml_dict['/chapter/citation/%s/editionNumber' % self.content_type()]
            if edition_number is None:
                return None
            else:
                return meta.edition(edition_number)
        finally:
            self.log.exit()

    def meta_edition_statement(self):
        try:
            self.log.enter()

            edition_statement = self.source_xml_dict['/chapter/citation/%s/editionStatement' % self.content_type()]
            if edition_statement is None:
                return None
            else:
                return meta.edition_statement(edition_statement)
        finally:
            self.log.exit()

    def meta_series_info(self):
        try:
            self.log.enter()

            series_info = []
            meta_title = self.source_xml_dict['/chapter/citation/%s/seriesGroup/seriesTitle' % self.content_type()]
            if meta_title is not None:
                series_info.append(
                    meta.title(meta_title)
                )

            meta_number = self.source_xml_dict['/chapter/citation/%s/seriesGroup/seriesNumber' % self.content_type()]
            if meta_number is not None:
                series_info.append(
                    meta.number(meta_number)
                )

            if meta_title is not None or meta_number is not None:
                return meta.series_info(*series_info)
            else:
                return None
        finally:
            self.log.exit()
