from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.conference_series.conference_series import ConferenceSeries
from gaia.gift.gift25 import gift_doc, essay, meta, shared, media, vault_link
from lxml import etree
from project.cho.egest_adapter.doc.document_error import DocumentError, SourceDataMissing, AtlasLanguageMissing, PubSegMissing, AtlasIllustrationMissing, LanguageMissing
from project.cho.egest_adapter.entity_reference import EntityReference
from gaia.gift.gift25.hyphen_element_maker import attr
from project.cho.egest_adapter.language_correction import LanguageCorrection


class ArticleConferenceSeries(ConferenceSeries):
    ''' return gift document instances for a ConferenceSeries
        The "article" part.
    '''
    FEED_GROUP = ChoFeedGroup.ARTICLE

    # this was generated from export_csv_into_dict.py
    pub_segs = {
        'front_matter': ('21817803', 'Front matter'),
        'article': ('14242630', 'Article'),
        'back_matter': ('21817804', 'Back matter'),
        'part': ('17528382', 'Part'),
        'chapter': ('17528382', 'Part'),
        'section': ('17528382', 'Part'),
        }

    def __init__(self, config, source_xml_dict, extra_args):
        ConferenceSeries.__init__(self, config, source_xml_dict, extra_args)
        self.language_correction = LanguageCorrection(config)

    def _meta_descriptive_indexing(self, document_instance):
        return self.meta_descriptive_indexing(document_instance, '21819391', 'Journal')

    def pub_seg_dict(self, lookup_key):
        try:
            return self.pub_segs[lookup_key]
        except KeyError:
            return None, None

    def document_instances(self):
        try:
            self.log.enter()
            document_instances = []

            document_instance_count = self.number_of_articles()
            for document_instance in range(1, document_instance_count + 1):

                doc_inst_str = self._gold_document_instances(document_instance)
                doc_inst_str_pretty_printed = EntityReference.unescape(etree.tostring(doc_inst_str, pretty_print=True))

                document_instances.append(doc_inst_str_pretty_printed)

            return document_instances
        finally:
            self.log.exit()

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

    def total_pages_of_article(self, article):
        ''' cumulative count of clips '''

        page_article_is_on, article_count_on_page = self._find_page_article_on(article)
        xpath = '/chapter/page[%s]/article[%s]/clip/@pgref' % (page_article_is_on, article_count_on_page)
        clips_for_article = self.source_xml_dict[xpath]

        if clips_for_article is None:
            raise SourceDataMissing('total_pages_of_article', xpath=xpath)

        if isinstance(clips_for_article, basestring):
            clips_for_article_count = 1
        else:
            clips_for_article_count = len(clips_for_article)

        return str(clips_for_article_count)

    def _meta_range(self, article):
        try:
            self.log.enter(article=article)

            page_article_is_on, article_index_on_page = self._find_page_article_on(article)
            self.log.debug(page_article_is_on=page_article_is_on, article_index_on_page=article_index_on_page)

            first_clip_pgref, last_clip_pgref = self._find_first_and_last_text_clip_pgref(page_article_is_on, article_index_on_page)
            self.log.debug(first_clip_pgref=first_clip_pgref, last_clip_pgref=last_clip_pgref)

            meta_begin_page = self.source_xml_dict['/chapter/page[%s]/sourcePage' % first_clip_pgref]
            meta_end_page = self.source_xml_dict['/chapter/page[%s]/sourcePage' % last_clip_pgref]
            self.log.debug(meta_begin_page=meta_begin_page, meta_end_page=meta_end_page)

            return meta_begin_page, meta_end_page
        finally:
            self.log.exit()

    def _find_first_and_last_text_clip_pgref(self, page, article):
        try:
            self.log.enter(page=page, article=article)
            xpath = '/chapter/page[%s]/article[%s]/clip/@pgref' % (page, article)

            clips = self.source_xml_dict[xpath]

            if clips is None:
                return None, None

            clip_pgrefs = []
            for clip in range(1, len(clips) + 1):
                clip_pgref = self.source_xml_dict['/chapter/page[%s]/article[%s]/clip[%s]/@pgref' % (page, article, clip)]
                if clip_pgref is not None:
                    clip_pgrefs.append(int(clip_pgref))

            if len(clip_pgrefs) == 0:
                return None, None

            if len(clip_pgrefs) == 1:
                return clip_pgrefs[0], None

            if len(clip_pgrefs) > 1:
                return clip_pgrefs[0], clip_pgrefs[len(clip_pgrefs) - 1]
        finally:
            self.log.exit()

        return

    def _find_page_article_on(self, article):
        # self.source_xml_dict doesn't give us any context of where we are in the xml, we need to figure out where we are ourselves
        try:
            self.log.enter()

            page_article_count = 0
            pages = self.number_of_documents()
            for page_article_is_on in range(1, pages + 1):

                articles_on_page = self.source_xml_dict['/chapter/page[%s]/article' % page_article_is_on]

                if articles_on_page is None:
                    continue

                if isinstance(articles_on_page, basestring):
                    articles_on_page_count = 1
                else:
                    articles_on_page_count = len(articles_on_page)

                for article_count_on_page in range(1, articles_on_page_count + 1):
                    page_article_count += 1

                    if page_article_count == article:
                        return page_article_is_on, article_count_on_page
        finally:
            self.log.exit()

    def gift_doc_document_metadata(self, document_instance):
        try:
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

            meta_descriptive_indexing = self.meta_descriptive_indexing(document_instance, '22199438', 'Conference proceedings')
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

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()

    def _product_content_type(self):
        try:
            self.log.enter()

            return meta.product_content_type(
                attr('type', 'CHO'),
                self.product_content_type()
                )
        finally:
            self.log.exit()

    def meta_source_citation_group(self):
        try:
            self.log.enter()

            return meta.source_citation_group(
                meta.source_citation(
                    self.meta_content_date()
                    )
                )
        finally:
            self.log.exit()

    def meta_source_institution(self):
        try:
            self.log.enter()

            name_xpath = '/chapter/metadataInfo/sourceLibrary/libraryName'
            name = self.source_xml_dict[name_xpath]
            location = 'London'
            copyright_statement = self.copyright_statement()

            if name is None or copyright_statement is None:
                return SourceDataMissing('meta_source_institution', name_xpath=name_xpath, copyright_statement=copyright_statement)

            return meta.source_institution(
                name,
                location,
                copyright_statement,
                )
        finally:
            self.log.exit()

    def meta_descriptive_indexing(self, document_instance, doc_info_type_id, doc_into_type_value):
        try:
            self.log.enter(document_instance=document_instance)

            page_article = self.page_article_ids[document_instance - 1]
            page = page_article['page_index']
            article = page_article['article_index']

            type_attr = self.source_xml_dict['/chapter/page[%s]/article[%s]/@type' % (page, article)]
            meta_term_id, meta_term_value = self.pub_seg_dict(type_attr)
            if meta_term_id is None or meta_term_value is None:
                raise PubSegMissing(page=page, article=article, type_attr=type_attr)

            return meta.descriptive_indexing(
                meta.indexing_term(
                    meta.term(
                        'DOC_INFO_TYPE',
                        'Atlas',
                        doc_info_type_id,
                        doc_into_type_value
                        )
                    ),
                meta.indexing_term(
                    meta.term(
                        'DOC_INFO_TYPE',
                        'Atlas',
                        meta_term_id,
                        meta_term_value
                        )
                    ),
                meta.indexing_term(
                    meta.term(
                        'CONT_REC_TYPE',
                        'Atlas',
                        '17234672',
                        'Text'
                        )
                    ),
                meta.indexing_term(
                    meta.term(
                        'CONT_TYPE',
                        'Atlas',
                        '21901547',
                        'DVI-Periodical'
                        )
                    ),
                meta.indexing_term(
                    meta.term(
                        'FUNC_TYPE',
                        'Atlas',
                        '21787856',
                        'Issue-volume article record'
                        )
                    ),
                *self._meta_indexing_term_art_lang(document_instance)
                )
        finally:
            self.log.exit()

    def _meta_indexing_term_art_lang(self, document_instance):
        # handle multiple languages
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            page_article = self.page_article_ids[document_instance - 1]
            article_id = page_article['article_id']

            meta_languages_list = []

            language = self._article_language_correction(psmid, article_id)

            if language == None:  # if not exist in excel, raise exception
                raise LanguageMissing('PSMID "%s" with article id "%s" not in language table' % (psmid, article_id))

            language_value = self.atlas_language[language]
            if language_value is None:
                raise AtlasLanguageMissing(language=language)

            meta_languages_list.append(meta.indexing_term(
                meta.term(
                    'ART_LANG',
                    'Atlas',
                    language_value,
                    language
                    )
                )
            )

            return meta_languages_list
        finally:
            self.log.exit()

    def _meta_authors_byline(self, page, article):
        try:
            self.log.enter()

            byline = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/byline' % (page, article)]
            if byline is not None:
                return meta.corporate_author(byline)
        finally:
            self.log.exit()

    def meta_authors(self, document_instance):
        try:
            self.log.enter()

            page_article = self.page_article_ids[document_instance - 1]
            page = page_article['page_index']
            article = page_article['article_index']

            authors = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author' % (page, article)]
            if authors is None:
                meta_authors_byline = self._meta_authors_byline(page, article)
                if meta_authors_byline is not None:
                    return meta.authors(
                        meta_authors_byline
                        )
                else:
                    return None

            if isinstance(authors, basestring):
                author_count = 1
            else:
                author_count = len(authors)

            authors = []
            for author_index in range(1, author_count + 1):
                role = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/@role' % (page, article, author_index)]

                if role == u'author':
                    prefix = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/prefix' % (page, article, author_index)]
                    first = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/first' % (page, article, author_index)]
                    middle = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/middle' % (page, article, author_index)]
                    last = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/last' % (page, article, author_index)]
                    suffix = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/author[%s]/suffix' % (page, article, author_index)]

                    xpath_aucomposed = '/chapter/page[%s]/article[%s]/articleInfo/author[%s]/aucomposed' % (page, article, author_index)
                    aucomposed = self.source_xml_dict[xpath_aucomposed]

                    if first is None or last is None:
                        args = []

                        sobriquet = aucomposed
                        if sobriquet is not None:
                            args.append(meta.sobriquet(
                                meta.name(sobriquet)
                                )
                            )

                        if aucomposed is None:
                            raise SourceDataMissing('aucomposed', xpath_aucomposed=xpath_aucomposed)
                        args.append(meta.composed_name(aucomposed))

                        authors.append(
                            meta.author(
                                *args
                            )
                        )

                    else:
                        mega_structured_name = meta.structured_name(
                            _prefix=prefix,
                            _first_name=first,
                            _middle_name=middle,
                            _last_name=last,
                            _suffix=suffix
                            )

                        if aucomposed is None:
                            aucomposed = ''
                        meta_composed_name = meta.composed_name(aucomposed)

                        authors.append(
                            meta.author(
                                mega_structured_name,
                                meta_composed_name
                            )
                        )

            if len(authors) > 0:
                corporate_author = self._meta_authors_byline(page, article)
                if corporate_author is not None:
                    authors.append(corporate_author)

                return meta.authors(
                    *authors
                    )
            else:
                return None
        finally:
            self.log.exit()

    def _article_language_correction(self, psmid, article_id):
        cont_type = ""

        if str(self.product_content_type()) == "Special Publications":
            if self.source_xml_dict['/chapter/citation/book'] != None:  # Refugee Survey
                cont_type = "book"
            elif self.source_xml_dict['/chapter/citation/journal'] != None:  # Weekly Review of Foreign Press Journal
                cont_type = "journal"
            language = self.language_correction.get_language(str(self.product_content_type()), psmid, article_sequence=article_id, content_type=cont_type)
        else:
            language = self.language_correction.get_language(str(self.product_content_type()), psmid, article_sequence=article_id, content_type=str(self.content_type()))

        return language

    def meta_languages(self, document_instance):
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            page_article = self.page_article_ids[document_instance - 1]
            article_id = page_article['article_id']

            meta_languages_list = []

            language = self._article_language_correction(psmid, article_id)

            if language == None:  # if not exist in excel, raise exception
                raise LanguageMissing('PSMID "%s" with article id "%s" not in language table' % (psmid, article_id))

            language_value = self.atlas_language[language]
            if language_value is None:
                raise AtlasLanguageMissing(language=language)

            ocr = language

            yes_or_no = 'Y'

            meta_languages_list.append(
                meta.language(
                    attr('term-id', language_value),
                    attr('ocr', ocr),
                    attr('ocr-term-id', language_value),
                    attr('primary', yes_or_no),
                    language
                    )
                )

            return meta.languages(
                *meta_languages_list
                )
        finally:
            self.log.exit()

    def meta_ocr_confidence(self, document_instance):
        try:
            self.log.enter()

            page_article = self.page_article_ids[document_instance - 1]
            page = page_article['page_index']
            article = page_article['article_index']

            xpath = '/chapter/page[%s]/article[%s]/articleInfo/ocr' % (page, article)
            ocr_confidence = self.source_xml_dict[xpath]
            if ocr_confidence is None:
                raise SourceDataMissing('metadataInfo/ocr', xpath=xpath)

            return meta.ocr_confidence(ocr_confidence)
        finally:
            self.log.exit()

    def meta_document_titles(self, document_instance):
        try:
            self.log.enter()

            page_article = self.page_article_ids[document_instance - 1]
            page = page_article['page_index']
            article = page_article['article_index']

            document_titles_list = []

            xpath = '/chapter/page[%s]/article[%s]/articleInfo/title' % (page, article)

            title_display = self.source_xml_dict[xpath]
            if title_display is None or title_display.isspace():
                # consider element empty
                raise SourceDataMissing('articleInfo/title', xpath=xpath)

            if title_display is not None:
                document_titles_list.append(
                    meta.title_display(
                        EntityReference.escape(title_display)
                        )
                    )
                document_titles_list.append(
                    meta.title_sort(
                        self._meta_document_titles_rules(
                            EntityReference.escape(title_display)
                        )
                    )
                )
                document_titles_list.append(
                    meta.title_open_url(
                        self._meta_document_titles_rules(
                            EntityReference.escape(title_display)
                        )
                    )
                )

            subtitle = self.source_xml_dict['/chapter/page[%s]/article[%s]/articleInfo/subtitle' % (page, article)]
            if subtitle is not None:
                document_titles_list.append(
                    meta.subtitle(EntityReference.escape(subtitle))
                )

            return gift_doc.document_titles(*document_titles_list)
        finally:
            self.log.exit()

    def gift_doc_body(self, document_instance):
        try:
            self.log.enter()

            page_article = self.page_article_ids[document_instance - 1]
            page = page_article['page_index']
            article = page_article['article_index']

            elements = []

            # find all clips that relevant to this article
            for page_article_textclip_pgref in self.page_article_textclip_pgrefs:
                page_clip = page_article_textclip_pgref['page_index']
                article_clip = page_article_textclip_pgref['article_index']

                if page == page_clip and article == article_clip:
                    elements.append(self.essay_div_article(document_instance, page_article_textclip_pgref))

            return gift_doc.body(
                essay.div(
                    'Body text',
                    '14214508',
                    'Atlas',
                    elements=elements
                    )
                )
        finally:
            self.log.exit()

    def essay_div_essay_p(self, article, page_article_clip_pgref):
        try:
            self.log.enter()

            page = page_article_clip_pgref['page_index']
            article = page_article_clip_pgref['article_index']
            textclip = page_article_clip_pgref['textclip_index']

            xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/p/word' % (page, article, textclip)
            essay_p = self.essay_p(xpath)

            if essay_p == None:
                return None

            return essay.div(
                'Body text',
                '14214508',
                'Atlas',
                essay_p=essay_p
                )
        finally:
            self.log.exit()

    def essay_div_article(self, document_instance, page_article_textclip_pgref):
        try:
            self.log.enter(document_instance=document_instance, page_article_textclip_pgref=page_article_textclip_pgref)

            term_id = '21902636'
            term_source = 'Atlas'
            category = 'DVI page'
            asset_id_page = self.asset_id(page_article_textclip_pgref['pgref_value'])
            self.log.debug(asset_id_page=asset_id_page)

            vault_link_page_doc = vault_link.vault_link(
                _link_type='external',
                term_id=term_id,
                term_source=term_source,
                _category=category,
                _action='point',
                where_path='//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id_page,
                _target='ancestor::gift-doc:document'
                )

            term_id = '22176901'
            term_source = 'Atlas'
            category = 'DVI volume'
            asset_id_parent = self.asset_id_document()
            self.log.debug(asset_id_parent=asset_id_parent)

            vault_link_parent_doc = vault_link.vault_link(
                _link_type='external',
                term_id=term_id,
                term_source=term_source,
                _category=category,
                _action='point',
                where_path='//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id_parent,
                _target='ancestor::gift-doc:document'
                )

            return essay.div(
                'DVI newspaper article clip',
                '21918445',
                'Atlas',
                complex_meta=self._essay_complex_meta(page_article_textclip_pgref),
                shared_media=self._shared_media(document_instance, page_article_textclip_pgref),
                vault_link0=vault_link_page_doc,
                vault_link1=vault_link_parent_doc,
                vault_link2=self._vault_link_related_docs(page_article_textclip_pgref),
                _ocr=self.essay_div_essay_p(document_instance, page_article_textclip_pgref)
                )
        finally:
            self.log.exit()

    def _essay_complex_meta(self, page_article_clip_pgref):
        try:
            self.log.enter()

            essay_complex_meta_list = []

            xpath = '/chapter/page[%s]/pageImage' % page_article_clip_pgref['pgref_value']
            page_id_number = self.source_xml_dict[xpath]
            if page_id_number.endswith('.jpg'):
                page_id_number = page_id_number[:-4]

            if page_id_number is None or len(page_id_number) < 5:
                raise SourceDataMissing('pageImage', xpath=xpath)
            else:
                page_id_number = page_id_number[-4:len(page_id_number)]
                essay_complex_meta_list.append(
                    meta.page_id_number(str(page_id_number)
                    )
                )

            meta_folio = self.meta_folio(page_article_clip_pgref['pgref_value'])
            if meta_folio is not None:
                essay_complex_meta_list.append(meta_folio
                )

            return essay.complex_meta(*essay_complex_meta_list)
        finally:
            self.log.exit()

    def _shared_media(self, article, page_article_clip_pgref):  # http://jira.cengage.com/browse/CHOA-1013
        try:
            self.log.enter(article=article, page_article_clip_pgref=page_article_clip_pgref)

            args = []

            page_article = self.page_article_ids[article - 1]
            _page = page_article['page_index']
            _article = page_article['article_index']

            xpath = '/chapter/page[%s]/@id' % page_article_clip_pgref['pgref_value']
            page = int(self.source_xml_dict[xpath])
            args.append(self.shared_media_page_image(page))

            if self.page_article_illustration_pgrefs is not None:
                for page_article_illustration_pgref in self.page_article_illustration_pgrefs:

                    # see: test_cho_rfpx_1940C_0000_042_0000 / http://jira.cengage.com/browse/CHOA-1013
                    if page_article_illustration_pgref['index_page'] == page_article_clip_pgref['page_index'] and \
                        page_article_illustration_pgref['index_article'] == page_article_clip_pgref['article_index'] and \
                        int(page_article_illustration_pgref['illustration_pgref']) == page_article_clip_pgref['pgref_value']:
                        args.append(self.shared_media_illustration_image(page_article_illustration_pgref))

