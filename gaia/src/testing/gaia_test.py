import shutil
import tempfile
import logging
import unittest
from gaia.log.log import Log

class GaiaTest(unittest.TestCase):
    ''' A Base Class implementation to do common test setup for Gaia Tests.`
        Sets up Logging.

        Provides
            .config
            .test_dir
            .log_fname
            .log_fpath
    '''
    def __init__(self, *args, **kwargs): 
        unittest.TestCase.__init__(self, *args, **kwargs)

    def runTest(self, result=None):
        unittest.run(self, result)

    def setUp(self, config=None):
        unittest.TestCase.setUp(self)
        test_dir = tempfile.mkdtemp()  # this works best on Windows (with ignore errors in rmtree)

        if config:
            try:
                config.log_dir
            except AttributeError, e:
                config.log_dir =  test_dir

            try:
                config.log_level
            except AttributeError, e:
                config.log_level = logging.DEBUG

        else:# configure logging for basic test usage by default
            class Config:
                log_dir = test_dir
                log_level = logging.DEBUG
            config = Config()

        self.config = config
        self.test_dir = test_dir
        self.log_fname = ',unit_test' #?.
        self.log_fpath = Log.configure_logging(self.log_fname, self.config, multi_process=False, rollover=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        unittest.TestCase.tearDown(self)
