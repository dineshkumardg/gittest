from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.book.test_book import TestBook
from project.cho.egest_adapter.doc.book import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from qa.models import Language
from project.cho.egest_adapter.entity_reference import EntityReference


class TestParentBook(TestBook):
    def test_cho_book_1929_heald_000_0000(self):
        mcode = 'XXXX'
        dom_name = 'cho_book_1929_heald_000_0000'
        publication_title = 'A Directory of Societies and Organizations in Great Britain Concerned with the Study of International Affairs'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        for i in range(1, 77):
            language = Language(psmid=dom_name, article_id=i, lang='English')
            language.save()

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.cho_book_1929)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped.encode('utf-8'), 'notEqual')

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestParentBook),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
