from project.cho.egest_adapter.doc.document import Document
from project.cho.egest_adapter.doc.document_error import SourceDataMissing, McodeMissing, McodeDuplicate
from gaia.gift.gift25 import meta, media, vault_link, essay
from project.cho.egest_adapter.entity_reference import EntityReference
from qa.models import MCodes


class ConferenceSeries(Document):
    def __init__(self, config, source_xml_dict, extra_args):
        Document.__init__(self, config, source_xml_dict, extra_args)
        self.asset_id_chunk_dict = {}

    def mcode_dict(self, lookup_key):  # TODO refactor commonality
        mcode = MCodes.objects.filter(psmid=lookup_key)
        if len(mcode) == 0:
            raise McodeMissing('Tried to release an item, but we do not yet have an MCode for this item', psm_id=lookup_key)
        if len(mcode) > 1:
            raise McodeDuplicate('Tried to release an item, but found more than 1 mcode in the database', psm_id=lookup_key)
        return  mcode[0].mcode

    def asset_id_page_article(self, page):
        # see: http://jira.cengage.com/browse/CHOA-1074
        #
        # Effectively this code - due to the data being passed into ['chunks'] has divorced the assets ids assigned to articles from how they are assigned inside the gdom :-(
        #
        # This had to be done as chunks contains not only text and binary articles (gift only cares about text); worse, the index into the asset id bears no resemblence
        # to the page we are on in gift.
        try:
            self.log.enter()

            ordered_chunks = sorted(self.extra_args['asset_id']['chunks'].iterkeys())
            # e.g. [u'1', u'10', u'100', u'101', u'102', u'103', u'104', u'105', u'106', u'107', u'108', u'109', u'11', u'110', u'111', u'112', u'113', u'114', u'115', u'116', u'117', u'118', u'119', u'12', u'120', u'121', u'122', u'123', u'124', u'125', u'126', u'127', u'128', u'129', u'13', u'130', u'131', u'132', u'133', u'134', u'135', u'136', u'137', u'138', u'14', u'15', u'16', u'17', u'18', u'19', u'2', u'20', u'21', u'22', u'23', u'24', u'25', u'26', u'27', u'28', u'29', u'3', u'30', u'31', u'32', u'33', u'34', u'35', u'36', u'37', u'38', u'39', u'4', u'40', u'41', u'42', u'43', u'44', u'45', u'46', u'47', u'48', u'49', u'5', u'50', u'51', u'52', u'53', u'54', u'55', u'56', u'57', u'58', u'59', u'6', u'60', u'61', u'62', u'63', u'64', u'65', u'66', u'67', u'68', u'69', u'7', u'70', u'71', u'72', u'73', u'74', u'75', u'76', u'77', u'78', u'79', u'8', u'80', u'81', u'82', u'83', u'84', u'85', u'86', u'87', u'88', u'89', u'9', u'90', u'91', u'92', u'93', u'94', u'95', u'96', u'97', u'98', u'99']
            #
            # meaning:
            # page # 1 = asset id of key u'1'          == self.extra_args['asset_id']['chunks'][u'1'] == u'JKQYDV986277688'
            # page # 2 = asset id of key u'10'       == self.extra_args['asset_id']['chunks'][u'10'] == u'FXFSMG145435618'
            # page # 3 = asset id of key u'100'    == self.extra_args['asset_id']['chunks'][u'10'] == u'HMPXFM019998982'

            correct_asset_key = ordered_chunks[int(page) - 1]  # offset by 1 as array starts at 0
            final_asset_id = self.extra_args['asset_id']['chunks'][correct_asset_key]

            self.log.debug(page=page, final_asset_id=final_asset_id)
            return final_asset_id
        finally:
            self.log.exit()

    def meta_publication_title(self):
        try:
            self.log.enter()
            conference_publication_title = self.source_xml_dict['/chapter/citation/%s/titleGroup/fullTitle' % self.content_type()]

            if conference_publication_title is not None:
                return meta.publication_title(EntityReference.escape('%s' % conference_publication_title))
            else:
                raise SourceDataMissing('conference_publication_title')
        finally:
            self.log.exit()

    def shared_media_page_image(self, page):
        try:
            self.log.enter()

            height_xpath = '/chapter/page[%s]/pageImage/@height' % page
            height = self.source_xml_dict[height_xpath]
            if height is None:
                raise SourceDataMissing('@height', height_xpath=height_xpath)

            width_xpath = '/chapter/page[%s]/pageImage/@width' % page
            width = self.source_xml_dict[width_xpath]
            if width is None:
                raise SourceDataMissing('@width', width_xpath=width_xpath)

            folio = self.source_xml_dict['/chapter/page[%s]/sourcePage' % page]

            sequence_xpath = '/chapter/page[%s]/pageImage' % page
            sequence = self.source_xml_dict[sequence_xpath]
            if sequence.endswith('.jpg'):
                sequence = sequence[:-4]

            if sequence is None or len(sequence) < 5:
                raise SourceDataMissing('pageImage', sequence_xpath=sequence_xpath)
            else:
                sequence = sequence[-4:len(sequence)]

            where = self.source_xml_dict['/chapter/page[%s]/pageImage' % page]

            return media.image(
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
        finally:
            self.log.exit()

    def essay_p(self, words_xpath):
        try:
            self.log.enter(words_xpath=words_xpath)

            words = self.source_xml_dict[words_xpath]
            if words is None:
                return None

            if isinstance(words, basestring):
                text_clip_words_count = 1
            else:
                text_clip_words_count = len(words)

            word_count = 0
            full_text = ''
            for word in range(1, text_clip_words_count + 1):
                xpath = '%s[%s]/@pos' % (words_xpath, word)
                #self.log.debug('xpath = %s' % xpath)

                if self.source_xml_dict[xpath] != '0,0,0,0':
                    xpath = '%s[%s]' % (words_xpath, word)
                    #self.log.debug('xpath = %s' % xpath)

                    word = self.source_xml_dict[xpath]
                    if word is not None:
                        word_count += 1
                        if word_count < text_clip_words_count + 1:
                            word += ' '  # http://www.w3.org/TR/REC-xml/#sec-white-space

                            full_text += EntityReference.escape(word)

            full_text = full_text.rstrip()

            if full_text == None:
                return None

            return essay.p(full_text)
        finally:
            self.log.exit()
