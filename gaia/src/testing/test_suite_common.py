class Config:
    log_level = 10
    log_dir = '/tmp'


import unittest
from cStringIO import StringIO
from multiprocessing.process import Process
import multiprocessing


class TestSuiteCommon(Process):
    def __init__(self):
        Process.__init__(self)

        self.queue = None
        self.queue = multiprocessing.Queue()

        self.standard_tests = None
        self.standard_results = None

    def run(self):
        if self.standard_tests is not None:
            self.standard_results = self._standard_test_runner()

        self.queue.put({'standard_results': self.standard_results})

    def _standard_test_runner(self):
        test_suite = unittest.TestSuite(self.standard_tests)
        results = StringIO()
        unittest.TextTestRunner(stream=results, verbosity=0).run(test_suite)

        return results.getvalue()

    @classmethod
    def print_results(cls, standard_results):
        print '... %s ...' % cls.__name__
        print standard_results
