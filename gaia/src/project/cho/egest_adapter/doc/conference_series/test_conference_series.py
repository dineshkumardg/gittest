from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.conference_series.article_conference_series import ArticleConferenceSeries
from project.cho.egest_adapter.doc.conference_series.parent_conference_series import ParentConferenceSeries
from project.cho.egest_adapter.doc.conference_series.page_conference_series import PageConferenceSeries
from project.cho.egest_adapter.entity_reference import EntityReference
from mock import Mock


class TestConferenceSeries(TestDocumentHelper):
    def create_parent(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_conference = self._create_document_instances('%s.xml' % dom_name, ParentConferenceSeries, extra_args)
        parent_conference._language_correction = Mock(return_value=['English'])
        actual_xml_pretty_printed = parent_conference.document_instances()[0]
        actual_xml_escaped = EntityReference.unescape(actual_xml_pretty_printed)

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_conference_series = self._create_document_instances('%s.xml' % dom_name, PageConferenceSeries, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(page_conference_series.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_article(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_conference = self._create_document_instances('%s.xml' % dom_name, ArticleConferenceSeries, extra_args)
        article_conference._article_language_correction = Mock(return_value='English')  # mock it out as test data not in the language .csv

        actual_xml_escaped = self._escape_create_document_instances(article_conference.document_instances())

        return expected_document_instances, actual_xml_escaped
