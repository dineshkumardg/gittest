from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from StringIO import StringIO
from lxml import etree
from project.cho.egest_adapter.doc.report.test_report import TestReport
from project.cho.egest_adapter.doc.report import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.report.mega_report import MegaReport
from project.cho.egest_adapter.doc.document_error import SourceDataMissing,\
    DocumentError
from gaia.xml.cached_xml_dict import CachedXmlDict
from project.cho.egest_adapter.entity_reference import EntityReference


class TestMegaReport(TestReport):
    def test_cho_rpax_1998_negrine_000_0000(self):
        dom_name = 'cho_rpax_1998_negrine_000_0000'

        try:
            expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.cho_rpax_1998_negrine, mock_out_language_correction=['English'])
            self.fail("the ProductContentType is book but we're in a report - conversion should not happen")
        except UnboundLocalError:
            pass

    def test_cho_rpax_2006_allison_000_0000(self):
        dom_name = 'cho_rpax_2006_allison_000_0000'

        try:
            expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.cho_rpax_2006_allison, mock_out_language_correction=['English'])
        except DocumentError as e:
            pass
        except Exception as e:
            self.fail(e)

    def test_cho_rpax_1943_notes_000_0000(self):
        dom_name = 'cho_rpax_1943_notes_000_0000'

        expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.cho_rpax_1943, mock_out_language_correction=['English', 'French'])
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test_cho_rpax_1944_notes_000_0000(self):
        dom_name = 'cho_rpax_1944_notes_000_0000'

        expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.cho_rpax_1944)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test_cho_rpax_1953_0000_000_0000(self):
        # ensure meta:corporate-author present even if no other author element is available
        dom_name = 'cho_rpax_1953_0000_000_0000'

        expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.cho_rpax_1953)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test_cho_rpax_1956_0000_004_0000(self):  # CHOA-809
        # ensure meta.imprint_composed year does not display as 'None'

        # EXPECTATION: we should get an exception raised

        # TEST
        source_xml = '''<?xml version="1.0" encoding="utf-8"?>
<chapter xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" contentType="book" xsi:noNamespaceSchemaLocation="../../../gaia/config/dtds/chatham_house.xsd">
    <metadataInfo>
        <PSMID>cho_rpax_1956_0000_004_0000</PSMID>
        <productContentType>Pamphlets and Reports</productContentType>
    </metadataInfo>
    <citation>
        <book>
            <pubDate>
                <composed>February 1956</composed>
                <pubDateStart>1956-02-01</pubDateStart>
                <pubDateEnd>1956-02-29</pubDateEnd>
            </pubDate>
            <titleGroup>
                <fullTitle>The Baghdad Pact</fullTitle>
            </titleGroup>
            <imprint>
            <imprintFull>Royal Institute of International Affairs</imprintFull>
            <imprintPublisher>Royal Institute of International Affairs</imprintPublisher>
            </imprint>
            <publicationPlace>
            <publicationPlaceCity>London</publicationPlaceCity>
            <publicationPlaceCountry>UK</publicationPlaceCountry>
            <publicationPlaceComposed>London, UK</publicationPlaceComposed>
            </publicationPlace>
        </book>
    </citation>
</chapter>'''
        source_xml_dict = CachedXmlDict(etree.parse(StringIO(source_xml)))

        mega_report = MegaReport(self.config, source_xml_dict, extra_args=None)

        # ASSERTION
        self.assertRaises(SourceDataMissing, mega_report.meta_imprint)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestMegaReport),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
