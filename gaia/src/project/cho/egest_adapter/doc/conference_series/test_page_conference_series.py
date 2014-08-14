from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.conference_series.test_conference_series import TestConferenceSeries
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.conference_series import test_extra_args
from project.cho.egest_adapter.entity_reference import EntityReference


# Chatham House Conversion Spec v1.0 Issue-volume page record.xlsx
class TestPageConferenceSeries(TestConferenceSeries):
    def test_cho_iprx_1933_0001_001_0000(self):
        # EXPECTATION / TEST
        mcode = '4XJF'
        dom_name = 'cho_iprx_1933_0001_001_0000'
        publication_title = 'Institute of Pacific Relations 5th Conference, Banff, Alberta, Canada, 1933. Vol. 1: Central Secretariat Papers'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.bcrc_1933_0001)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test_cho_bcrc_1933_0001_000_0000(self):
        # Regression test from system tests for where - in meta_editors - there arn't any editors
        # EXPECTATION / TEST
        mcode = '4XFN'
        dom_name = 'cho_bcrc_1933_0001_000_0000'
        publication_title = 'British Commonwealth Relations 1st Conference, Toronto, Ontario, Canada, 1933. Verbatim Papers, vol. 1'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.bcrc_1933_0001)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestPageConferenceSeries),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
