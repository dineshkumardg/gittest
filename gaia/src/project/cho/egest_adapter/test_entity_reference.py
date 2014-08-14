# coding: utf-8

import os
import unittest
from project.cho.egest_adapter.entity_reference import EntityReference
from testing.gaia_test import GaiaTest


class TestEntityReference(GaiaTest):
    def test__escape_for_lst_platform_one_line_at_a_time(self):
        expected = u'Soviet Union’s Chemical Industry'
        actual = EntityReference._escape_for_lst_platform('Soviet Union&#8217;s Chemical Industry')
        self.assertEqual(expected, actual)

        expected = u'Factors Underlying British Foreign Policy Today – Iv'
        actual = EntityReference._escape_for_lst_platform('Factors Underlying British Foreign Policy Today &#8211; Iv')
        self.assertEqual(expected, actual)

        expected = u'Dr. W. W. Schütz'
        actual = EntityReference._escape_for_lst_platform('Dr. W. W. Sch&#252;tz')
        self.assertEqual(expected, actual)

        expected = u'André'
        actual = EntityReference._escape_for_lst_platform('Andr&#233;')
        self.assertEqual(expected, actual)

        expected = u'Günter'
        actual = EntityReference._escape_for_lst_platform('G&#252;nter')
        self.assertEqual(expected, actual)

    def test_choa_1286(self):
        escaped_htc_value = EntityReference.escape('AV&#228;ant Pharmaceuticals')  # <title>AV&#228;ant Pharmaceuticals</title> in JIRA
        unescaped_htc_value = EntityReference.unescape(escaped_htc_value)
        escaped_for_lst = EntityReference._escape_for_lst_platform(unescaped_htc_value)
        actual = EntityReference.strip_out_various_entities(escaped_for_lst)
        self.assertEqual(u'AVäant Pharmaceuticals', actual)

        escaped_htc_value = EntityReference.escape('AV&#x00E4; Ant Pharmaceuticals')  # <title>AV&#x00E4; Ant Pharmaceuticals</title> in HTC (JIRA not 100% accurate)
        unescaped_htc_value = EntityReference.unescape(escaped_htc_value)
        escaped_for_lst = EntityReference._escape_for_lst_platform(unescaped_htc_value)
        actual = EntityReference.strip_out_various_entities(escaped_for_lst)
        self.assertEqual(u'AVä Ant Pharmaceuticals', actual)

    def test_escape(self):
        htc_data = '&#x00BB;uu&amp;# &amp# a'
        unescaped_htc_value = EntityReference.unescape(htc_data)
        escaped_for_lst = EntityReference._escape_for_lst_platform(unescaped_htc_value)
        actual = EntityReference.strip_out_various_entities(escaped_for_lst)
        self.assertEqual(u'»uu&amp;# &amp# a', actual)

    def test_prepare_for_lst(self):
        self._assert_equal('cho_book_1929_heald_000_0000_ARTICLE')  # expected gift from choaEntityConversion.pl

    def test_prepare_for_lst_data_services_examples_article(self):
        self._assert_equal('cho_iaxx_1926_0005_000_0000_ARTICLE')  # expected gift from choaEntityConversion.pl

    def test_prepare_for_lst_data_services_examples_page(self):
        self._assert_equal('cho_iaxx_1926_0005_000_0000_PAGE')  # expected gift from choaEntityConversion.pl

    def test_prepare_for_lst_data_services_examples_parent(self):
        # expected gift from choaEntityConversion.pl BUT manually fixed to cover photon defect, after showing to SH
        self._assert_equal('cho_iaxx_1926_0005_000_0000_PARENT')

    def _assert_equal(self, psmid):
        expected_gift_run_through_choaEntityConversion_pl = open(os.path.join(os.path.dirname(__file__), 'test_data/%s-expected.xml' % psmid)).read()

        raw_gift_not_prepared_for_lst = open(os.path.join(os.path.dirname(__file__), 'test_data/%s-raw.xml' % psmid)).read()
        actual_gift_prepared_for_lst = EntityReference.prepare_for_lst(raw_gift_not_prepared_for_lst)
        actual_gift_prepared_for_lst = '<?xml version="1.0" encoding="UTF-8"?>\n' + actual_gift_prepared_for_lst.encode('utf-8')

        try:
            self.assertEqual(expected_gift_run_through_choaEntityConversion_pl, actual_gift_prepared_for_lst, 'not equal')
        except AssertionError as e:
            #self._dump_to_file('%s-actual.xml' % psmid, actual_gift_prepared_for_lst)
            raise e

    def _dump_to_file(self, fname, content):
        fpath = os.path.join(os.path.dirname(__file__), 'test_data/,%s' % fname)
        f = open(fpath, 'w')
        f.write(content.encode('utf-8'))
        f.close()

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestEntityReference),
    ])

if __name__ == '__main__':
    import testing
    testing.main(suite)
