from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.survey.test_survey import TestSurvey
from project.cho.egest_adapter.doc.survey import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.entity_reference import EntityReference


# cho_diax_1962_0000_000_0000 & cho_siax_1962_0000_000_0000 are a complete item (bi-directional relatedDocument)
class TestParentSurvey(TestSurvey):
    def test_cho_diax_1962_0000_000_0000(self):
        mcode = '5XHZ'
        dom_name = 'cho_diax_1962_0000_000_0000'
        publication_title = 'Documents on International Affairs 1962'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.cho_diax_1962)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test_cho_siax_1962_0000_000_0000(self):
        mcode = '5XKG'
        dom_name = 'cho_siax_1962_0000_000_0000'
        publication_title = 'Survey of International Affairs 1962'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.cho_siax_1962)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestParentSurvey),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
