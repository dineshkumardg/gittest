import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()


from django.test import TestCase
from qa.ws.views import WSItem
from lxml import etree
import os


class TestViews(TestCase):
    """
    Test that fix's are applied against the original source xml
    """
    def _assertEquals(self, original_xml_fname, possible_fixes, expected_xml_fname, dump_to_file=True, assert_msg='fail: not equal'):
        original_xml = open(os.path.join(os.path.dirname(__file__), 'test_data/%s' % original_xml_fname)).read()
        ws_item = WSItem()
        actual_xml = etree.tostring(ws_item.patch(etree.fromstring(original_xml), possible_fixes))
        expected_xml = open(os.path.join(os.path.dirname(__file__), 'test_data/%s' % expected_xml_fname)).read()

        try:
            self.assertEqual(expected_xml, actual_xml, msg=assert_msg)
        except AssertionError as e:
            if dump_to_file:
                f = open(os.path.join(os.path.dirname(__file__), 'test_data/,%s.actual' % original_xml_fname), 'w')  # , in .gitignore
                f.write(actual_xml)
                f.close()
            raise e

    def test_patch_conference_series(self):
        original_xml_fname = 'cho_bcrc_1933_0001_000_0000.xml'
        possible_info_fixes = [
            {u'_asset_fname': u'cho_bcrc_1933_0001_000_0001.jpg', u'/chapter/page[1]/article/text/textclip/footnote/word': u'_IS_ABSENT_', u'_dom_name': u'_IS_ABSENT_', u'_dom_id': 1, u'/chapter/page[1]/sourcePage': u'_IS_ABSENT_', u'_img_url': u'cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0001.jpg', u'_id': 1, u'@id': u'1 FIX#01', u'_thumb_url': u'cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0001_thumbnail.jpg'},
            {u'/chapter/page[1]/article/articleInfo/pageCount': u'1 FIX#05', u'/chapter/page[1]/article/articleInfo/language': u'English FIX#04', u'_page_ids': [1], u'/chapter/page[1]/article/articleInfo/title': u'Front Matter FIX#07', u'/chapter/page[1]/article/articleInfo/startingColumn': u'A FIX#06', u'_dom_name': u'Front Matter', u'/chapter/page[1]/article/@type': u'front_matter FIX#03', u'/chapter/page[1]/article/articleInfo/byline': u'_IS_ABSENT_', u'/chapter/page[1]/article/articleInfo/author/aucomposed': u'_IS_ABSENT_', u'/chapter/page[1]/article/@id': u'1 FIX#01', u'_clip_ids': None, u'_dom_id': 1, u'/chapter/page[1]/article/articleInfo/issueNumber': u'_IS_ABSENT_', u'/chapter/page[1]/article/articleInfo/issueTitle': u'_IS_ABSENT_', u'/chapter/page[1]/article/text/textclip/marginalia': u'_IS_ABSENT_', u'/chapter/page[1]/article/@level': u'1 FIX#02', u'/chapter/page[1]/article/articleInfo/author/@type': u'_IS_ABSENT_', u'_is_binary': False},
            {u'/chapter/page[4]/article/articleInfo/byline': u'_IS_ABSENT_', u'_page_ids': [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54], u'/chapter/page[4]/article/articleInfo/title': u'Opening Session First Business Session', u'/chapter/page[4]/article/text/textclip/marginalia': u'OPENING SESSION', u'/chapter/page[4]/article/articleInfo/author/@type': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/language': u'English', u'/chapter/page[4]/article/articleInfo/issueTitle': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/pubDate/pubDateStart': u'1933-09-11', u'_clip_ids': None, u'_dom_id': 3, u'/chapter/page[4]/article/@level': u'1', u'/chapter/page[4]/article/articleInfo/pubDate/pubDateEnd': u'1933-09-11', u'/chapter/page[4]/article/articleInfo/imprint': u'\t\t\t\t\t', u'/chapter/page[4]/article/articleInfo/author/aucomposed': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/publicationPlace': u'\t\t\t\t\t', u'_dom_name': u'Opening Session First Business Session', u'/chapter/page[4]/article/articleInfo/pubDate/composed': u'September 11, 1933', u'/chapter/page[4]/article/articleInfo/pageCount': u'51', u'/chapter/page[4]/article/@type': u'article', u'/chapter/page[4]/article/articleInfo/pubDate/month': u'09', u'/chapter/page[4]/article/articleInfo/pubDate/year': u'1933', u'/chapter/page[4]/article/articleInfo/startingColumn': u'A', u'/chapter/page[4]/article/articleInfo/issueNumber': u'_IS_ABSENT_', u'/chapter/page[4]/article/@id': u'3 FIX#02', u'_is_binary': False},
            {u'_id': 5, u'_dom_name': u'[1]', u'/chapter/page[5]/article/text/textclip/footnote/word': u'_IS_ABSENT_', u'_dom_id': 5, u'_img_url': u'cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0005.jpg', u'/chapter/page[5]/sourcePage': u'[1] FIX#01', u'_asset_fname': u'cho_bcrc_1933_0001_000_0005.jpg', u'@id': u'5', u'_thumb_url': u'cho_bcrc_1933_0001_000_0000/10126/cho_bcrc_1933_0001_000_0005_thumbnail.jpg'},
            {u'/chapter/citation/conference/byline': u'_IS_ABSENT_', u'/chapter/@contentType': u'book FIX#08', u'/chapter/metadataInfo/language': u'English FIX#25', u'/chapter/citation/conference/volumeGroup/volumeNumber': u'1 FIX#17', u'/chapter/metadataInfo/PSMID': u'cho_bcrc_1933_0001_000_0000 FIX#19', u'/chapter/citation/conference/pubDate/composed': u'September 11th-21st, 1933 FIX#11', u'/chapter/citation/conference/pubDate/pubDateEnd': u'1933-09-21 FIX#13', u'/chapter/citation/conference/author/@role': u'_IS_ABSENT_', u'/chapter/metadataInfo/contentDate/contentIrregular': u'September 11th-21st, 1933 FIX#24', u'/chapter/citation/conference/conferenceGroup/conferenceLocation': u'Toronto FIX#09', u'_dom_id': u'cho_bcrc_1933_0001_000_0000', u'/chapter/metadataInfo/issn': u'_IS_ABSENT_', u'/chapter/citation/conference/pubDate/irregular': u'September 11th-21st, 1933 FIX#12', u'/chapter/citation/conference/conferenceGroup/conferenceName': u'British Commonwealth Relations. 1st Conference FIX#10', u'/chapter/metadataInfo/chathamHouseRule': u'No FIX#20', u'/chapter/metadataInfo/productContentType': u'Conference Series FIX#26', u'/chapter/metadataInfo/isbn': u'_IS_ABSENT_', u'/chapter/citation/conference/pubDate/pubDateStart': u'1933-09-11 FIX#14', u'/chapter/metadataInfo/contentDate/contentComposed': u'September 11th-21st, 1933 FIX#21', u'_dom_name': u'cho_bcrc_1933_0001_000_0000', u'/chapter/citation/conference/volumeGroup/volumeTitle': u'Verbatim reports FIX#18', u'/chapter/citation/conference/editionStatement': u'_IS_ABSENT_', u'/chapter/citation/conference/titleGroup/fullTitle': u'British Commonwealth Relations Conference FIX#15', u'/chapter/metadataInfo/contentDate/contentDateEnd': u'1933-09-21 FIX#22', u'/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England FIX#28', u'/chapter/citation/conference/editionNumber': u'_IS_ABSENT_', u'/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs FIX#27', u'/chapter/metadataInfo/contentDate/contentDateStart': u'1933-09-11 FIX#23', u'/chapter/citation/conference/totalPages': u'806 FIX#16', u'/chapter/citation/conference/author/@type': u'_IS_ABSENT_', u'/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House FIX#29'},
            ]

        expected_xml_fname = 'cho_bcrc_1933_0001_000_0000.xml.expected'

        self._assertEquals(original_xml_fname, possible_info_fixes, expected_xml_fname)

    def test_patch_book(self):
        original_xml_fname = 'cho_book_1933_grubb_000_0000.xml'
        possible_info_fixes = [
            {u'/chapter/page[4]/article/articleInfo/byline': u'_IS_ABSENT_', u'_page_ids': [4], u'/chapter/page[4]/article/articleInfo/title': u'Preface FIX#10', u'/chapter/page[4]/article/text/textclip/marginalia': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/issueTitle': u'_IS_ABSENT_', u'_dom_name': u'Preface', u'/chapter/page[4]/article/articleInfo/author/middle': u'G. FIX#06', u'/chapter/page[4]/article/articleInfo/issueNumber': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/author/first': u'Kenneth FIX#04', u'_clip_ids': None, u'/chapter/page[4]/article/articleInfo/author/@type': u'_IS_ABSENT_', u'/chapter/page[4]/article/articleInfo/author/last': u'Grubb FIX#05', u'/chapter/page[4]/article/articleInfo/language': u'English FIX#07', u'/chapter/page[4]/article/articleInfo/pageCount': u'1 FIX#08', u'/chapter/page[4]/article/articleInfo/startingColumn': u'A FIX#09', u'_dom_id': 4, u'/chapter/page[4]/article/articleInfo/author/aucomposed': u'Kenneth G. Grubb', u'/chapter/page[4]/article/@id': u'4 FIX#01', u'/chapter/page[4]/article/@level': u'1 FIX#02', u'/chapter/page[4]/article/@type': u'front_matter FIX#03', u'_is_binary': False},
            {u'/chapter/citation/book/pubDate/year': u'1933 FIX#22', u'_dom_id': u'cho_book_1933_grubb_000_0000', u'/chapter/citation/book/seriesGroup/seriesNumber': u'10 FIX#26', u'/chapter/@contentType': u'book FIX#11', u'/chapter/citation/book/byline': u'_IS_ABSENT_', u'/chapter/metadataInfo/language': u'English FIX#38', u'/chapter/metadataInfo/contentDate/contentDecade': u'1930-1939 FIX#35', u'/chapter/citation/book/author/@role': u'author FIX#12', u'/chapter/metadataInfo/PSMID': u'cho_book_1933_grubb_000_0000 FIX#30', u'/chapter/citation/book/pubDate/pubDateEnd': u'1933-11-30 FIX#20', u'/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'London, UK FIX#24', u'/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England FIX#41', u'/chapter/citation/book/totalPages': u'160 FIX#29', u'/chapter/metadataInfo/contentDate/contentYear': u'1933 FIX#37', u'/chapter/metadataInfo/issn': u'_IS_ABSENT_', u'/chapter/metadataInfo/contentDate/contentDateStart': u'1933-11-01 FIX#34', u'/chapter/citation/book/titleGroup/fullTitle': u'The Republics of South America FIX#28', u'/chapter/metadataInfo/chathamHouseRule': u'No FIX#31', u'/chapter/citation/book/editionNumber': u'_IS_ABSENT_', u'/chapter/citation/book/imprint/imprintPublisher': u'Royal Institute of International Affairs FIX#17', u'/chapter/citation/book/pubDate/month': u'11 FIX#19', u'/chapter/metadataInfo/isbn': u'_IS_ABSENT_', u'/chapter/citation/book/author/aucomposed': u'Kenneth George Grubb', u'/chapter/citation/book/pubDate/composed': u'November, 1933 FIX#18', u'/chapter/metadataInfo/contentDate/contentComposed': u'November, 1933 FIX#32', u'_dom_name': u'cho_book_1933_grubb_000_0000', u'/chapter/citation/book/author/last': u'Grubb FIX#14', u'/chapter/metadataInfo/productContentType': u'Books FIX#39', u'/chapter/citation/book/editionStatement': u'_IS_ABSENT_', u'/chapter/citation/book/author/middle': u'George FIX#15', u'/chapter/metadataInfo/contentDate/contentDateEnd': u'1933-11-30 FIX#33', u'/chapter/citation/book/seriesGroup/seriesTitle': u'Information Department Papers FIX#27', u'/chapter/citation/book/publicationPlace/publicationPlaceCountry': u'UK FIX#25', u'/chapter/citation/book/author/first': u'Kenneth FIX#13', u'/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs FIX#40', u'/chapter/citation/book/publicationPlace/publicationPlaceCity': u'London FIX#23', u'/chapter/citation/book/author/@type': u'_IS_ABSENT_', u'/chapter/citation/book/pubDate/pubDateStart': u'1933-11-01 FIX#21', u'/chapter/metadataInfo/contentDate/contentMonth': u'11 FIX#36', u'/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House FIX#42', u'/chapter/citation/book/imprint/imprintFull': u'Royal Institute of International Affairs FIX#16'},
            ]

        expected_xml_fname = 'cho_book_1933_grubb_000_0000.xml.expected'

        self._assertEquals(original_xml_fname, possible_info_fixes, expected_xml_fname)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestViews),
    ])

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
