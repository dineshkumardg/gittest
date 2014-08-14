from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.review_foreign_press.article_review_foreign_press import ArticleReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press.page_review_foreign_press import PageReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press.parent_review_foreign_press import ParentReviewForeignPress


class TestReviewForeignPress(TestDocumentHelper):
    mcodes = {'cho_rfpx_1939B_0000_001_0000': '5XHZ'}

    def create_article(self, dom_name, extra_args, creation_date='20130403'):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_review_foreign_press = self._create_document_instances('%s.xml' % dom_name, ArticleReviewForeignPress, extra_args, creation_date)
        article_review_foreign_press.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(article_review_foreign_press.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args, creation_date='20130403'):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_review_foreign_press = self._create_document_instances('%s.xml' % dom_name, PageReviewForeignPress, extra_args, creation_date)
        page_review_foreign_press.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(page_review_foreign_press.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_parent(self, dom_name, extra_args, creation_date='20130403'):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_review_foreign_press = self._create_document_instances('%s.xml' % dom_name, ParentReviewForeignPress, extra_args, creation_date)
        parent_review_foreign_press.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(parent_review_foreign_press.document_instances())

        return expected_document_instances, actual_xml_escaped
