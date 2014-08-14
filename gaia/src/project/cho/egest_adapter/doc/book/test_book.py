from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.book.article_book import ArticleBook
from project.cho.egest_adapter.doc.book.page_book import PageBook
from project.cho.egest_adapter.doc.book.parent_book import ParentBook


class TestBook(TestDocumentHelper):
    mcodes = {'cho_book_1929_heald_000_0000': 'XXXX', }

    def create_article(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_book = self._create_document_instances('%s.xml' % dom_name, ArticleBook, extra_args)
        # patch in only mcodes required for unit tests in Articlebook
        article_book.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(article_book.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_book = self._create_document_instances('%s.xml' % dom_name, PageBook, extra_args)
        # patch in only mcodes required for unit tests in Pagebook
        page_book.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(page_book.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_parent(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_book = self._create_document_instances('%s.xml' % dom_name, ParentBook, extra_args)
        # patch in only mcodes required for unit tests in ParentBook
        parent_book.mcodes = self.mcodes
        actual_xml_escaped = self._escape_create_document_instances(parent_book.document_instances())

        return expected_document_instances, actual_xml_escaped
