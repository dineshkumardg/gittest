from testing.test_suite_common import TestSuiteCommon


import project.cho.egest_adapter.doc.report.test_mega_report
import project.cho.egest_adapter.doc.report.test_page_report
import project.cho.egest_adapter.doc.meeting.test_mega_meeting
import project.cho.egest_adapter.doc.meeting.test_page_meeting
import project.cho.egest_adapter.doc.conference_series.test_article_conference_series
import project.cho.egest_adapter.doc.conference_series.test_page_conference_series
import project.cho.egest_adapter.doc.conference_series.test_parent_conference_series
import project.cho.egest_adapter.doc.book.test_article_book
import project.cho.egest_adapter.doc.book.test_page_book
import project.cho.egest_adapter.doc.book.test_parent_book


class TestSuiteProjectDoc(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            project.cho.egest_adapter.doc.report.test_mega_report.suite,
            project.cho.egest_adapter.doc.report.test_page_report.suite,
            project.cho.egest_adapter.doc.meeting.test_mega_meeting.suite,
            project.cho.egest_adapter.doc.meeting.test_page_meeting.suite,
            project.cho.egest_adapter.doc.test_document.suite,
            project.cho.egest_adapter.doc.test_doc_factory.suite,
            project.cho.egest_adapter.doc.conference_series.test_article_conference_series.suite,
            project.cho.egest_adapter.doc.conference_series.test_page_conference_series.suite,
            project.cho.egest_adapter.doc.conference_series.test_parent_conference_series.suite,
            project.cho.egest_adapter.doc.book.test_article_book.suite,
            project.cho.egest_adapter.doc.book.test_page_book.suite,
            project.cho.egest_adapter.doc.book.test_parent_book.suite,
            ]
