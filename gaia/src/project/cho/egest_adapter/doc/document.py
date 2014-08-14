# coding=UTF-8

import re
from datetime import datetime
from lxml import etree
from cengage.atlas.atlas_language_dict import AtlasLanguageDict
from gaia.log.log import Log
from gaia.gift.gift25 import meta, essay, media, vault_link, shared, gold, gift_doc
from gaia.gift.gift25.hyphen_element_maker import attr
from project.cho.cho_content_type import ChoContentType
from project.cho.egest_adapter.doc.document_error import DocumentError, SourceDataMissing, AtlasLanguageMissing, AtlasIllustrationMissing, LanguageMissing, McodeMissing, McodeDuplicate
from project.cho.egest_adapter.feed.cho_feed_group import ChoFeedGroup
from project.cho.egest_adapter.entity_reference import EntityReference
from cengage.atlas.atlas_illustration_dict import AtlasIllustrationDict
from project.cho.egest_adapter.language_correction import LanguageCorrection
from qa.models import MCodes
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from project.cho.hard_coded_mcodes import HardCodedMCodes


class Document:  # TODO rename this to Doc?
    FEED_GROUP = None

    def __init__(self, config, source_xml_dict, extra_args):
        self.log = Log.get_logger(self)
        self.config = config
        self.source_xml_dict = source_xml_dict

        psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
        if psmid is None:
            # fundamental problem!
            raise SourceDataMissing('PSMID')
        else:
            self.log.info(PSMID=psmid, FEED_GROUP=self.FEED_GROUP)

        self.extra_args = extra_args
        self.log.info(extra_args)

        self.atlas_language = AtlasLanguageDict()
        self.atlas_illustration = AtlasIllustrationDict()

        # figure out appropriate xpaths, as source_xml_dict doesn't reveal this information :-(
        self.page_article_ids = self._page_article_ids()

        self.page_article_textclip_pgrefs = self._page_article_textclip_pgrefs()
        self.page_article_illustration_pgrefs = self._page_article_illustration_pgrefs()

        self.language_correction = LanguageCorrection(config)

    def _vault_link_related_docs(self, page_article_illustration_pgref): # a text_clip contains n relatedDocument's
        self.log.enter(page_article_illustration_pgref=page_article_illustration_pgref)
        # not everything has related documents, so extra_args might not have anything for us:

        try:
            self.extra_args['related_documents']
        except KeyError,e :
            return None

        # match any relatedDocument's to the page/article/text/textclip that we are on
        page_index = page_article_illustration_pgref['page_index']
        article_index = page_article_illustration_pgref['article_index']
        textclip_index = page_article_illustration_pgref['textclip_index']

        related_document_vault_links = []

        for related_document in self.extra_args['related_documents']:
            for key in related_document[0]:
                page = article = textclip = 1

                # splits up the pgref key from extra args to retrieve the page, article and textclip
                if '@pgref' in key:
                    for split_keys in key.split('/'):
                        if 'page' in split_keys:
                            if '[' and ']' in split_keys:
                                page = split_keys.split('[')[1].split(']')[0]
                        if 'article' in split_keys:
                            if '[' and ']' in split_keys:
                                article = split_keys.split('[')[1].split(']')[0]
                        if 'textclip' in split_keys:
                            if '[' and ']' in split_keys:
                                textclip = split_keys.split('[')[1].split(']')[0]

                    if page_index == int(page) and article_index == int(article) and textclip_index == int(textclip):
                        related_document_pgref = related_document[0][key]

                        if related_document_pgref is None:
                            raise SourceDataMissing('relatedDocument/@pgref', page_article_illustration_pgref=page_article_illustration_pgref)

                        # pgref needs to be prefixed correctly:"Must be four character so "1" must be "0001" 
                        related_document_pgref_refixed = "%04d" % int(related_document_pgref)

                        asset_id = related_document[1]

                        related_document_vault_links.append(vault_link.vault_link(
                            _link_type='external',
                            term_id='19009864',
                            term_source='Atlas',
                            _category='Related document',
                            _action='point',
                            where_path='//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id,
                            _target='ancestor::gift-doc:document',
                            _display_point='//gift-doc:document/gift-doc:body/essay:div/essay:div/essay:complex-meta/meta:page-id-number="%s"' % related_document_pgref_refixed,
                            _display_link=self._related_doc_display_link(related_document[0]['_dom_name'], related_document[0]['_target']['document'])
                            )
                        )

        self.log.exit()

        if len(related_document_vault_links) == 0:
            return None
        else:
            return related_document_vault_links

    def _realted_doc_docref(self):
        pass

    def _realted_doc_chunks(self):
        pass

    def _related_doc_display_link(self, display_link, doc_ref=None):  # get's overloaded by children
        return display_link

    def _page_article_ids(self):
        # return a list of [page, article, article_id] absolute xpaths - we need this info as source_xml_dict only returns a string and not Element(s)
        try:
            self.log.enter()

            page_article_ids = []

            # find all pages
            pages = self.number_of_documents()

            for page in range(1, pages + 1):
                # find all articles on a page
                xpath = '/chapter/page[%s]/article' % page
                self.log.debug(xpath=xpath)

                articles = self.source_xml_dict[xpath]
                if articles is None:
                    continue

                if isinstance(articles, basestring):
                    articles_count = 1
                else:
                    articles_count = len(articles)

                for article in range(1, articles_count + 1):
                    # find all articles on this page & their id
                    xpath = '/chapter/page[%s]/article[%s]/@id' % (page, article)
                    self.log.debug(xpath=xpath)

                    article_id = self.source_xml_dict[xpath]

                    page_article_ids.append({'page_index': page, 'article_index': article, 'article_id': article_id})

            return page_article_ids
        finally:
            self.log.exit()

    def _page_article_textclip_pgrefs(self):
        # return a list of [page, article, textclip, pgref] absolute xpaths - we need this info as source_xml_dict only returns a string and not Element(s)
        try:
            self.log.enter()

            page_article_textclip_pgrefs = []

            # find all pages
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

                for article in range(1, articles_count + 1):
                    # we need article id's as well!
                    article_id = int(self.source_xml_dict['/chapter/page[%s]/article[%s]/@id' % (page, article)])

                    # find all textclips in an article
                    textclips = self.source_xml_dict['/chapter/page[%s]/article[%s]/text/textclip' % (page, article)]
                    if textclips is None:
                        continue

                    if isinstance(textclips, basestring):
                        textclips_count = 1
                    else:
                        textclips_count = len(textclips)

                    for textclip in range(1, textclips_count + 1):
                        # find all pgref values in a textclip
                        pgref = self.source_xml_dict['/chapter/page[%s]/article[%s]/text/textclip[%s]/articlePage/@pgref' % (page, article, textclip)] 

                        if pgref is None:
                            continue
                        page_article_textclip_pgrefs.append(
                            {'page_index': page,
                             'article_index': article,
                             'article_id': article_id,
                             'textclip_index': textclip,
                             'pgref_value': int(pgref)})

            return page_article_textclip_pgrefs
        finally:
            self.log.exit()

    def _page_article_illustration_pgrefs(self):
        # avoid the xml_dict._val 'feature' that returns None for an element with no value, but with attributes.
        try:
            self.log.enter()

            # see if there are any illustrations:
            try:
                if self.extra_args is None or self.extra_args['illustrations'] is None:
                    return None
            except KeyError, e:
                self.log.debug('no illustrations available')
                return None

            page_article_illustation_pgref = []

            for chunk in self.extra_args['illustrations']:
                pgref = None
                _type = None
                caption = None

                for xpath in chunk.info:
                    value = chunk.info[xpath]

                    if '@pgref' in xpath:
                        pgref = value
                        index_page, index_article, index_illustration = self._get_page_article_illustration_indexes(xpath)

                    if '@type' in xpath:
                        _type = value

                    if 'caption' in xpath:  # can be an attribute or an element value!
                        if value is not GaiaDomAdapter.MISSING_FIELD_VALUE:  # signifies an missing element
                            caption = value

                page_article_illustation_pgref.append({'type': _type,
                   'caption': caption,
                   'illustration_pgref': pgref,
                   'index_page': index_page,
                   'index_article': index_article,
                   'index_illustration': index_illustration})

            return page_article_illustation_pgref
        finally:
            self.log.exit()

    def _get_page_article_illustration_indexes(self, value):
        try:
            self.log.enter()
            page_index = '1'
            article_index = '1'
            illustration_index = '1'

            for value in value.split('/'):
                if 'page[' in value:
                    page_index = value.replace('page[', '')
                    page_index = page_index.replace(']', '')

                if 'article[' in value:
                    article_index = value.replace('article[', '')
                    article_index = article_index.replace(']', '')

                if 'illustration[' in value:
                    illustration_index = value.replace('illustration[', '')
                    illustration_index = illustration_index.replace(']', '')

            return int(page_index), int(article_index), int(illustration_index)
        finally:
            self.log.exit()

    def content_type(self):
        try:
            self.log.enter()
            chapter_citation_book_value = self.source_xml_dict['/chapter/citation/book']
            return ChoContentType.content_type(chapter_citation_book_value, self.product_content_type())
        finally:
            self.log.exit()

    def product_content_type(self):
        try:
            self.log.enter()

            product_content_type_xpath = '/chapter/metadataInfo/productContentType'
            product_content_type = self.source_xml_dict[product_content_type_xpath]
            if product_content_type is None:
                raise SourceDataMissing('productContentType', product_content_type_xpath=product_content_type_xpath)
            else:
                return product_content_type
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
                asset_id = self.asset_id(document_instance)
                if asset_id is None:
                    raise DocumentError('No Asset Id', document_instance=document_instance)

                return meta.document_ids(
                    _type0='Gale asset',
                    _value0=asset_id
                    )
        finally:
            self.log.exit()

    def asset_id(self, page):
        try:
            return self.extra_args['asset_id']['pages'][unicode(page)]
        except KeyError:
            raise DocumentError('unable to lookup pages asset_id from extra_args', page=page)

    def asset_id_document(self):
        try:
            return self.extra_args['asset_id']['document']
        except KeyError:
            raise DocumentError('unable to lookup document asset_id from extra_args')

    def _mcode(self, psmid=None):  # easier 'monkey patching'
        hard_coded_mcode = HardCodedMCodes.mcode_from_psmid(psmid)
        if hard_coded_mcode is not None:
            return [MCodes(psmid=psmid, mcode=hard_coded_mcode, publication_title=None)]

        return MCodes.objects.filter(psmid=psmid)

    def meta_mcode(self):
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            if psmid is None:
                raise SourceDataMissing('PSMID')

            mcode = self._mcode(psmid)
            if len(mcode) == 0:
                raise McodeMissing('Tried to release an item, but we do not yet have an MCode for this item', psm_id=psmid)
            if len(mcode) > 1:
                raise McodeDuplicate('Tried to release an item, but found more than 1 mcode in the database', psm_id=psmid)
            return meta.mcode(
                mcode[0].mcode
                )

        finally:
            self.log.exit()

    def meta_publication_date(self):
        try:
            self.log.enter()

            # we either have an irregular date or any of the other elements, BUT start and send data also present!
            start_date_xpath = '/chapter/citation/%s/pubDate/pubDateStart' % self.content_type()
            start_date = self.source_xml_dict[start_date_xpath]

            if start_date is None:
                raise SourceDataMissing('pubDateStart', start_date_xpath=start_date_xpath)

            end_date_xpath = '/chapter/citation/%s/pubDate/pubDateEnd' % self.content_type()
            end_date = self.source_xml_dict[end_date_xpath]
            if end_date is None:
                raise SourceDataMissing('pubDateEnd', end_date_xpath=end_date_xpath)

            irregular = self.source_xml_dict['/chapter/citation/%s/pubDate/irregular' % self.content_type()]
            if irregular is not None:
                return meta.publication_date(
                    _irregular_value=irregular,
                    _start_date=start_date.replace('-', ''),
                    _end_date=end_date.replace('-', '')
                )
            else:
                return meta.publication_date(
                    _year=self.source_xml_dict['/chapter/citation/%s/pubDate/year' % self.content_type()],
                    _month=self.source_xml_dict['/chapter/citation/%s/pubDate/month' % self.content_type()],
                    _day=self.source_xml_dict['/chapter/citation/%s/pubDate/day' % self.content_type()],
                    _day_of_week=self.source_xml_dict['/chapter/citation/%s/pubDate/dayofweek' % self.content_type()],
                    _start_date=start_date.replace('-', ''),
                    _end_date=end_date.replace('-', '')
                    )
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

    def creation_type(self):
        return 'Original'  # TODO changes depending upon rework [ 'Original', 'Replace']

    def creation_date(self):
        date_time = datetime.now()
        return '%d%02d%02d' % (date_time.year, date_time.month, date_time.day)

    def _language_correction(self, psmid):
        # get languages from csv spread sheet
        cont_type = ""
        if str(self.product_content_type()) == "Special Publications":
            if self.source_xml_dict['/chapter/citation/book'] != None: # Refugee Survey
                cont_type = "book"
            elif self.source_xml_dict['/chapter/citation/journal'] != None: # Weekly Review of Foreign Press Journal
                cont_type = "journal"
            languages = self.language_correction.get_parent_languages(str(self.product_content_type()), psmid, content_type=cont_type)
        else:
            languages = self.language_correction.get_parent_languages(str(self.product_content_type()), psmid, content_type=str(self.content_type()))

        return languages

    def meta_languages(self):
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']

            meta_languages_list = []

            languages = self._language_correction(psmid)
            if languages == []:
                raise LanguageMissing('psmid "%s" not in language table' % psmid)

            for language in languages:
                language_value = self.atlas_language[language]
                if language_value is None:
                    raise AtlasLanguageMissing(language=language)

                ocr = language

                if language == languages[0]:
                    yes_or_no = 'Y'
                else:
                    yes_or_no = 'N'

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

    def meta_ocr_confidence(self):
        try:
            self.log.enter()

            ocr_confidence_xpath = '/chapter/metadataInfo/ocr'
            ocr_confidence = self.source_xml_dict[ocr_confidence_xpath]
            if ocr_confidence is None:
                raise SourceDataMissing('metadataInfo/ocr', ocr_confidence_xpath=ocr_confidence_xpath)

            return meta.ocr_confidence(ocr_confidence)
        finally:
            self.log.exit()

    def total_pages(self):
        try:
            self.log.enter()

            xpath = '/chapter/citation/%s/totalPages' % self.content_type()
            value = self.source_xml_dict[xpath]
            if value is None:
                raise SourceDataMissing('totalPages', xpath=xpath, productContentType=self.content_type())
            else:
                return value
        finally:
            self.log.exit()

    def essay_container_divs(self):
        try:
            self.log.enter()

            number_of_pages = int(self.total_pages())
            div_list = []
            for page in range(1, number_of_pages + 1):

                # get a list of all articles on this page
                xpath = '/chapter/page[%s]/article' % page
                self.log.debug('xpath = %s' % xpath)
                articles_on_page = self.source_xml_dict[xpath]

                if articles_on_page is not None:
                    if isinstance(articles_on_page, basestring):
                        articles_on_page_count = 1
                    else:
                        articles_on_page_count = len(articles_on_page)

                    for article in range(1, articles_on_page_count + 1):
                        # get a list of all textclip's
                        xpath = '/chapter/page[%s]/article[%s]/text/textclip' % (page, article)
                        self.log.debug('xpath = %s' % xpath)

                        text_clips = self.source_xml_dict[xpath]
                        if isinstance(text_clips, basestring):
                            text_clips_count = 1
                        else:
                            text_clips_count = len(text_clips)

                        for text_clip in range(1, text_clips_count + 1):
                            div_list.append(self.essay_divs_from_page(page, article, text_clip))

            div_container = essay.div_container(
                'Body text',
                '14214508',
                'Atlas',
                div_list
                )

            return div_container
        finally:
            self.log.exit()

    def essay_divs_from_page(self, page, article, text_clip):
        try:
            self.log.enter()
            contents_list = []

            complex_meta_list = []

            xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/articlePage' % (page, article, text_clip)
            page_id_number = self.source_xml_dict[xpath]

            if page_id_number is None or len(page_id_number) < 5:
                raise SourceDataMissing('articlePage number', xpath=xpath)
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

            _essay_p = None
            if self.FEED_GROUP == ChoFeedGroup.MEETING_MEGA:
                _essay_p = self.essay_p(page, article, text_clip)

            sequence_xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/articlePage' % (page, article, text_clip)
            sequence = self.source_xml_dict[sequence_xpath]
            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('articlePage sequence', sequence_xpath=sequence_xpath)
            else:
                sequence = sequence[-4:len(sequence)]

            pgref_xpath = '/chapter/page[%s]/article[%s]/text/textclip[%s]/articlePage/@pgref' % (page, article, text_clip)
            pgref = self.source_xml_dict[pgref_xpath]
            if pgref is None:
                raise SourceDataMissing('articlePage/@pgref', pgref_xpath=pgref_xpath)

            width_xpath = '/chapter/page[%s]/pageImage/@width' % pgref
            width = self.source_xml_dict[width_xpath]
            if width is None:
                raise SourceDataMissing('pageImage/@width', width_xpath=width_xpath)

            height_xpath = '/chapter/page[%s]/pageImage/@height' % pgref
            height = self.source_xml_dict[height_xpath]
            if height is None:
                raise SourceDataMissing('pageImage/@height', height_xpath=height_xpath)

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % pgref]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % pgref]
            if where.endswith('.jpg'):
                where = where[:-4]

            _shared_media = shared.media(
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

            asset_id = self.asset_id(pgref)
            if asset_id is None:
                raise DocumentError('No Asset Id', pgref=pgref)

            where = '//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="%s"]' % asset_id

            _vault_link0 = vault_link.vault_link(
                    _link_type='external',
                    term_id='21902636',
                    term_source='Atlas',
                    _category='DVI page',
                    _action='point',
                    where_path=where,
                    _target='ancestor::gift-doc:document'
                    )

            # find all related document vault-link's on this page / article / textclip
            related_doc_vault_links = self._vault_link_related_docs({'page_index': page, 'article_index': article, 'textclip_index': text_clip})

            return essay.div_related_doc(
                'Page',
                '21922233',
                'Atlas',
                _complex_meta=complex_meta_list,
                essay_p=_essay_p,
                shared_media=_shared_media,
                vault_link=_vault_link0,
                vault_link_related_doc=related_doc_vault_links
                )
        finally:
            self.log.exit()

    def document_instances(self):
        try:
            self.log.enter()
            document_instances = []

            document_instance_count = self.number_of_documents()
            for document_instance in range(1, document_instance_count + 1):

                doc_inst_str = self._gold_document_instances(document_instance)
                doc_inst_str_pretty_printed = EntityReference.unescape(etree.tostring(doc_inst_str, pretty_print=True))

                document_instances.append(doc_inst_str_pretty_printed)

            return document_instances
        finally:
            self.log.exit()

    def _gold_document_instances(self, document_instance):
        try:
            self.log.enter()
            return gold.document_instance(
                gift_doc.document(
                    gift_doc.metadata(
                        self.gift_doc_node_metadata(document_instance),
                        self.gift_doc_document_metadata(document_instance)
                        ),
                    self.gift_doc_body(document_instance)
                    )
                )
        finally:
            self.log.exit()

    def gift_doc_node_metadata(self, document_instance):
        try:
            self.log.enter()

            page_number_xpath = '/chapter/page[%s]/pageImage' % document_instance
            page_number = self.source_xml_dict[page_number_xpath]
            if page_number.endswith('.jpg'):
                page_number = page_number[:-4]

            if page_number is None:
                raise SourceDataMissing('pageImage', page_number_xpath=page_number_xpath)

            page_number = page_number[-4:len(page_number)]

            return gift_doc.node_metadata(
                gift_doc.pagination_group(
                    gift_doc.pagination(
                        meta.ranges(
                            meta.range(
                                meta.begin_page(page_number)
                                )
                            ),
                        meta.total_pages(self.total_pages())
                        )
                    )
                )
        finally:
            self.log.exit()

    def number_of_documents(self):
        try:
            self.log.enter()

            xpath = '/chapter/page'
            value = self.source_xml_dict[xpath]
            if value is None:
                raise SourceDataMissing('page', xpath=xpath)
            else:
                if isinstance(value, basestring):
                    return 1
                else:
                    return len(value)
        finally:
            self.log.exit()

    def number_of_articles(self):
        try:
            self.log.enter()
            value = self.source_xml_dict['/chapter/page/article']
            if value is None:
                raise SourceDataMissing('article')
            else:
                if isinstance(value, basestring):
                    return 1
                else:
                    return len(value)
        finally:
            self.log.exit()

    def meta_folio(self, document_instance):
        try:
            self.log.enter()

            source_page = self.source_xml_dict['/chapter/page[%s]/sourcePage' % document_instance]
            if source_page is None:
                return None  # its optional

            return meta.folio(
                meta.start_number(source_page)
                )
        finally:
            self.log.exit()

    def essay_div_body(self, div):
        try:
            self.log.enter()
            return essay.div(
                'Body text',
                '14214508',
                'Atlas',
                _div=div
                )
        finally:
            self.log.exit()

    def essay_complex_meta(self, document_instance):
        try:
            self.log.enter()

            essay_complex_meta_list = []

            page_id_number = self.source_xml_dict['/chapter/page[%s]/pageImage' % document_instance]
            if page_id_number.endswith('.jpg'):
                page_id_number = page_id_number[:-4]

            if page_id_number is None or len(page_id_number) < 5:
                raise SourceDataMissing('pageImage')
            else:
                page_id_number = page_id_number[-4:len(page_id_number)]
                essay_complex_meta_list.append(
                    meta.page_id_number(str(page_id_number)
                    )
                )

            meta_folio = self.meta_folio(document_instance)
            if meta_folio is not None:
                essay_complex_meta_list.append(meta_folio
                )

            return essay.complex_meta(*essay_complex_meta_list)
        finally:
            self.log.exit()

    def meta_document_titles(self):
        try:
            self.log.enter()

            # all three elements have the same xpath!!
            titles_xpath = '/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()
            titles = self.source_xml_dict[titles_xpath]

            if titles is None:
                raise SourceDataMissing('fullTitle', titles_xpath=titles_xpath)

            titles = EntityReference.escape(titles)

            args = []
            if titles is not None:
                args.append(meta.title_display(
                    titles
                    )
                )

            if titles is not None:
                args.append(meta.title_sort(
                    self._meta_document_titles_rules(titles)
                    )
                )

            if titles is not None:
                args.append(meta.title_open_url(
                    self._meta_document_titles_rules(titles)
                    )
                )

            subtitle = self.source_xml_dict['/chapter/citation/%s/titleGroup/fullSubtitle' % self.content_type()]

            if subtitle is not None:
                args.append(meta.subtitle(
                    subtitle
                    )
                )

            return gift_doc.document_titles(*args)
        finally:
            self.log.exit()

    def _meta_document_titles_rules(self, value):
        '''
         - strip out leading articles (A, An, The)
         - strip out all single, double quotes and left and right single and double quotation marks
         - strip out all HTML tags including "&#x2013;"
         - strip off any trailing commas or full stops.
        '''
        removal_prefixes = ['A ', 'An ', 'The ']

        try:
            self.log.enter(value=value)

            value = EntityReference.strip_out_various_entities(value)

            for prefix in removal_prefixes:
                if value.startswith(prefix):
                    value = value[len(prefix):]
                    break   # must only ever remove ONE prefix

            return value
        finally:
            self.log.exit()

    def meta_authors(self):
        try:
            self.log.enter()
            authors = []

            author_list = self.source_xml_dict['/chapter/citation/%s/author' % self.content_type()]

            byline = self.source_xml_dict['/chapter/citation/%s/byline' % self.content_type()]
            if byline is not None:
                authors.append(
                    meta.corporate_author(byline)
                )

            if author_list is not None:
                author_count = len(author_list)
                for author_index in range(1, author_count + 1):

                    role = self.source_xml_dict['/chapter/citation/%s/author[%s]/@role' % (self.content_type(), author_index)]
                    if role == u'author':

                        prefix = self.source_xml_dict['/chapter/citation/%s/author[%s]/prefix' % (self.content_type(), author_index)]
                        prefix = prefix

                        first = self.source_xml_dict['/chapter/citation/%s/author[%s]/first' % (self.content_type(), author_index)]
                        middle = self.source_xml_dict['/chapter/citation/%s/author[%s]/middle' % (self.content_type(), author_index)]
                        last = self.source_xml_dict['/chapter/citation/%s/author[%s]/last' % (self.content_type(), author_index)]
                        suffix = self.source_xml_dict['/chapter/citation/%s/author[%s]/suffix' % (self.content_type(), author_index)]
                        sobriquet = self.source_xml_dict['/chapter/citation/%s/author/sobriquet' % self.content_type()]

                        xpath_aucomposed = '/chapter/citation/%s/author[%s]/aucomposed' % (self.content_type(), author_index)
                        aucomposed = self.source_xml_dict[xpath_aucomposed]

                        if first is None or last is None:
                            name = ''

                            if prefix is not None:
                                name += prefix

                            if first is not None:
                                if name is not '':
                                    name += ' '
                                name += first

                            if middle is not None:
                                if name is not '':
                                    name += ' '
                                name += middle

                            if last is not None:
                                if name is not '':
                                    name += ' '
                                name += last

                            if suffix is not None:
                                if name is not '':
                                    name += ' '
                                name += suffix

                            if len(name) == 0:
                                name = sobriquet

                            meta_sobriquet = meta.sobriquet(
                                meta.name(name)
                                )

                            if aucomposed is None:
                                raise SourceDataMissing('aucomposed', xpath_aucomposed=xpath_aucomposed)

                            meta_composed_name = meta.composed_name(aucomposed)

                            authors.append(
                                meta.author(
                                    meta_sobriquet,
                                    meta_composed_name
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
                return meta.authors(
                    *authors
                    )
            else:
                return None
        finally:
            self.log.exit()

    def meta_editors(self):  # very similar to authors but a different xpaths!
        try:
            self.log.enter()
            editors = []

            editors_xml = self.source_xml_dict['/chapter/citation/%s/author' % self.content_type()]
            if editors_xml is None:
                return None

            editor_count = len(editors_xml)
            for editor_index in range(1, editor_count + 1):

                role = self.source_xml_dict['/chapter/citation/%s/author[%s]/@role' % (self.content_type(), editor_index)]
                if role == u'editor':

                    prefix = self.source_xml_dict['/chapter/citation/%s/author[%s]/prefix' % (self.content_type(), editor_index)]
                    first = self.source_xml_dict['/chapter/citation/%s/author[%s]/first' % (self.content_type(), editor_index)]
                    middle = self.source_xml_dict['/chapter/citation/%s/author[%s]/middle' % (self.content_type(), editor_index)]
                    last = self.source_xml_dict['/chapter/citation/%s/author[%s]/last' % (self.content_type(), editor_index)]
                    suffix = self.source_xml_dict['/chapter/citation/%s/author[%s]/suffix' % (self.content_type(), editor_index)]

                    aucomposed_xpath = '/chapter/citation/%s/author[%s]/aucomposed' % (self.content_type(), editor_index)
                    aucomposed = self.source_xml_dict[aucomposed_xpath]

                    if first is None or last is None:
                        name = ''

                        if prefix is not None:
                            name += prefix

                        if first is not None:
                            if name is not '':
                                name += ' '
                            name += first

                        if middle is not None:
                            if name is not '':
                                name += ' '
                            name += middle

                        if last is not None:
                            if name is not '':
                                name += ' '
                            name += last

                        if suffix is not None:
                            if name is not '':
                                name += ' '
                            name += suffix

                        meta_sobriquet = meta.sobriquet(
                            meta.name(name)
                            )

                        if aucomposed is None:
                            raise SourceDataMissing('aucomposed', aucomposed_xpath=aucomposed_xpath)

                        meta_composed_name = meta.composed_name(aucomposed)

                        editors.append(
                            meta.editor(
                                meta_sobriquet,
                                meta_composed_name
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

                        editors.append(
                            meta.editor(
                                mega_structured_name,
                                meta_composed_name
                            )
                        )

            if len(editors) > 0:
                return meta.editors(
                    *editors
                    )
            else:
                return None
        finally:
            self.log.exit()

    def copyright_statement(self):
        try:
            self.log.enter()

            copyright_statement = self.source_xml_dict['/chapter/metadataInfo/sourceLibrary/copyrightStatement']
            if copyright_statement is None:
                raise SourceDataMissing('copyrightStatement')
            else:
                return copyright_statement
        finally:
            self.log.exit()

    def meta_holding_institution(self):
        try:
            self.log.enter()

            return meta.holding_institution(
                meta.institution_name(
                    'Chatham House'
                ),
                meta.institution_location(
                    'London'
                )
            )
        finally:
            self.log.exit()

    def meta_content_date(self):
        try:
            self.log.enter()
            # we either have an irregular date or any of the other elements, BUT start and send data also present!
            start_date = self.source_xml_dict['/chapter/metadataInfo/contentDate/contentDateStart']
            end_date = self.source_xml_dict['/chapter/metadataInfo/contentDate/contentDateEnd']

            if start_date is None or end_date is None:
                raise SourceDataMissing('contentDate Start or End')

            irregular_value = self.source_xml_dict['/chapter/metadataInfo/contentDate/contentIrregular']
            if irregular_value is not None:
                return meta.content_date(
                    _irregular_value=irregular_value,
                    _start_date=start_date.replace('-', ''),
                    _end_date=end_date.replace('-', '')
                    )
            else:
                return meta.content_date(
                    _year=self.source_xml_dict['/chapter/metadataInfo/contentDate/contentYear'],
                    _month=self.source_xml_dict['/chapter/metadataInfo/contentDate/contentMonth'],
                    _day=self.source_xml_dict['/chapter/metadataInfo/contentDate/contentDay'],
                    _day_of_week=self.source_xml_dict['/chapter/metadataInfo/contentDate/contentDayofweek'],
                    _start_date=start_date.replace('-', ''),
                    _end_date=end_date.replace('-', ''),
                    )
        finally:
            self.log.exit()

    def gift_doc_pagination_group(self):
        try:
            self.log.enter()

            return gift_doc.pagination_group(
                gift_doc.pagination(
                    meta.total_pages(self.total_pages())
                    )
                )
        finally:
            self.log.exit()

    def meta_volume_number(self):
        try:
            self.log.enter()
            volume_number = self.source_xml_dict['/chapter/citation/%s/volumeGroup/volumeNumber' % self.content_type()]

            if volume_number is not None:
                return meta.volume_number(volume_number)
            else:
                return None
        finally:
            self.log.exit()

    def meta_bibliographic_ids_psmid_isbn_issn(self, document_instance=0):
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            if psmid is None:
                raise SourceDataMissing('PSMID')

            # there can be upto two isbn's, but both must be a different length
            isbn_lengths = self.source_xml_dict['/chapter/metadataInfo/isbn/@length']
            isbns = self.source_xml_dict['/chapter/metadataInfo/isbn']

            isbn0 = None
            isbn1 = None

            if isbns is not None:
                if isinstance(isbn_lengths, basestring):
                    isbn0 = isbns
                else:
                    if len(isbns) > 2:
                        raise DocumentError("too many isbns", isbns=isbns)

                    if len(isbn_lengths) == 2:
                        if isbn_lengths[0] == isbn_lengths[1]:
                            raise DocumentError("2 isbn's with same length!", isbns=isbn_lengths)

                    isbn0 = isbns[0]
                    isbn1 = isbns[1]

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

    def meta_bibliographic_ids_psmid(self):
        try:
            self.log.enter()

            psmid = self.source_xml_dict['/chapter/metadataInfo/PSMID']
            if psmid is None:
                raise SourceDataMissing('PSMID')

            if psmid is not None:
                return meta.bibliographic_ids(
                    'PSM',
                    psmid
                    )
        finally:
            self.log.exit()

    def shared_media_illustration_image(self, page_article_illustration_pgref):
        try:
            self.log.enter()

            page_pgref = page_article_illustration_pgref['illustration_pgref']

            height = self.source_xml_dict['/chapter/page[%s]/pageImage/@height' % page_pgref]
            if height is None:
                raise SourceDataMissing('@height')

            width = self.source_xml_dict['/chapter/page[%s]/pageImage/@width' % page_pgref]
            if width is None:
                raise SourceDataMissing('@width')

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % page_pgref]

            sequence = self.source_xml_dict['/chapter/page[%s]/pageImage' % page_pgref]
            if sequence.endswith('.jpg'):
                sequence = sequence[:-4]

            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('pageImage')
            else:
                sequence = sequence[-4:len(sequence)]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % page_pgref]
            if where.endswith('.jpg'):
                where = where[:-4]

            caption = page_article_illustration_pgref['caption']

            illustration = page_article_illustration_pgref['type']
            if illustration is None:
                raise AtlasIllustrationMissing('illustration/@type')
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

    def _validate_isbns(self, isbns, isbn_lengths):
        if isinstance(isbns, basestring) or isbns is None:
            return

        if len(isbns) > 2:
            raise DocumentError('isbn(s) not good', isbns=isbns)

        if isbn_lengths.count('10') >= 2:
            raise DocumentError('isbn(s) not good', isbns=isbns)

        if isbn_lengths.count('13') >= 2:
            raise DocumentError('isbn(s) not good', isbns=isbns)