#                     illustration_pgref = int(page_article_illustration_pgref['illustration_pgref'])
#                     if page == illustration_pgref:
#                         args.append(self.shared_media_illustration_image(page_article_illustration_pgref))

                return shared.media(*args)
            else:
                return None
        finally:
            self.log.exit()

    def shared_media_illustration_image(self, page_article_illustration_pgref):
        try:
            self.log.enter()

            page_pgref = page_article_illustration_pgref['illustration_pgref']

            height_xpath = '/chapter/page[%s]/pageImage/@height' % page_pgref
            height = self.source_xml_dict[height_xpath]
            if height is None:
                raise SourceDataMissing('@height', height_xpath=height_xpath)

            width_xpath = '/chapter/page[%s]/pageImage/@width' % page_pgref
            width = self.source_xml_dict[width_xpath]
            if width is None:
                raise SourceDataMissing('@width', width_xpath=width_xpath)

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % page_pgref]

            sequence_xpath = '/chapter/page[%s]/pageImage' % page_pgref
            sequence = self.source_xml_dict[sequence_xpath]
            if sequence.endswith('.jpg'):
                sequence = sequence[:-4]

            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('pageImage', sequence_xpath=sequence_xpath)
            else:
                sequence = sequence[-4:len(sequence)]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % page_pgref]  # TODO refactor
            if where.endswith('.jpg'):
                where = where[:-4]

            caption = page_article_illustration_pgref['caption']

            illustration = page_article_illustration_pgref['type']
            if illustration is None:
                raise AtlasIllustrationMissing('illustration/@type', page_article_illustration_pgref=page_article_illustration_pgref)
            else:
                # correct it according to the spec.
                illustration_term_key = illustration.replace('_', ' ')
                illustration_term_key = illustration_term_key[0].capitalize() + illustration_term_key[1:]

            term_id = self.atlas_illustration[illustration_term_key]
            term_value = illustration_term_key
            if term_value is None:
                raise DocumentError('atlas illustration', illustration_term_key=illustration_term_key)

            descriptive_indexing = meta.descriptive_indexing(
                meta.indexing_term(
                    meta.term(
                        'DOC_INFO_TYPE',
                        'Atlas',
                        term_id,
                        term_value
                        )
                    )
                )

            return media.image(
                data_type='jpeg',
                height=height,
                width=width,
                image_type='inline',
                layout='single',
                color_mode='color',
                folio=folio,
                sequence=sequence,
                vault_link=vault_link.vault_link(
                    _link_type='external',
                    _action='point',
                    where_path=where),
                _caption=caption,
                _descriptive_indexing=descriptive_indexing
                )
        finally:
            self.log.exit()

    def meta_document_ids(self, document_instance=None):
        try:
            self.log.enter()

            if document_instance is None:
                return meta.document_ids(
                    _type0='Gale asset',
                    _value0=self.asset_id_document()
                    )
            else:
                asset_id = self.asset_id_page_article(document_instance)
                if asset_id is None:
                    raise DocumentError('No Asset Id', document_instance=document_instance)

                return meta.document_ids(
                    _type0='Gale asset',
                    _value0=asset_id
                    )
        finally:
            self.log.exit()
