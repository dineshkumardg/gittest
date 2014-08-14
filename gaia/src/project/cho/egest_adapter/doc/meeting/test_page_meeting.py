from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.meeting.test_meeting import TestMeeting
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.meeting import test_extra_args
from project.cho.egest_adapter.entity_reference import EntityReference


class TestPageMeeting(TestMeeting):
    def test_cho_meet_1922_0010_000_0000(self):
        # EXPECTATION / TEST
        dom_name = 'cho_meet_1922_0010_000_0000'
        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.meet_1922_0010)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

    def test_cho_meet_1923_0015_000_0000(self):
        # Regression test for essay_p - no ocr words available on page

        # EXPECTATION / TEST
        dom_name = 'cho_meet_1923_0015_000_0000'
        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.meet_1923_0015)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestPageMeeting),
    ])

django_test.tearDown()

if __name__ == "__main__":
   import testing
   testing.main(suite)
