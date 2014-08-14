from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.review_foreign_press.test_review_foreign_press import TestReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.entity_reference import EntityReference


class TestParentReviewForeignPress(TestReviewForeignPress):
    def test_cho_rfpx_1939B_0000_001_0000(self):
        mcode = '5XHZ'
        dom_name = 'cho_rfpx_1939B_0000_001_0000'  # Special Publication: Journal
        publication_title = 'Review of the Foreign Press. Series B: European Neutrals and the Near East'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.cho_rfpx_1939B_0000)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
        #self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
        #self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestParentReviewForeignPress),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
