import os
import unittest
from scripts.reports.module_2_content import module_2_content


class TestModule2Content(unittest.TestCase):
    def test_get_psmid_prefix(self):
        self.assertEqual('cho_book', module_2_content.get_psmid_prefix('cho_book_1980_archer_000_0000'))

    def test_get_details_from_book_or_report_pamphlet_and_briefing_paper(self):
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('cho_book'))
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('cho_chbp'))

        self.assertEqual('cho_chrx_1990_0025_000_0000|||J. P. Hayes|||Foreign Direct Investment: Will the Uruguay Round Make a Difference?|||1990\n',
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_chrx_1990_0025_000_0000', use_test_data=True))

        self.assertEqual('cho_rpax_1980_dafter_000_0000|||Ray Dafter|||North Sea Oil and Gas and British Foreign Policy|||1980\ncho_rpax_1980_dafter_000_0000|||Ian Davidson|||North Sea Oil and Gas and British Foreign Policy|||1980\n',
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_rpax_1980_dafter_000_0000', use_test_data=True))

    def test_get_details_from_meeting(self):
        self.assertEqual("cho_meet_2006_6871_000_0000|||Joaquim Chissano|||Chatham House Prizewinner's Address|||Monday, 16th October 2006\n",
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_meet_2006_6871_000_0000', use_test_data=True))

    def test_get_details_from_conference_series(self):
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('cho_bcrc'))
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('cho_iprx'))

        self.assertEqual('cho_conf_1988_0000_002_0000|||Conference Series|||1998\n',
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_conf_1988_0000_002_0000', use_test_data=True))

    def test_get_details_from_journal(self):
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('cho_binx'))

        self.assertEqual('cho_iaxx_1980_0056_000_0000|||56\n',
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_iaxx_1980_0056_000_0000', use_test_data=True))

        self.assertEqual('cho_wtxx_1980_0036_000_0000|||36\n',
                         module_2_content.get_xpath_values_from_fixed_psmid('cho_wtxx_1980_0036_000_0000', use_test_data=True))

    def test_get_xpath_values_from_fixed_psmid(self):
        self.assertEqual(None, module_2_content.get_xpath_values_from_fixed_psmid('unknown_psmid'))

    def test_get_fixed_xml(self):
        self.assertEquals(583646, len(module_2_content.get_fixed_xml_as_string_from_file('cho_chrx_1990_0025_000_0000', use_test_data=True)))

    def test_main(self):
        module_2_content.main()

if __name__ == '__main__':
    unittest.main()
