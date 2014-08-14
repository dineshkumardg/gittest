import unittest
from test_utils.test_helper import TestHelper

class GaiaTest(unittest.TestCase):
    ''' A Base Class implementation to do common test setup for Gaia Tests.`

        Creates self.test_dir for test methods
    '''

    def setUp(self):
        self.test_dir, self.log_fpath, self.log_fname, self.config = TestHelper.setUp()

    def tearDown(self):
        TestHelper.tearDown(self.test_dir)
