from gaia.gift.gift25 import gift_doc, essay, meta, shared, media, vault_link
from project.cho.egest_adapter.doc.document_error import DocumentError, SourceDataMissing
from project.cho.egest_adapter.doc.meeting.meeting import Meeting
from project.cho.egest_adapter.entity_reference import EntityReference
from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup


# TODO get rid of _list variables
class PageMeeting(Meeting):
    FEED_GROUP = ChoFeedGroup.MEETING_PAGE

    def __init__(self,  config, source_xml_dict, extra_args):
        Meeting.__init__(self, config, source_xml_dict, extra_args)

    def gift_doc_document_metadata(self, document_instance):
        try:
            self.log.enter()
            gift_doc_document_metadata_list = []

            meta_document_ids = self.meta_document_ids(document_instance)
            if meta_document_ids is not None:
                gift_doc_document_metadata_list.append(meta_document_ids)

            meta_bibliographic_ids = self.meta_bibliographic_ids_psmid_isbn_issn()
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

    def meta_record_admin_info(self):
        try:
            self.log.enter()
            return meta.record_admin_info( 
                self.creation_type(),
                self.creation_date()
                )
        finally:
            self.log.exit()

    def meta_publication_title(self):
        try:
            self.log.enter()
            title = None

            if self.product_content_type() == 'Meetings':
                title = 'Chatham House Meetings and Speeches'

            if self.product_content_type() == 'Pamphlets and Reports':
                title = 'Chatham House Reports and Pamphlets'

            if title is None:
                raise SourceDataMissing('meta-publication-title')

            return meta.publication_title(
                title
                )
        finally:
            self.log.exit()

    def meta_descriptive_indexing(self):
        try:
            self.log.enter()
            return meta.descriptive_indexing(
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
                        '14214549',
                        'Page view'
                        )
                    )
                )
        finally:
            self.log.exit()

    def gift_doc_body(self, document_instance):
        try:
            self.log.enter()

            args = []
            essay_div_page = self.essay_div_page(document_instance)
            essay_div_body = self.essay_div_body(essay_div_page)
            args.append(essay_div_body)

            # possible that HTC scanner can't scan a page - so no ocr words on it
            ocr = self.essay_div_ocr(document_instance)
            if ocr is not None:
                args.append(ocr)

            return gift_doc.body(
                *args
                )
        finally:
            self.log.exit()

    def essay_div_page(self, document_instance):
        try:
            self.log.enter()
            return essay.div(
                'Page',
                '21922233',
                'Atlas',
                complex_meta=self.essay_complex_meta(document_instance),
                essay_p=self.essay_p(document_instance),
                shared_media=self.shared_media(document_instance),
                vault_link0=self.vault_link0(),  # TODO rename vault_link0 to something else - i.e. vault_link_document

                # TODO relatedDocument is unable to be produced at present - this is because we don't have an asset id available for this documentInstance
                #vault_link1=self.vault_link1(document_instance)
                )
        finally:
            self.log.exit()

    def vault_link0(self):
        try:
            self.log.enter()

            asset_id = self.asset_id_document()
            if asset_id is None:
                raise DocumentError('No Asset Id')
            where_path = '//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id

            return vault_link.vault_link(
                _link_type='external',
                term_id='21902593',
                term_source='Atlas',
                _category='DVI megametadocument',
                _data_type='text/xml',
                _action='point',
                where_path=where_path,
                _target='ancestor::gift-doc:document'
                )
        finally:
            self.log.exit()

    def vault_link1(self, document_instance):
        try:
            self.log.enter()

            type_xpath = '/chapter/page/article/text/textclip[%s]/relatedDocument/@type' % document_instance
            type = self.source_xml_dict[type_xpath]
            if type is None:
                return None

            if type not in ['footnote', 'article']:
                raise SourceDataMissing('relatedDocument/@type', type_xpath=type_xpath)

            if type == 'footnote':
                category_term_id = '19131191'
                category='Footnote'
            else:
                category_term_id = '19009864'
                category='Related document'

            asset_id = self.asset_id(document_instance)
            if asset_id is None:
                raise DocumentError('No Asset Id', document_instance=document_instance)
            where_path = '//gift-doc:document-metadata/meta:document-ids/meta:is[@type="Gale asset"]/meta:value[.="%s"]' % asset_id

            display_point_value_xapth = '/chapter/page[%s]/@id' % document_instance
            display_point_value = self.source_xml_dict[display_point_value_xapth]
            if display_point_value is None:
                raise SourceDataMissing('@id', display_point_value_xapth=display_point_value_xapth)
            display_point = '/gift-doc:document/gift-doc:body/essay:div/essay:div/essay:complex-meta/meta:page-id-number="value"%s"' % display_point_value

            display_link_xpath = '/chapter/page/article/text/textclip[%s]/relatedDocument/@docref' % document_instance
            display_link = self.source_xml_dict[display_link_xpath]
            if display_link is None:
                raise SourceDataMissing('@docref', display_link_xpath=display_link_xpath)

            display_link_startswith = display_link[:8]
            if display_link_startswith not in ['cho_iaxx', 'cho_wtxx']:
                raise SourceDataMissing('@docref startswith', display_link_startswith=display_link_startswith)

            # TODO create a proper element for this <pres:italics>
            if display_link.startswith('cho_iaxx'):  # TODO resolve with Tushar how best to handle entity references
                display_link_value = EntityReference.escape('Link to published version in _zQz_LT_KP_QzQ_pres:italics_zQz_GT_KP_QzQ_International Affairs_zQz_LT_KP_QzQ_/pres:italics_zQz_GT_KP_QzQ_')
            else:
                display_link_value = EntityReference.escape('Link to published version in _zQz_LT_KP_QzQ_pres:italics_zQz_GT_KP_QzQ_The World Today_zQz_LT_KP_QzQ_/pres:italics_zQz_GT_KP_QzQ_')

            return vault_link.vault_link(
                _link_type='external',
                term_id=category_term_id,
                term_source='Atlas',
                _category=category,
                _data_type='text/xml',
                _action='point',
                where_path=where_path,
                _target='ancestor::gift-doc:document',
                _display_point=display_point,
                _display_link=display_link_value
                )
        finally:
            self.log.exit()

    def essay_div_ocr(self, document_instance):
        try:
            self.log.enter()
            ocr_word_list = []

            ocr_words = self.source_xml_dict['/chapter/page/article/text/textclip[%s]/p/word' % document_instance]
            if ocr_words is None:
                self.log.debug("missing: ", ocr_words=ocr_words)
                return None

            if isinstance(ocr_words, basestring):
                ocr_words_count = 1
            else:
                ocr_words_count = len(ocr_words)

            for ocr_word in range(1, ocr_words_count + 1):
                position = self.source_xml_dict['/chapter/page/article/text/textclip[%s]/p/word[%s]/@pos' % (document_instance, ocr_word)]
                word = self.source_xml_dict['/chapter/page/article/text/textclip[%s]/p/word[%s]' % (document_instance, ocr_word)]
                if word is not None:
                    word = EntityReference.escape(word)
                    ocr_word_list.append(
                        essay.ocr_text(
                            unicode(position), 
                            word
                            )
                        )

            return essay.div(
                'OCR text',
                '21905043',
                'Atlas',
                _ocr= essay.p(
                    *ocr_word_list
                    )
            )
        finally:
            self.log.exit()

    def shared_media(self, document_instance):
        try:
            self.log.enter()

            height_xpath = '/chapter/page[%s]/pageImage/@height' % document_instance
            height = self.source_xml_dict[height_xpath]
            if height is None:
                raise SourceDataMissing('@height', height_xpath=height_xpath)

            width_xpath = '/chapter/page[%s]/pageImage/@width' % document_instance
            width = self.source_xml_dict[width_xpath]
            if width is None:
                raise SourceDataMissing('@width', width_xpath=width_xpath)

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % document_instance]

            sequence_xpath = '/chapter/page[%s]/pageImage' % document_instance
            sequence = self.source_xml_dict[sequence_xpath]
            if sequence.endswith('.jpg'):
                sequence = sequence[:-4]

            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('pageImage', sequence_xpath=sequence_xpath)
            else:
                sequence = sequence[-4:len(sequence)]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % document_instance]
            if where.endswith('.jpg'):
                where = where[:-4]

            return shared.media(
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
        finally:
            self.log.exit()

    def essay_p(self, document_instance):  # TODO possible refactor of similar code in 'Conference Series'?
        try:
            self.log.enter()

            xpath = '/chapter/page/article/text/textclip[%s]/p/word' % document_instance
            self.log.debug('xpath = %s' % xpath)

            words =  self.source_xml_dict[xpath]
            if words is None:
                self.log.debug("missing: ", words=xpath)
                return None

            if isinstance(words, basestring):
                text_clip_words_count = 1
            else:
                text_clip_words_count = len(words)

            word_count = 0
            full_text = ''
            for word in range(1, text_clip_words_count + 1):
                xpath = '/chapter/page/article/text/textclip[%s]/p/word[%s]/@pos' % (document_instance, word)
                #self.log.debug('xpath = %s' % xpath)

                if self.source_xml_dict[xpath] != '0,0,0,0':
                    xpath = '/chapter/page/article/text/textclip[%s]/p/word[%s]' % (document_instance, word)
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

    def publication_segment_type(self):
        try:
            self.log.enter()

            xpath = '/chapter/page/article/@type'
            value = self.source_xml_dict[xpath]
            if value == 'article':
                return 'Article'
            else:
                raise SourceDataMissing('@type', xpath=xpath)
        finally:
            self.log.exit()
