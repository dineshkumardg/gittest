from testing.test_suite_common import TestSuiteCommon


import gaia.gift.gift25.test_essay
import gaia.gift.gift25.test_etoc
import gaia.gift.gift25.test_gift_doc
import gaia.gift.gift25.test_gold
import gaia.gift.gift25.test_hyphen_element_maker
import gaia.gift.gift25.test_media
import gaia.gift.gift25.test_meta
import gaia.gift.gift25.test_shared
import gaia.gift.gift25.test_vault_link
import project.cho.gaia_dom_adapter.test_factory
import project.cho.gaia_dom_adapter.test_validation_rules
import project.cho.gaia_dom_adapter.test_cho
import project.cho.gaia_dom_adapter.test_cho_conference_series
import project.cho.gaia_dom_adapter.test_cho_review_foreign_press
import project.cho.gaia_dom_adapter.test_cho_fix
import project.cho.gaia_dom_adapter.test_cho_survey
import project.cho.gaia_dom_adapter.test_cho_report
import project.cho.gaia_dom_adapter.test_cho_journal
import project.cho.gaia_dom_adapter.test_cho_meeting
import project.cho.gaia_dom_adapter.test_cho_book
import project.cho.gaia_dom_adapter.test_cho_refugee_survey
import project.cho.gaia_dom_adapter.test_validation_rules
import project.cho.egest_adapter.test_cho_namespaces
import project.cho.egest_adapter.test_language_correction
import project.cho.egest_adapter.test_entity_reference
import project.cho.egest_adapter.feed.test_feed_wrapper
import project.cho.egest_adapter.feed.test_feed_file
import project.cho.test_cho_content_type
import project.cho.test_hard_coded_mcodes
import project.stha.gaia_dom_adapter.test_factory
import project.stha.gaia_dom_adapter.test_stha
import test_utils.test_create_cho_xml


class TestSuiteProject(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            gaia.gift.gift25.test_essay.suite,
            gaia.gift.gift25.test_etoc.suite,
            gaia.gift.gift25.test_gift_doc.suite,
            gaia.gift.gift25.test_gold.suite,
            gaia.gift.gift25.test_hyphen_element_maker.suite,
            gaia.gift.gift25.test_media.suite,
            gaia.gift.gift25.test_meta.suite,
            gaia.gift.gift25.test_shared.suite,
            gaia.gift.gift25.test_vault_link.suite,
            project.cho.test_cho_content_type.suite,
            project.cho.test_hard_coded_mcodes.suite,
            project.cho.gaia_dom_adapter.test_factory.suite,
            project.cho.gaia_dom_adapter.test_validation_rules.suite,
            project.cho.gaia_dom_adapter.test_cho.suite,
            project.cho.gaia_dom_adapter.test_cho_conference_series.suite,
            project.cho.gaia_dom_adapter.test_cho_review_foreign_press.suite,
            project.cho.gaia_dom_adapter.test_cho_fix.suite,
            project.cho.gaia_dom_adapter.test_cho_survey.suite,
            project.cho.gaia_dom_adapter.test_cho_journal.suite,
            project.cho.gaia_dom_adapter.test_cho_report.suite,
            project.cho.gaia_dom_adapter.test_cho_meeting.suite,
            project.cho.gaia_dom_adapter.test_cho_book.suite,
            project.cho.gaia_dom_adapter.test_cho_refugee_survey.suite,
            project.cho.gaia_dom_adapter.test_validation_rules.suite,
            project.cho.egest_adapter.test_cho_namespaces.suite,
            project.cho.egest_adapter.test_language_correction.suite,
            project.cho.egest_adapter.test_entity_reference.suite,
            project.cho.egest_adapter.feed.test_feed_wrapper.suite,
            project.cho.egest_adapter.feed.test_feed_file.suite,
            project.stha.gaia_dom_adapter.test_factory.suite,
            project.stha.gaia_dom_adapter.test_stha.suite,
            test_utils.test_create_cho_xml.suite,
            ]
