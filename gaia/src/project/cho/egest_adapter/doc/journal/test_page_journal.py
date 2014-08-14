from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.journal.test_journal import TestJournal
from project.cho.egest_adapter.doc.journal import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.entity_reference import EntityReference


class TestPageJournal(TestJournal):
    def test_cho_iaxx_1926_0005_000_0000(self):
        mcode = '5WWU'
        dom_name = 'cho_iaxx_1926_0005_000_0000'
        publication_title = 'A Directory of Societies and Organizations in Great Britain Concerned with the Study of International Affairs'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_page(dom_name, test_extra_args.cho_iaxx_1926_0005)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PAGE-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PAGE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestPageJournal),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
