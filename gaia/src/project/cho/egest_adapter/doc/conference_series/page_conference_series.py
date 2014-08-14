from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.doc.conference_series.conference_series import ConferenceSeries
from gaia.gift.gift25 import gift_doc, meta, essay, vault_link, shared
from project.cho.egest_adapter.doc.document_error import SourceDataMissing
from project.cho.egest_adapter.entity_reference import EntityReference


class PageConferenceSeries(ConferenceSeries):
    ''' return gift document instances for a ConferenceSeries
        The "page" part.
    '''
    FEED_GROUP = ChoFeedGroup.PAGE

    def __init__(self, config, source_xml_dict, extra_args):
        ConferenceSeries.__init__(self, config, source_xml_dict, extra_args)

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

    def meta_descriptive_indexing(self):
        try:
            self.log.enter()
            return meta.descriptive_indexing(
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
                        '21787857',
                        'Issue-volume page record'
                        )
                    )
                )
        finally:
            self.log.exit()

    def gift_doc_body(self, document_instance):
        try:
            self.log.enter()

            essay_div_page = self.essay_div_page(document_instance)
            essay_div_body = self.essay_div_body(essay_div_page)

            return gift_doc.body(
                essay_div_body
                )
        finally:
            self.log.exit()

    def essay_div_page(self, document_instance):
        try:
            self.log.enter(document_instance=document_instance)

            return essay.div(
                'Page',
                '21922233',
                'Atlas',
                complex_meta=self.essay_complex_meta(document_instance),
                elements=self.essay_div_articles(document_instance)
                )
        finally:
            self.log.exit()

    def essay_div_articles(self, document_instance):
        try:
            self.log.enter(document_instance=document_instance)

            articles_with_textclip_on_page = []
            for page_article_textclip_pgref in self.page_article_textclip_pgrefs:
                pgref_value = page_article_textclip_pgref['pgref_value']

                if document_instance == int(pgref_value):
                    articles_with_textclip_on_page.append(page_article_textclip_pgref)

            return self.essay_div_article(document_instance, articles_with_textclip_on_page)
        finally:
            self.log.exit()

    def essay_div_article(self, document_instance, articles_with_textclip_on_page):
        try:
            self.log.enter(document_instance=document_instance, articles_with_textclip_on_page=articles_with_textclip_on_page)

            article_divs = []
            for article_with_textclip_on_page in articles_with_textclip_on_page:
                page_index = article_with_textclip_on_page['page_index']
                article_index = article_with_textclip_on_page['article_index']
                textclip_index = article_with_textclip_on_page['textclip_index']

                words_xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/p/word' % (page_index, article_index, textclip_index)

                divs = []

                words = self.essay_p(words_xpath)
                if words is not None:
                    divs.append(
                        self.essay_div_body(words)
                        )

                ocr = self.essay_div_ocr(words_xpath)
                if ocr is not None:
                    divs.append(ocr)

                shared_media = shared.media(
                    self.shared_media_page_image(document_instance)
                    )

                article_divs.append(
                    essay.div(
                        'DVI article',
                        '21918442',
                        'Atlas',
                        shared_media=shared_media,
                        vault_link0=self.vault_link0(document_instance, article_with_textclip_on_page),  # TODO rename vault_link0 to something better
                        elements=divs
                        )
                    )

            return article_divs
        finally:
            self.log.exit()

    def essay_div_ocr(self, words_xpath):
        try:
            self.log.enter(words_xpath=words_xpath)

            words = self.source_xml_dict[words_xpath]
            if words is None:
                return None

            if isinstance(words, basestring):
                text_clip_words_count = 1
            else:
                text_clip_words_count = len(words)

            ocr_word_list = []
            for word in range(1, text_clip_words_count + 1):
                position = self.source_xml_dict['%s[%s]/@pos' % (words_xpath, word)]
                #self.log.debug('position = %s' % position)

                if position != '0,0,0,0':
                    xpath = '%s[%s]' % (words_xpath, word)
                    #self.log.debug('xpath = %s' % xpath)

                    word = self.source_xml_dict[xpath]
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

    def vault_link0(self, document_instance, article_with_textclip_on_page):  # TODO give this def a better name
        try:
            self.log.enter(document_instance=document_instance, article_with_textclip_on_page=article_with_textclip_on_page)

            page = article_with_textclip_on_page['page_index']
            article = article_with_textclip_on_page['article_index']
            article_id = article_with_textclip_on_page['article_id']

            #print document_instance, page, article, article_id
            asset_id = self.asset_id_page_article(article_id)  # Previously page was being passed in :-(

            where_path = '//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id
            self.log.debug(asset_id=asset_id)

            xpath = '/chapter/page[%s]/article[%s]/articleInfo/title' % (page, article)
            display_link = self.source_xml_dict[xpath]
            if display_link is None or display_link.isspace():
                # consider element empty
                raise SourceDataMissing('articleInfo/title', xpath=xpath)

            return vault_link.vault_link(
                _link_type='external',
                term_id='21902640',
                term_source='Atlas',
                _category='DVI article',
                _data_type='text/xml',
                _action='point',
                where_path=where_path,
                _target='ancestor::gift-doc:document',
                _display_link=EntityReference.escape(display_link)
                )
        finally:
            self.log.exit()
