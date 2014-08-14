import os
import tempfile
from gaia.schema.schema import Xsd
from StringIO import StringIO
from lxml import etree
from test_utils.create_cho import meetings, journals, books, conference, reports

# The file name has these parts:
# Project     Publication     Year/Across Multiple years     Volume # / Author Surname as source/ Series     Issue/Part #     Image / audio Sequence     File Extension


class CreateChoXML():
    # we only have 1 example of each contentType
    meet_head = meetings.meet_head
    meet_head_related_media = meetings.meet_head_related_media
    meet_page_01_header = meetings.meet_page_01_header
    meet_page_01_clip = meetings.meet_page_01_clip
    meet_page_01_articleInfo = meetings.meet_page_01_articleInfo
    meet_page_01_textclip = meetings.meet_page_01_textclip
    meet_page_01_footer = meetings.meet_page_01_footer
    meet_mid_0n = meetings.meet_mid_0n
    meet_tail = meetings.meet_tail

    iaxx_head = journals.iaxx_head
    iaxx_mid = journals.iaxx_mid
    iaxx_no_related_mid = journals.iaxx_no_related_mid
    iaxx_tail = journals.iaxx_tail
    related_dict = journals.related_dict

    # TODO implement the following examples in the imports
    book_head = books.book_head
    book_mid = books.book_mid
    book_tail = books.book_tail

    bcrc_head = conference.bcrc_head
    bcrc_mid = conference.bcrc_mid
    bcrc_tail = conference.bcrc_tail

    rpax_head = reports.rpax_head
    rpax_mid = reports.rpax_mid
    rpax_tail = reports.rpax_tail

    @classmethod
    def _get_head(cls, item_type, item_name_stem, item_num, num_pages, data_type):
        xml = None
        # make sure that last digit sequence always starts 0001
        item_name = '%s_%04d' % (item_name_stem, 1)

        if item_type == 'iaxx':
            xml = cls.iaxx_head % (item_name, "1234", item_num, num_pages)
        elif item_type == 'meet':
            if data_type and (data_type == 'Video' or data_type == 'Audio'):
                related_media_id, related_media_media_type, related_media_data_type = cls._related_media(item_name, data_type)
                xml = cls.meet_head_related_media % (item_name, related_media_id, related_media_media_type, related_media_data_type, item_num, num_pages)
            else:
                xml = cls.meet_head % (item_name, item_num, num_pages)
        elif item_type == 'book':
            xml = cls.book_head % (item_name, item_num, num_pages)
        elif item_type == 'bcrc':
            item_name = '%s_%04d' % (item_name_stem, 0)
            mcode = cls._get_mcode(item_name, item_type)
            xml = cls.bcrc_head % (item_name, mcode, item_num, num_pages)
        elif item_type == 'related_iaxx':
            item_name = '%s_%04d' % (item_name_stem, 0)
            mcode = cls._get_mcode(item_name, item_type)
            xml = cls.iaxx_head % (item_name, mcode, item_num, num_pages)
        elif item_type == 'rpax':
            xml = cls.book_head % (item_name, item_num, num_pages)
        return xml

    @classmethod
    def _related_media(cls, item_name, data_type):
        if data_type == 'Audio':
            media_id = '%s.%s' % (item_name, 'mp3')
            media_type = 'Audio'
            data_type_postifx = 'mp3'
        else:
            media_id = '%s.%s' % (item_name, 'mp4')
            media_type = 'Video'
            data_type_postifx = 'mp4'

        return media_id, media_type, data_type_postifx

    @classmethod
    def _get_body(cls, num_pages, img_file_ext, item_type, item_name_stem):
        xml = ''
        for i in range(1, num_pages + 1):
            page_name = '%s_%04d' % (item_name_stem, i)
            img_name = '%s' % page_name

            # pgref = '%04d' % i
            if item_type == 'iaxx':
                xml += cls.iaxx_mid % (i, img_name, i, i, i, i, i, i, num_pages, page_name, i, i)
            
            if item_type == 'related_iaxx':
                if cls.related_dict[item_name_stem][i-1]['docref']:
                    xml += cls.iaxx_mid % (i, img_name, i, i, i, i, i, i, num_pages, cls.related_dict[item_name_stem][i-1]['docref'], cls.related_dict[item_name_stem][i-1]['pgref'], cls.related_dict[item_name_stem][i-1]['articleref'])
                else:
                    xml += cls.iaxx_no_related_mid % (i, img_name, i, i, i, i, i, i, num_pages)

            if item_type == 'bcrc':
                xml += cls.bcrc_mid % (i, img_name, i, i, i, i, i, i, num_pages)

            if item_type == 'rpax':   # TODO: rpax needs to use correct head and body
                #xml += cls.bcrc_mid % (i, img_name, i, i, i, i, i, i, num_pages, page_name)
                xml += cls.bcrc_mid % (i, img_name, i, i, i, i, i, i, num_pages)

            if item_type == 'book':
                xml += cls.book_mid % (i, img_name, i, i, i, i, i, num_pages, page_name)

        if item_type == 'meet':
            xml += cls._get_body_meet(num_pages, img_file_ext, item_type, item_name_stem)

        return xml

    @classmethod
    def _get_body_meet(cls, num_pages, img_file_ext, item_type, item_name_stem):
        # a meeting has 1 article only, this is in the first page
        page_name = '%s_%04d' % (item_name_stem, 1)

        xml = cls.meet_page_01_header % (1, page_name, 1)

        for pgref in range(1, num_pages + 1):
             xml += cls.meet_page_01_clip % (pgref, pgref)

        xml += cls.meet_page_01_articleInfo % str(num_pages)

        for pgref in range(1, num_pages + 1):
            val = str(pgref)
            page_name = '%s_%04d' % (item_name_stem, pgref)
            xml += cls.meet_page_01_textclip % (val, val, page_name, val)

        xml += cls.meet_page_01_footer

        # not do the page elements, without a meeting!
        for id in range(2, num_pages + 1):
            val = str(id)
            page_name = '%s_%04d' % (item_name_stem, id) 
            xml += cls.meet_mid_0n % (val, page_name, val)

        return xml

    @classmethod
    def _get_tail(cls, item_type):
        xml = None
        if item_type == 'iaxx':
            xml = cls.iaxx_tail
        elif item_type == 'related_iaxx':
            xml = cls.iaxx_tail
        elif item_type == 'meet':
            xml = cls.meet_tail
        elif item_type == 'book':
            xml = cls.book_tail
        elif item_type == 'bcrc':
            xml = cls.bcrc_tail
        elif item_type == 'rpax':
            xml = cls.rpax_tail
        return xml

    @classmethod
    def _write_xml_to_file(cls, xml):
        test_dir = tempfile.mkdtemp()
        fpath = os.path.join(test_dir, 'gift.xml')
        fname =  open(fpath, 'w')
        fname.write(xml)
        fname.close()
        return fpath
        
    @classmethod
    def _get_mcode(cls, item_name, item_type):
        if item_type == 'bcrc':
            mcode_dict = conference.mcodes
        elif item_type == 'related_iaxx':
            mcode_dict = journals.mcodes 
        mcode = mcode_dict.get(item_name)
        return mcode 

    @classmethod
    def create_xml_asset(cls, num_pages, img_file_ext, item_type, item_num, item_name_stem, fpath_xsd, data_type=None):
        xml = CreateChoXML._get_head(item_type, item_name_stem, item_num, num_pages, data_type)
        xml += CreateChoXML._get_body(num_pages, img_file_ext, item_type, item_name_stem)
        xml += CreateChoXML._get_tail(item_type)

        xml_fpath = cls._write_xml_to_file(xml)

        Xsd.validate(xml_fpath, os.path.realpath(fpath_xsd))
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(StringIO(xml), parser=parser)
        return etree.tostring(tree, xml_declaration=True, pretty_print=True, encoding='UTF-8')

    @classmethod
    def create(cls, num_pages, img_file_ext, item_type, item_num, asset_dir, item_name_stem, fpath_xsd, data_type):
        xml = CreateChoXML.create_xml_asset(num_pages, img_file_ext, item_type, item_num, item_name_stem, fpath_xsd, data_type)

        if item_type == 'bcrc' or item_type == 'related_iaxx':
            asset_fname = '%s_0000.xml' % item_name_stem
        else:
            asset_fname = '%s_0001.xml' % item_name_stem
        f = open(os.path.join(asset_dir, asset_fname), 'w+')
        f.write(xml)
        f.close()
        return asset_fname
