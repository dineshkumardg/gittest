from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.report.test_report import TestReport
from project.cho.egest_adapter.doc.report import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.entity_reference import EntityReference


class TestPageReport(TestReport):
    def test_cho_rpax_1943_notes_000_0000(self):
        dom_name = 'cho_rpax_1943_notes_000_0000'

        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.cho_rpax_1943)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestPageReport),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
