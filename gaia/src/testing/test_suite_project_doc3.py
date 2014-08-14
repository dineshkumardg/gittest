from testing.test_suite_common import TestSuiteCommon


import project.cho.egest_adapter.doc.survey.test_article_survey
import project.cho.egest_adapter.doc.survey.test_page_survey
import project.cho.egest_adapter.doc.survey.test_parent_survey


class TestSuiteProjectDoc3(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            project.cho.egest_adapter.doc.survey.test_article_survey.suite,
            project.cho.egest_adapter.doc.survey.test_page_survey.suite,
            project.cho.egest_adapter.doc.survey.test_parent_survey.suite,
            ]
