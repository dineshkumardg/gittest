from testing.test_suite_common import TestSuiteCommon  #, Config
#from gaia.log.log import Log


import qa.fix.test_fix_form
import qa.reject.test_reject_report
import qa.analyse.test_analyse_export_form
import qa.reject.test_reject_form
import qa.test_qa_link
import qa.test_qa_query
import qa.test_models
import qa.test_view_mixin
import qa.manage.test_manage_view
import qa.report.test_ingest_error
import qa.report.test_item_error
import qa.report.test_released_item
import qa.report.test_report_qa
import qa.report.test_feed_file_index
import qa.report.test_feed_file_items
import qa.test_item_views
import qa.test_mcode_view
import qa.templatetags.test_item_view_tags
import qa.ws.test_views


class TestSuiteQA(TestSuiteCommon):
    def __init__(self,):
        TestSuiteCommon.__init__(self)
#         self.log_fname = Log.configure_logging(',%s' % self.__class__.__name__, Config())
#         self.log = Log.get_logger(self)
#         self.log.info(...')

        self.standard_tests = [
            qa.fix.test_fix_form.suite,
            qa.reject.test_reject_report.suite,
            qa.analyse.test_analyse_export_form.suite,
            qa.reject.test_reject_form.suite,
            qa.test_qa_link.suite,
            qa.test_qa_query.suite,
            qa.test_models.suite,
            qa.test_view_mixin.suite,
            qa.manage.test_manage_view.suite,
            qa.report.test_ingest_error.suite,
            qa.report.test_item_error.suite,
            qa.report.test_released_item.suite,
            qa.report.test_report_qa.suite,
            qa.report.test_feed_file_index.suite,
            qa.report.test_feed_file_items.suite,
            qa.test_item_views.suite,
            qa.test_mcode_view.suite,
            qa.templatetags.test_item_view_tags.suite,
            qa.ws.test_views.suite,
        ]
