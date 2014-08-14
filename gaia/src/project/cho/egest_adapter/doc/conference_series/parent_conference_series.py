from lxml import etree
from gaia.gift.gift25 import gold, gift_doc, meta, essay, etoc, vault_link, shared, media
from project.cho.egest_adapter.doc.document_error import SourceDataMissing, AtlasLanguageMissing, DocumentError, LanguageMissing
from project.cho.egest_adapter.doc.conference_series.conference_series import ConferenceSeries
from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.entity_reference import EntityReference


class ParentConferenceSeries(ConferenceSeries):
    ''' return gift document instances for a ConferenceSeries
        The "issue" part.
    '''
    FEED_GROUP = ChoFeedGroup.ISSUE

    def __init__(self, config, source_xml_dict, extra_args):
        ConferenceSeries.__init__(self, config, source_xml_dict, extra_args)

    def document_instances(self):
        try:
            self.log.enter()

            args = []
            meta_volume_number = self.meta_volume_number()
            if meta_volume_number is not None:
                args.append(meta_volume_number)

            gift_doc_pagination_group = self.gift_doc_pagination_group()
            if gift_doc_pagination_group is not None:
                args.append(gift_doc_pagination_group)

            document_instance = gold.document_instance(
                gift_doc.document(
                    gift_doc.metadata(
                        gift_doc.node_metadata(
                            *args
                        ),
                        self.gift_doc_document_metadata()
                    ),
                gift_doc.body(
                        essay.div_container(
                            'Body text',
                            '14214508',
                            'Atlas',
                            self.essay_container_divs()
                        ),
                        self.etoc_document()
                    )
                )
            )
            # TODO: might need this?...etree.tostring(root, encoding='UTF-8') (and treat therafter as a byte-stream not as a character string.
            return [EntityReference.unescape(etree.tostring(document_instance, pretty_print=True))]
        finally:
            self.log.exit()

    def etoc_document(self):
        try:
            self.log.enter()

            etoc_page_levels = self._etoc_page_levels()  # collect all useful data related to levels

            # the first level MUST be 1
            first_etoc_page_level = int(etoc_page_levels[0]['level'])
            if first_etoc_page_level != 1:
                raise DocumentError('etoc level must start at 1 not', first_etoc_page_level=first_etoc_page_level)

            etoc_document = etoc.document(
                self._make_etoc_levels(etoc_page_levels)
                )

            etoc_document_with_sequential_unique_id_chunk = self._make_asset_id_chunk_sequential(etoc_document)

            etoc_document_with_sequential_unique_id = self._make_unique_ids_sequential(etoc_document_with_sequential_unique_id_chunk)

            return etoc_document_with_sequential_unique_id
        finally:
            self.log.exit()

    def _make_etoc_levels(self, etoc_page_levels):  # TODO ideally replace this 'design' with Tushar's ordered tree implementation
        # go through all the levels and create a correctly indented etoc:links-chunk 'tree'
        try:
            self.log.enter()
            etoc_page_levels.append({'article': 0, 'page': 0, 'level': 0})  # add a 'final' marker dict into the list

            parent_count = 0  # we keep track of how many children we have, so that we can close the correct # of tags
            etoc_xml = '<etoc:links-chunk xmlns:etoc="http://www.gale.com/goldschema/etoc">'

            for etoc_index in range(0, len(etoc_page_levels) - 1):  # see: http://wiki.cengage.com/display/EDT/etoc+layout
                etoc_level_current = int(etoc_page_levels[etoc_index]['level'])
                etoc_level_next = int(etoc_page_levels[1 + etoc_index]['level'])

                etoc_movement_score = etoc_level_next - etoc_level_current  # levels can be 'scored' to help us figure out indentation & apply rules

                # etoc 1 can only move to 2, it can't jump to, say, 3; etoc indention must be sequential
                if etoc_movement_score > 1:
                    raise DocumentError('etoc level must be sequential', etoc_level_current=etoc_level_current, etoc_level_next=etoc_level_next)

                etoc_xml_inner = self._etoc_xml_inner(etoc_page_levels[etoc_index])

                if etoc_movement_score == 0:  # node with no child, a 'leaf'
                    etoc_xml += '<etoc:etoc-link>'
                    etoc_xml += etoc_xml_inner
                    etoc_xml += '</etoc:etoc-link>'

                if etoc_movement_score == 1:  # move to rhs: node with child
                    parent_count += 1
                    etoc_xml += '<etoc:etoc-link>'
                    etoc_xml += etoc_xml_inner
                    etoc_xml += '<etoc:links-chunk>'

                if etoc_movement_score < 0:  # 'leaf' + close associated parents
                    xml_close_tags = ''
                    for i in range(0, etoc_movement_score, -1):
                        if parent_count == 0:
                            break
                        parent_count = parent_count -1
                        xml_close_tags += '</etoc:links-chunk></etoc:etoc-link>'

                    etoc_xml += '<etoc:etoc-link>'
                    etoc_xml += etoc_xml_inner
                    etoc_xml += '</etoc:etoc-link>'
                    etoc_xml += xml_close_tags

            etoc_xml += '</etoc:links-chunk>'

            return etree.fromstring(etoc_xml)
        finally:
            self.log.exit()

    def _etoc_xml_inner(self, etoc_page_level):
        try:
            self.log.enter()

            meta_document_ids, vault_link, meta_title_display, unique_id = self._etoc_link_values(etoc_page_level)
            etoc_xml_inner = etree.tostring(meta_document_ids)
            etoc_xml_inner += etree.tostring(vault_link)
            etoc_xml_inner += etree.tostring(meta_title_display)
            etoc_xml_inner += etree.tostring(etoc.etoc_unique_id(unique_id))
            return etoc_xml_inner
        finally:
            self.log.exit()

    def _make_unique_ids_sequential(self, etoc_document):
        try:
            self.log.enter()

            # the etoc-unique-id has to be in sequential order in the document-instance!
            etoc_document_string = etree.tostring(etoc_document)

            for i in range(0, len(self._extra_args_asset_id_chunks())):
                unique_id = '%06d' % int(1 + i)
                self.log.debug('replacing first UNIQUE_ID with %s' % unique_id)
                etoc_document_string = etoc_document_string.replace('UNIQUE_ID', unique_id, 1)

            return etree.fromstring(etoc_document_string)
        finally:
            self.log.exit()

    def _extra_args_asset_id_chunks(self):  # refactored into a single method to aid testing
        return self.extra_args['asset_id']['chunks']

    def _make_asset_id_chunk_sequential(self, etoc_document):
        try:
            self.log.enter()

            etoc_document_string = etree.tostring(etoc_document)
            sorted_asset_id_chunks = sorted(self._extra_args_asset_id_chunks().iterkeys())

            for key in sorted_asset_id_chunks:
                value = self._extra_args_asset_id_chunks()[key]
                self.log.debug('replacing first ASSET_ID_CHUNK with %s' % value)
                etoc_document_string = etoc_document_string.replace('ASSET_ID_CHUNK', value, 1)

            return etree.fromstring(etoc_document_string)
        finally:
            self.log.exit()

    def _etoc_link_values(self, page_level_toc):
        try:
            self.log.enter()

            meta_document_ids = meta.document_ids(
                _type0='Gale asset',
                _value0='ASSET_ID_CHUNK'  # we sequentualise these at the end of document construction
            )

            where_path = self.source_xml_dict['/chapter/page[%s]/pageImage' % page_level_toc['page']]
            if where_path.endswith('.jpg'):
                where_path = where_path[:-4]

            display_point_value_xpath = '/chapter/page[%s]/pageImage' % page_level_toc['page']
            display_point_value = self.source_xml_dict[display_point_value_xpath]
            if display_point_value.endswith('.jpg'):
                display_point_value = display_point_value[:-4]

            if display_point_value is None or len(display_point_value) < 5: 
                raise SourceDataMissing('pageImage', display_point_value_xpath=display_point_value_xpath)
            else:
                display_point = 'media:image[@sequence="%s"]' % display_point_value[-4:len(display_point_value)]

            display_link_xpath = '/chapter/page[%s]/article[%s]/articleInfo/title' % (page_level_toc['page'], page_level_toc['article'])
            display_link = self.source_xml_dict[display_link_xpath]
            if display_link is None or display_link.isspace():
                raise SourceDataMissing('articleInfo/title', display_link_xpath=display_link_xpath)

            display_link = EntityReference.escape(display_link)

            _vault_link = vault_link.vault_link(
                        _link_type='external',
                        _data_type='image/jpeg',
                        _action='point',
                        where_path=where_path,
                        _target='ancestor::gift-doc:document',
                        _display_point=display_point,
                        _display_link=display_link
                    )

            meta_title_display = meta.title_display(display_link)

            return meta_document_ids, _vault_link, meta_title_display, 'UNIQUE_ID'  # we sequentualise these at the end of document construction
        finally:
            self.log.exit()

    def _etoc_page_levels(self):
        '''
        Figure out which pages and articles, etoc levels belong to, by producing an intermeidate structure - i.e.

        list: [
            {'article': 1, 'page': u'1', 'level': u'1'},
            {'article': 1, 'page': u'3', 'level': u'1'},
            {'article': 1, 'page': u'6', 'level': u'2'},
            {'article': 1, 'page': u'8', 'level': u'3'},
            {'article': 2, 'page': u'8', 'level': u'1'}
            ]
        '''
        try:
            self.log.enter()

            etoc_sequence = []

            # go through each page - we have to do this as some of the etoc data is based on relative page, that proceeds etoc element!
            pages = self.number_of_documents()

            for page in range(1, pages + 1):
                # find all articles on a page
                articles = self.source_xml_dict['/chapter/page[%s]/article' % page]
                if articles is None:
                    continue

                if isinstance(articles, basestring):
                    articles_count = 1
                else:
                    articles_count = len(articles)

                # find levels for each article
                for article in range(1, articles_count + 1):
                    xpath = '/chapter/page[%s]/article[%s]/@level' % (page, article)
                    level = self.source_xml_dict[xpath]

                    if level is None:
                        continue

                    if isinstance(level, basestring):
                        levels_in_page = [level]
                    else:
                        levels_in_page = level

                    for level in levels_in_page:

                        # source cho xsd only supports levels upto 5
                        if level not in [u'1', u'2', u'3', u'4', u'5']:
                            raise DocumentError('etoc level must be within range 1..5', level=level)

                        etoc_sequence.append({'page': unicode(page), 'article' : article, 'level': level })

            self.log.debug(etoc_sequence)

            return etoc_sequence
        finally:
            self.log.exit()

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

            meta_editors = self.meta_editors()
            if meta_editors is not None:
                gift_doc_document_metadata_list.append(meta_editors)

            meta_descriptive_indexing = self.meta_descriptive_indexing()
            if meta_descriptive_indexing is not None:
                gift_doc_document_metadata_list.append(meta_descriptive_indexing)

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()

    def meta_descriptive_indexing(self):
        try:
            self.log.enter()

            meta_indexing_term_art_langs = []

            meta_indexing_term_art_langs.append(
                    meta.indexing_term(
                    meta.term(
                        'CONT_TYPE',
                        'Atlas',
                        '21901547',
                        'DVI-Periodical'
                        )
                    )
                )

            meta_indexing_term_art_langs.append(
                meta.indexing_term(
                    meta.term(
                        'FUNC_TYPE',
                        'Atlas',
                        '21787859',
                        'Issue-volume record'
                        )
                    )
                )

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']

            languages = self._language_correction(psmid)

            if languages == []:  # if not exist in excel, raise exception
                raise LanguageMissing('PSMID "%s" not in language table' % psmid)

            for language in languages:
                language_value = self.atlas_language[language]
                if language_value is None:
                    raise AtlasLanguageMissing(language=language)

                meta_indexing_term_art_langs.append(
                    meta.indexing_term(
                        meta.term(
                            'ART_LANG',
                            'Atlas',
                            language_value,
                            language
                        )
                    )
            )

            return meta.descriptive_indexing(
                *meta_indexing_term_art_langs
                )
        finally:
            self.log.exit()

    def meta_publication_title(self):
        try:
            self.log.enter()

            publication_title_xpath = '/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()
            publication_title = self.source_xml_dict[publication_title_xpath]

            if publication_title is not None:
                return meta.publication_title(publication_title)
            else:
                raise SourceDataMissing('titleGroup/fullTitle', publication_title_xpath=publication_title_xpath)
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
        # we're not interested in articles / text clips, just pages :-)
        try:
            self.log.enter()
            contents_list = []

            complex_meta_list = []

            page_id_number_xpath = '/chapter/page[%s]/@id' % page
            page_id_number = self.source_xml_dict[page_id_number_xpath]

            if page_id_number is None:
                raise SourceDataMissing('page/@id', page_id_number_xpath=page_id_number_xpath)
            else:
                page_id_number = '%04d' % int(page_id_number)
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

            sequence_xpath = '/chapter/page[%s]/pageImage' % page
            sequence = self.source_xml_dict[sequence_xpath]
            if sequence.endswith('.jpg'):
                sequence = sequence[:-4]

            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('articlePage sequence', sequence_xpath=sequence_xpath)
            else:
                sequence = sequence[-4:len(sequence)]

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
                    )
                )
            )

            asset_id = self.asset_id(page)
            where = '//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id
            self.log.debug(asset_id=asset_id)

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
                *contents_list
                )
        finally:
            self.log.exit()
