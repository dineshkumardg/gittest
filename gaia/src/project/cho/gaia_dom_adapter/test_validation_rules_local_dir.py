import unittest
import os
import glob
from testing.gaia_test import GaiaTest
from lxml import etree
from StringIO import StringIO
from project.cho.gaia_dom_adapter.validation_rules import ValidationRules


#
# export PYTHONPATH=$HOME/GTI_REPOS/gaia/src
# py -m unittest test_validation_rules_local_dir
# py test_validation_rules_local_dir.py > test_validation_rules_local_dir.log
# 
class TestValidationRulesLocalDir(GaiaTest):
    def _get_xml(self, filename):
        xml_src = open(os.path.join(os.path.dirname(__file__), '%s' % filename)).read()
        xml_tree = etree.parse(StringIO(xml_src))
        return xml_tree

    LOCAL_DIR = '/home/jsears/Desktop/all_cho_xml/tmp'

    def test_report_are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(self):
        print 'test_report_are_chapter_page_article_text_textclip_articlepage_pgrefs_unique'
        # copy all prod xml (but overwrites latest?)
        # find /mnt/nfs/gaia/web_root -type f -name '*.xml' -print -exec cp {} . \;

        # filter out m2 stuff
        # find /mnt/nfs/gaia/outbox -type f -name '*.xml' -newermt 2013-12-17 -exec cp -p {} . \;
        # or
        # ls | egrep '^cho_[a-z]{4}_(198|199|20).*$'| xargs -I{} mv {} m2

        xml_test_filenames = sorted(glob.glob('/%s/*.xml' % self.LOCAL_DIR))
        validation_rules = ValidationRules()
        for xml_test_filename in xml_test_filenames:
            xml_tree = self._get_xml(xml_test_filename)
            validation_rules.are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(xml_tree, _print=True)

    def test_report_are_chapter_page_article_clip_pgrefs_unique(self):
        print 'test_report_are_chapter_page_article_clip_pgrefs_unique'

        xml_test_filenames = sorted(glob.glob('/%s/*.xml' % self.LOCAL_DIR))
        validation_rules = ValidationRules()
        for xml_test_filename in xml_test_filenames:
            xml_tree = self._get_xml(xml_test_filename)
            validation_rules.are_chapter_page_article_clip_pgrefs_unique(xml_tree, _print=True)

    def test_report_are_clip_pgrefs_matching_articlepage_pgrefs(self):
        print 'test_report_are_clip_pgrefs_matching_articlepage_pgrefs'

        xml_test_filenames = sorted(glob.glob('/%s/*.xml' % self.LOCAL_DIR))
        validation_rules = ValidationRules()
        for xml_test_filename in xml_test_filenames:
            xml_tree = self._get_xml(xml_test_filename)
            validation_rules.are_clip_pgrefs_matching_articlepage_pgrefs(xml_tree, _print=True)

    def test_report_are_illustration_pgrefs_matching_clip_pgrefs(self):
        print 'test_report_are_illustration_pgrefs_matching_clip_pgrefs'

        xml_test_filenames = sorted(glob.glob('/%s/*.xmlpy test_validation_rules_local_dir.py > test_validation_rules_local_dir.log' % self.LOCAL_DIR))
        validation_rules = ValidationRules()
        for xml_test_filename in xml_test_filenames:
            xml_tree = self._get_xml(xml_test_filename)
            validation_rules.are_illustration_pgrefs_matching_clip_pgrefs(xml_tree, _print=True)

    def test_are_isbn_lengths_ok(self):
        print 'test_are_isbn_lengths_ok'

        xml_test_filenames = sorted(glob.glob('/%s/*.xml' % self.LOCAL_DIR))
        validation_rules = ValidationRules()
        for xml_test_filename in xml_test_filenames:
            print xml_test_filename
            xml_tree = self._get_xml(xml_test_filename)
            validation_rules.are_isbn_lengths_ok(xml_tree, _print=True)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestValidationRulesLocalDir),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
