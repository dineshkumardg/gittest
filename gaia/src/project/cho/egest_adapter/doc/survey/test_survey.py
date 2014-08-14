from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.survey.article_survey import ArticleSurvey
from project.cho.egest_adapter.doc.survey.page_survey import PageSurvey
from project.cho.egest_adapter.doc.survey.parent_survey import ParentSurvey


class TestSurvey(TestDocumentHelper):
    def create_article(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_survey = self._create_document_instances('%s.xml' % dom_name, ArticleSurvey, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(article_survey.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_survey = self._create_document_instances('%s.xml' % dom_name, PageSurvey, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(page_survey.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_parent(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_survey = self._create_document_instances('%s.xml' % dom_name, ParentSurvey, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(parent_survey.document_instances())

        return expected_document_instances, actual_xml_escaped
