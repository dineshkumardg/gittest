import shutil
import tempfile
import logging
from gaia.log.log import Log
import os


class TestHelper:
    '''
    A class providing utility set up and tear down functions for tests
    
    GaiaTests use this to in their setUp and tearDown methods but these
    functions can also be used by _doctests_ by calling them directly.
    '''

    @classmethod
    def setUp(cls, output_dir=None):
        # create a test area for this test

        if output_dir is None:
            test_dir = tempfile.mkdtemp()  # this works best on Windows (with ignore errors in rmtree)
        else:
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            os.makedirs(output_dir)
            test_dir = output_dir

        # configure logging for basic test usage
        class Config:
            log_dir = test_dir
            log_level = logging.DEBUG
            CONFIG_NAME = 'UNIT_TEST'

        log_fname = 'test'
        config = Config()
        log_fpath = Log.configure_logging(log_fname, config, multi_process=False, rollover=False)

        return test_dir, log_fpath, log_fname, config


    @classmethod
    def tearDown(cls, test_dir):
        shutil.rmtree(test_dir, ignore_errors=True)
