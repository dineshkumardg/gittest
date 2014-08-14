from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.refugee_survey.article_refugee_survey import ArticleRefugeeSurvey
from project.cho.egest_adapter.doc.refugee_survey.page_refugee_survey import PageRefugeeSurvey
from project.cho.egest_adapter.doc.refugee_survey.parent_refugee_survey import ParentRefugeeSurvey
from mock import Mock


class TestRefugeeSurvey(TestDocumentHelper):
    mcodes = {'cho_rsxx_1945_TEST_000_0000': 'XXXX'}
    creation_date = '20121202'  # as found in Data Services hand crafted gift

    def create_article(self, dom_name, extra_args, mock_langs=True):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_refugee_survey = self._create_document_instances('%s.xml' % dom_name, ArticleRefugeeSurvey, extra_args, self.creation_date)
        if mock_langs == True:
            article_refugee_survey._article_language_correction = Mock(return_value='English')  # mock it out as test data not in the language .csv
        article_refugee_survey.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(article_refugee_survey.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_refugee_survey = self._create_document_instances('%s.xml' % dom_name, PageRefugeeSurvey, extra_args, self.creation_date)
        page_refugee_survey.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(page_refugee_survey.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_parent(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_refugee_survey = self._create_document_instances('%s.xml' % dom_name, ParentRefugeeSurvey, extra_args, self.creation_date)
        parent_refugee_survey._language_correction = Mock(return_value=['English'])
        parent_refugee_survey.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(parent_refugee_survey.document_instances())

        return expected_document_instances, actual_xml_escaped
