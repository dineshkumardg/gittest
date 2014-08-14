from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
import os
from StringIO import StringIO
from lxml import etree
from test_utils.create_cho_xml import CreateChoXML
from gaia.xml.cached_xml_dict import CachedXmlDict
from project.cho.egest_adapter.doc.meeting.test_meeting import TestMeeting
from project.cho.egest_adapter.entity_reference import EntityReference
from project.cho.egest_adapter.doc.meeting.mega_meeting import MegaMeeting
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.meeting import test_extra_args
from mock import Mock
from qa.models import Language


class TestMegaMeeting(TestMeeting):
    def test_cho_meet_1922_0000_000_0000_with_RELATED_DOCUMENT(self):
        # EXPECTATION / TEST
        dom_name = 'cho_meet_1922_0000_000_0000'
        expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.meet_1922_0000)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

    def test_cho_meet_1922_0010_000_0000(self):
        # EXPECTATION / TEST
        dom_name = 'cho_meet_1922_0010_000_0000'
        expected_document_instances, actual_xml_escaped = self.create_mega(dom_name, test_extra_args.meet_1922_0010)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

    def test_create_cho_xml_meet(self):
        # EXPECTATION
        expected_document_instances = self.source_xml('create_cho_xml_meet_MEGA.xml')

        # TEST
        # do a  py create_test_items.py  --num_pages=50 --img_file_ext='jpg' --item_type='meet' --num_items=1
        num_pages = 6
        img_file_ext = 'jpg'
        item_type = 'meet'
        item_num = 1
        item_name_stem = 'cho_meet_2013_0000_000'
        fpath_xsd = os.path.join(os.path.dirname(__file__), '../../../../../gaia/config/dtds/chatham_house.xsd')
        xml = CreateChoXML.create_xml_asset(num_pages, img_file_ext, item_type, item_num, item_name_stem, fpath_xsd)

        source_xml_dict = CachedXmlDict(etree.parse(StringIO(xml)))

        mega_meeting = MegaMeeting(self.config, source_xml_dict, test_extra_args.meet_create_cho_xml)
        # patch out the Original
        mega_meeting.creation_date = Mock(return_value='20121202')
        mega_meeting._language_correction = Mock(return_value=['English'])

        actual_xml_pretty_printed = mega_meeting.document_instances()[0]
        actual_xml_escaped = EntityReference.unescape(actual_xml_pretty_printed)
        actual_xml_without_ns = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
        self.assertEqual(expected_document_instances, actual_xml_without_ns, 'notEqual')

    def test_cho_meet_1949_1724_000_0000(self):  # no mocking of language
        # regression test for: http://jira.cengage.com/browse/CHOA-1064

        # EXPECTATION
        dom_name = 'cho_meet_1949_1724_000_0000'
        expected_document_instances = self.source_xml('%s_MEGA.xml' % dom_name)

        # TEST
        language = Language(psmid=dom_name, article_id='1', lang='French')
        language.save()

        mega_meeting = self._create_document_instances('%s.xml' % dom_name, MegaMeeting, test_extra_args.meet_1949_1724)
        actual_xml_pretty_printed = mega_meeting.document_instances()[0]
        actual_xml_without_ns = ChoNamespaces.remove_ns(actual_xml_pretty_printed)
        actual_xml_escaped = EntityReference.unescape(actual_xml_without_ns)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

    def test_cho_meet_1972_3498_000_0000(self):  # no mocking of language
        # regression test for: http://jira.cengage.com/browse/CHOA-1064

        # EXPECTATION
        dom_name = 'cho_meet_1972_3498_000_0000'
        expected_document_instances = self.source_xml('%s_MEGA.xml' % dom_name)

        # TEST
        language = Language(psmid=dom_name, article_id='1', lang='Spanish')
        language.save()

        mega_meeting = self._create_document_instances('%s.xml' % dom_name, MegaMeeting, test_extra_args.meet_1972_3498)
        actual_xml_pretty_printed = mega_meeting.document_instances()[0]
        actual_xml_without_ns = ChoNamespaces.remove_ns(actual_xml_pretty_printed)
        actual_xml_escaped = EntityReference.unescape(actual_xml_without_ns)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_MEGA-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_MEGA-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestMegaMeeting),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
