from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from project.cho.egest_adapter.doc.journal.article_journal import ArticleJournal
from project.cho.egest_adapter.doc.journal.page_journal import PageJournal
from project.cho.egest_adapter.doc.journal.parent_journal import ParentJournal


class TestJournal(TestDocumentHelper):
    def create_article(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_ARTICLE.xml' % dom_name)

        article_journal = self._create_document_instances('%s.xml' % dom_name, ArticleJournal, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(article_journal.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_page(self, dom_name, extra_args):
        expected_document_instances = self.source_xml('%s_PAGE.xml' % dom_name)

        page_journal = self._create_document_instances('%s.xml' % dom_name, PageJournal, extra_args)
        actual_xml_escaped = self._escape_create_document_instances(page_journal.document_instances())

        return expected_document_instances, actual_xml_escaped

    def create_parent(self, dom_name, extra_args, create_date='20121102'):
        expected_document_instances = self.source_xml('%s_PARENT.xml' % dom_name)

        parent_journal = self._create_document_instances('%s.xml' % dom_name, ParentJournal, extra_args, create_date)
        actual_xml_escaped = self._escape_create_document_instances(parent_journal.document_instances())

        return expected_document_instances, actual_xml_escaped
