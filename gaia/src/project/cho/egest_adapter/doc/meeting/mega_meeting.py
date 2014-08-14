from gaia.gift.gift25 import gold, gift_doc, meta, vault_link, shared, media, essay
from gaia.gift.gift25.hyphen_element_maker import attr
from project.cho.egest_adapter.doc.document_error import SourceDataMissing, AtlasLanguageMissing
from project.cho.egest_adapter.doc.meeting.meeting import Meeting
from project.cho.egest_adapter.entity_reference import EntityReference
from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from lxml import etree 


# TODO get rid of _list variables
class MegaMeeting(Meeting):
    ''' return gift document instances for a Meeting
        The "mega" parts, ie issue and article bits
    '''
    FEED_GROUP = ChoFeedGroup.MEETING_MEGA

    def __init__(self, config, source_xml_dict, extra_args):
        Meeting.__init__(self, config, source_xml_dict, extra_args)

    def document_instances(self):
        try:
            self.log.enter()
            document_instance = gold.document_instance(
                gift_doc.document(
                    gift_doc.metadata(
                        gift_doc.node_metadata(
                            meta.descriptive_indexing(
                                meta.indexing_term(
                                    meta.term(
                                        _type='PUB_SEG_TYPE',
                                        source='Atlas',
                                        _id='14242630',
                                        value=self.publication_segment_type()
                                        )
                                    )
                                ),
                            gift_doc.pagination_group(
                                gift_doc.pagination(
                                    meta.total_pages(self.total_pages())
                                    )
                                )
                            ),
                            self.gift_doc_document_metadata()
                        ),
                    gift_doc.body(
                        essay.div_container(
                            'Body text',
                            '14214508',
                            'Atlas',
                            self.essay_container_divs()
                            )
                        )
                    )
                )
            # TODO: might need this?...etree.tostring(root, encoding='UTF-8') (and treat therafter as a byte-stream not as a character string.
            return [ EntityReference.unescape(etree.tostring(document_instance, pretty_print=True)) ]
        finally:
            self.log.exit()

    def gift_doc_document_metadata(self):
        try:
            self.log.enter()
            gift_doc_document_metadata_list = []

            meta_document_ids = self.meta_document_ids()
            if meta_document_ids is not None:
                gift_doc_document_metadata_list.append(meta_document_ids)

            meta_bibliographic_ids = self.meta_bibliographic_ids_psmid()
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

            shared_media = self.shared_media()
            if shared_media is not None:
                gift_doc_document_metadata_list.append(shared_media)

            meta_product_content_type = self.meta_product_content_type()
            if meta_product_content_type is not None:
                gift_doc_document_metadata_list.append(meta_product_content_type)

            meta_content_filter = self.meta_content_filter()
            if meta_content_filter is not None:
                gift_doc_document_metadata_list.append(meta_content_filter)

            return gift_doc.document_metadata(*gift_doc_document_metadata_list)
        finally:
            self.log.exit()

    def meta_product_content_type(self):
        try:
            self.log.enter()
            product_content_type = 'Meetings and Speeches'

            return meta.product_content_type(
                attr('type', 'CHO'),
                product_content_type
                )
        finally:
            self.log.exit()

    def meta_content_filter(self):
        try:
            self.log.enter()
            return meta.content_filter(
                attr('type', 'CHO rule'),
                'No'
                )
        finally:
            self.log.exit()

    def meta_publication_title(self):
        return meta.publication_title(
            'Chatham House Meetings and Speeches'
            )

    def meta_descriptive_indexing(self):
        try:
            self.log.enter()
            product_content_type = self.product_content_type()

            doc_info_term_id = ''
            if product_content_type == 'Meetings':
                doc_info_term_id = '17525832'
                doc_info_term_value = 'Meeting transcript'

            if product_content_type == 'Pamphlets and Reports':
                doc_info_term_id = '14174382'
                doc_info_term_value = 'Report'

            languages_xpath = '/chapter/metadataInfo/language'

            # CHOA-1064
            languages = self._language_correction(self.psmid())

            if languages is None:
                raise SourceDataMissing('metadataInfo/languages', languages_xpath=languages_xpath)

            if isinstance(languages, basestring):
                language_count = 1
                languages = [languages]
            else:
                language_count = len(languages)

            meta_languages_list = []
            for lang in range(1, language_count + 1):

                language = languages[lang -1]

                language_value = self.atlas_language[language]
                if language_value is None:
                    raise AtlasLanguageMissing(language=language)

                meta_languages_list.append(
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
                meta.indexing_term(
                    meta.term(
                        'DOC_INFO_TYPE',
                        'Atlas',
                        doc_info_term_id,
                        doc_info_term_value
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
                        '21901545',
                        'DVI-Monograph'
                        )
                    ),
                meta.indexing_term(
                    meta.term(
                        'FUNC_TYPE',
                        'Atlas',
                        '14214546',
                        'Megametadocument'
                        )
                    ),
                *meta_languages_list
                )
        finally:
            self.log.exit()

    def meta_source_institution(self):
        return meta.source_institution(
            'Chatham House',
            'London',
            'COPYRIGHT Royal Institute of International Affairs',
            )

    def meta_source_citation_group(self):
        try:
            self.log.enter()

            meeting_number_xpath = '/chapter/citation/%s/meetingGroup/meetingNumber' % self.content_type()
            meeting_number = self.source_xml_dict[meeting_number_xpath]
            if meeting_number is None:
                raise SourceDataMissing('meetingNumber', meeting_number_xpath=meeting_number_xpath)

            reference_number_display = "RIIA/%s" % meeting_number

            return meta.source_citation_group(
                meta.source_citation(
                    attr('type', 'speech'),
                    self.meta_publication_date(),
                    meta.reference_number(
                        meta.reference_number_display(reference_number_display)
                    ),
                    meta.geo_location('Chatham House, London'),
                    meta.organization('Chatham House'),
                    self.meta_content_date()
                    )
                )
        finally:
            self.log.exit()

    def shared_media(self):
        try:
            self.log.enter()

            product_content_type = self.product_content_type()
            media_type = self.source_xml_dict['/chapter/metadataInfo/relatedMedia/@mediaType']
            if product_content_type == 'Meetings' and media_type == 'Audio':

                where_xpath = '/chapter/metadataInfo/relatedMedia/@id'
                where = self.source_xml_dict[where_xpath]
                if where is None:
                    raise SourceDataMissing('relatedMedia/@id', where_xpath=where_xpath)

                data_type_xpath = '/chapter/metadataInfo/relatedMedia/@dataType'
                data_type = self.source_xml_dict[data_type_xpath]
                if data_type is None:
                    raise SourceDataMissing('relatedMedia/@data_type', data_type_xpath=data_type_xpath)

                media_title_xpath = '/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()
                media_title = self.source_xml_dict[media_title_xpath]
                if media_title is None:
                    raise SourceDataMissing('fullTitle', media_title_xpath=media_title_xpath)

                shared_media = shared.media(
                    media.audio(
                         self.file_size(where, data_type),
                        'mp3',
                        'inline',
                        meta.descriptive_indexing(
                            meta.indexing_term(
                                meta.term(
                                    'DOC_INFO_TYPE',
                                    'Atlas',
                                    '198465964',
                                    'Audio file'
                                    )
                                )
                            ),
                        vault_link.vault_link(
                            _link_type='external',
                            _data_type='mp3',
                            _action='point',
                            where_path=where
                            ),
                        media_title
                        )
                    )
                return shared_media
            else:
                return None
        finally:
            self.log.exit()

    def essay_p(self, page, article, text_clip):  # TODO try and refactor similar functionality in 'conference series'
        try:
            self.log.enter()

            # get a list of all words in a textclip
            xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/p/word' % (page, article, text_clip)
            self.log.debug('xpath = %s' % xpath)

            text_clip_words = self.source_xml_dict[xpath]
            if text_clip_words is None:
                return None

            if isinstance(text_clip_words, basestring):
                text_clip_words_count = 1
            else:
                text_clip_words_count = len(text_clip_words)

            word_count = 0
            full_text = ''
            for text_clip_word in range(1, text_clip_words_count + 1):
                xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/p/word[%s]/@pos' % (page, article, text_clip, text_clip_word)
                #self.log.debug('xpath = %s' % xpath)

                if self.source_xml_dict[xpath] != '0,0,0,0':
                    xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/p/word[%s]' % (page, article, text_clip, text_clip_word)
                    #self.log.debug('xpath = %s' % xpath)

                    word = self.source_xml_dict[xpath]
                    if word is not None:
                        word_count += 1
                        if word_count < text_clip_words_count + 1:
                            word += ' '  # http://www.w3.org/TR/REC-xml/#sec-white-space

                            full_text += EntityReference.escape(word)

            full_text = full_text.rstrip()
            #self.log.debug('full_text = %s' % full_text)

            return essay.p(full_text)
        finally:
            self.log.exit()

    def number_of_documents(self):
        return 1

    def page_range(self, page_number):
        return self.source_xml_dict['/chapter/page[%s]/article/articleInfo/pageRange' % page_number]

    def _related_doc_display_link(self, display_link, doc_ref=None):
        if doc_ref is not None:
            if doc_ref.startswith('cho_iaxx'):
                display_link_value = EntityReference.escape("Link to published version in '_zQz_LT_KP_QzQ_pres:italics_zQz_GT_KP_QzQ_International Affairs_zQz_LT_KP_QzQ_/pres:italics_zQz_GT_KP_QzQ_'")
            else:
                display_link_value = EntityReference.escape("Link to published version in '_zQz_LT_KP_QzQ_pres:italics_zQz_GT_KP_QzQ_The World Today_zQz_LT_KP_QzQ_/pres:italics_zQz_GT_KP_QzQ_'")

            return display_link_value
        else:
            return display_link
