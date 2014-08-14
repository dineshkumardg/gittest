from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.report.mega_report import MegaReport
from project.cho.egest_adapter.doc.report.page_report import PageReport
from project.cho.egest_adapter.entity_reference import EntityReference
from mock import Mock


class TestReport(TestDocumentHelper):
    def create_mega(self, dom_name, extra_args, mock_out_language_correction=['English']):
        expected_document_instances = self.source_xml('%s_MEGA.xml' % dom_name)

        mega_meeting = self._create_document_instances('%s.xml' % dom_name, MegaReport, extra_args)
        mega_meeting._language_correction = Mock(return_value=mock_out_language_correction)
        actual_xml_pretty_printed = mega_meeting.document_instances()[0]

        actual_xml_escaped = EntityReference.unescape(actual_xml_pretty_printed)

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_meeting = self._create_document_instances('%s.xml' % dom_name, PageReport, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(page_meeting.document_instances())

        return expected_document_instances, actual_xml_escaped
