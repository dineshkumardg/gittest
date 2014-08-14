import unittest
from cStringIO import StringIO
from coverage import coverage


class Coverage:
    def start(self):
        self.coverage = coverage(source=['project.cho.egest_adapter.doc'],
                                 omit=['*__init__*', '*/__init__*', '*/test_*'])
        self.coverage.use_cache(False)
        self.coverage.start()

    def stop(self):
        self.coverage.stop()

        output = StringIO()
        self.coverage.report(file=output)
        results = output.getvalue()

        print results


def run_unit_tests():
    output = StringIO()
    unittest.TextTestRunner(stream=output, verbosity=2).run(all_tests)
    results = output.getvalue()
    print results
    gaia_summary = results.split('\n')[-4:]
    return gaia_summary


gaia_coverage = Coverage()
gaia_coverage.start()

#find . -name test_\*.py

import project.cho.egest_adapter.doc.book.test_page_book
import project.cho.egest_adapter.doc.book.test_parent_book
import project.cho.egest_adapter.doc.conference_series.test_article_conference_series
import project.cho.egest_adapter.doc.conference_series.test_page_conference_series
import project.cho.egest_adapter.doc.conference_series.test_parent_conference_series
import project.cho.egest_adapter.doc.journal.test_article_journal
import project.cho.egest_adapter.doc.journal.test_page_journal
import project.cho.egest_adapter.doc.journal.test_parent_journal
import project.cho.egest_adapter.doc.meeting.test_mega_meeting
import project.cho.egest_adapter.doc.meeting.test_page_meeting
import project.cho.egest_adapter.doc.refugee_survey.test_article_refugee_survey
import project.cho.egest_adapter.doc.refugee_survey.test_page_refugee_survey
import project.cho.egest_adapter.doc.refugee_survey.test_parent_refugee_survey
import project.cho.egest_adapter.doc.report.test_mega_report
import project.cho.egest_adapter.doc.report.test_page_report
import project.cho.egest_adapter.doc.review_foreign_press.test_article_review_foreign_press
import project.cho.egest_adapter.doc.review_foreign_press.test_page_review_foreign_press
import project.cho.egest_adapter.doc.review_foreign_press.test_parent_review_foreign_press
import project.cho.egest_adapter.doc.survey.test_article_survey
import project.cho.egest_adapter.doc.survey.test_page_survey
import project.cho.egest_adapter.doc.survey.test_parent_survey


all_tests = unittest.TestSuite([
    project.cho.egest_adapter.doc.book.test_page_book.suite,
    project.cho.egest_adapter.doc.book.test_parent_book.suite,
    project.cho.egest_adapter.doc.conference_series.test_article_conference_series.suite,
    project.cho.egest_adapter.doc.conference_series.test_page_conference_series.suite,
    project.cho.egest_adapter.doc.conference_series.test_parent_conference_series.suite,
    project.cho.egest_adapter.doc.journal.test_article_journal.suite,
    project.cho.egest_adapter.doc.journal.test_page_journal.suite,
    project.cho.egest_adapter.doc.journal.test_parent_journal.suite,
    project.cho.egest_adapter.doc.meeting.test_mega_meeting.suite,
    project.cho.egest_adapter.doc.meeting.test_page_meeting.suite,
    project.cho.egest_adapter.doc.refugee_survey.test_article_refugee_survey.suite,
    project.cho.egest_adapter.doc.refugee_survey.test_page_refugee_survey.suite,
    project.cho.egest_adapter.doc.refugee_survey.test_parent_refugee_survey.suite,
    project.cho.egest_adapter.doc.report.test_mega_report.suite,
    project.cho.egest_adapter.doc.report.test_page_report.suite,
    project.cho.egest_adapter.doc.review_foreign_press.test_article_review_foreign_press.suite,
    project.cho.egest_adapter.doc.review_foreign_press.test_page_review_foreign_press.suite,
    project.cho.egest_adapter.doc.review_foreign_press.test_parent_review_foreign_press.suite,
    project.cho.egest_adapter.doc.survey.test_article_survey.suite,
    project.cho.egest_adapter.doc.survey.test_page_survey.suite,
    project.cho.egest_adapter.doc.survey.test_parent_survey.suite,
    ])

summary = run_unit_tests()
gaia_coverage.stop()
