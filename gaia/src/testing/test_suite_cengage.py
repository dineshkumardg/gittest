from testing.test_suite_common import TestSuiteCommon


import cengage.asset_id.test_models
import cengage.callisto.test_delivery_manifest
import cengage.callisto.test_image_manifest
import cengage.atlas.test_atlas


class TestSuiteCengage(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            cengage.atlas.test_atlas.suite,
            cengage.callisto.test_delivery_manifest.suite,
            cengage.callisto.test_image_manifest.suite,
            cengage.asset_id.test_models.suite,
        ]
