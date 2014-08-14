import unittest
import os
import glob
from testing.gaia_test import GaiaTest
from lxml import etree
from StringIO import StringIO
from project.cho.gaia_dom_adapter.validation_rules import ValidationRules


class TestValidationRules(GaiaTest):
    def _get_xml(self, filename):
        xml_src = open(os.path.join(os.path.dirname(__file__), '%s' % filename)).read()
        xml_tree = etree.parse(StringIO(xml_src))
        return xml_tree

    def test_are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(self):
        xml_tree = self._get_xml('%s/../test_samples/cho_rfpx_1940C_0000_049_0000.xml' % os.path.dirname(__file__))  # http://jira.cengage.com/browse/EG-493
        #xml_tree = self._get_xml('/home/jsears/Desktop/cho_byil_1938_0019_000_0000/cho_byil_1938_0019_000_0000.xml')  # CHOA-1121

        validation_rules = ValidationRules()
        validation_rules_passed = validation_rules.are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(xml_tree)

        self.assertFalse(validation_rules_passed)

    def test_are_chapter_page_article_clip_pgrefs_unique(self):
        xml_tree = self._get_xml('%s/../test_samples/cho_book_1939_Kuczynski_000_0000.xml' % os.path.dirname(__file__))  # http://jira.cengage.com/browse/EG-522

        validation_rules = ValidationRules()
        validation_rules_passed = validation_rules.are_chapter_page_article_clip_pgrefs_unique(xml_tree)

        self.assertFalse(validation_rules_passed)

    def test_bulk_are_articles_pgrefs_unique(self):
        xml_test_filenames = sorted(glob.glob('%s/../test_samples/*.xml' % os.path.dirname(__file__)))
        validation_rules = ValidationRules()

        fail_count = 0
        for xml_test_filename in xml_test_filenames:
            xml_tree = self._get_xml(xml_test_filename)
            if validation_rules.are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(xml_tree) == False:
                fail_count += 1

        self.assertEqual(44, fail_count)

    def test_are_clip_pgrefs_matching_articlepage_pgrefs(self):
        xml_tree = self._get_xml('%s/../test_samples/cho_book_1939_Kuczynski_000_0000.xml' % os.path.dirname(__file__))  # http://jira.cengage.com/browse/EG-523

        validation_rules = ValidationRules()
        validation_rules_passed = validation_rules.are_clip_pgrefs_matching_articlepage_pgrefs(xml_tree)

        self.assertFalse(validation_rules_passed)

    def test_are_illustration_pgrefs_matching_clip_pgrefs(self):
        xml_tree = self._get_xml('%s/../test_samples/cho_binx_1939_0016_002_0000.xml' % os.path.dirname(__file__))  # http://jira.cengage.com/browse/EG-527

        validation_rules = ValidationRules()
        validation_rules_passed = validation_rules.are_illustration_pgrefs_matching_clip_pgrefs(xml_tree)

        self.assertFalse(validation_rules_passed)

    def test_are_isbn_lengths_ok(self):
        validation_rules = ValidationRules()
        xml_tree = self._get_xml('%s/../test_samples/cho_book_2005_keating_000_0000.xml' % os.path.dirname(__file__))  # http://jira.cengage.com/browse/EG-533
        validation_rules_passed = validation_rules.are_isbn_lengths_ok(xml_tree)
        self.assertFalse(validation_rules_passed)

        validation_rules = ValidationRules()
        xml_tree = self._get_xml('%s/../test_samples/cho_bcrc_1938_cleeve_001_0000.xml' % os.path.dirname(__file__))
        validation_rules_passed = validation_rules.are_isbn_lengths_ok(xml_tree)
        self.assertTrue(validation_rules_passed)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestValidationRules),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
