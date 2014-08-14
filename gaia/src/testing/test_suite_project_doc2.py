from testing.test_suite_common import TestSuiteCommon


import project.cho.egest_adapter.doc.review_foreign_press.test_article_review_foreign_press
import project.cho.egest_adapter.doc.review_foreign_press.test_page_review_foreign_press
import project.cho.egest_adapter.doc.review_foreign_press.test_parent_review_foreign_press
import project.cho.egest_adapter.doc.test_document_instances
import project.cho.egest_adapter.doc.test_document
import project.cho.egest_adapter.doc.test_doc_factory
import project.cho.egest_adapter.doc.journal.test_article_journal
import project.cho.egest_adapter.doc.journal.test_page_journal
import project.cho.egest_adapter.doc.journal.test_parent_journal
import project.cho.egest_adapter.doc.refugee_survey.test_article_refugee_survey
import project.cho.egest_adapter.doc.refugee_survey.test_page_refugee_survey
import project.cho.egest_adapter.doc.refugee_survey.test_parent_refugee_survey


class TestSuiteProjectDoc2(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            project.cho.egest_adapter.doc.review_foreign_press.test_article_review_foreign_press.suite,
            project.cho.egest_adapter.doc.review_foreign_press.test_page_review_foreign_press.suite,
            project.cho.egest_adapter.doc.review_foreign_press.test_parent_review_foreign_press.suite,
            project.cho.egest_adapter.doc.test_document_instances.suite,
            project.cho.egest_adapter.doc.test_document.suite,
            project.cho.egest_adapter.doc.test_doc_factory.suite,
            project.cho.egest_adapter.doc.journal.test_article_journal.suite,
            project.cho.egest_adapter.doc.journal.test_page_journal.suite,
            project.cho.egest_adapter.doc.journal.test_parent_journal.suite,
            project.cho.egest_adapter.doc.refugee_survey.test_article_refugee_survey.suite,
            project.cho.egest_adapter.doc.refugee_survey.test_page_refugee_survey.suite,
            project.cho.egest_adapter.doc.refugee_survey.test_parent_refugee_survey.suite,
            ]
