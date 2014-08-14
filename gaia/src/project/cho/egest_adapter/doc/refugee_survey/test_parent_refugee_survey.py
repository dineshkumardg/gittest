from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.refugee_survey.test_refugee_survey import TestRefugeeSurvey
from project.cho.egest_adapter.doc.refugee_survey import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.entity_reference import EntityReference


class TestParentRefugeeSurvey(TestRefugeeSurvey):
    def test_cho_rsxx_1945_TEST_000_0000(self):
        mcode = 'XXXX'
        dom_name = 'cho_rsxx_1945_TEST_000_0000'
        publication_title = 'test'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.cho_rsxx_1945_TEST)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
        #self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
        #self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestParentRefugeeSurvey),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
