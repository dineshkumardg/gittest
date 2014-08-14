import os
import unittest
from datetime import timedelta
from test_utils.gaia_test import GaiaTest
from gaia.utils.lock import LockError
from gaia.ingest.worker_job_lock import WorkerJobLock

class _TestConfig:
    def __init__(self, test_dir):
        self.working_dir = test_dir

class TestWorkerJobLock(GaiaTest):

    def setUp(self):
        GaiaTest.setUp(self)
        self.config = _TestConfig(self.test_dir)

    def test__init__OK(self):
        expected_lock_period = timedelta(seconds=4*60*60)   # 4 hours
        expected_lock_fpath = os.path.join(self.test_dir, 'ingest_worker_job_item_1.lock')

        item_name = 'item_1'
        lock = WorkerJobLock(item_name, self.config)

        self.assertEqual(expected_lock_fpath, lock.lock_fpath)
        self.assertEqual(expected_lock_period, lock.lock_period)

    def test_lock(self):
        item_name = 'item_1'

        # Acquire a lock
        lock = WorkerJobLock(item_name, self.config)

        # Try to grab the lock again (should fail)
        self.assertRaises(LockError, WorkerJobLock, item_name, self.config)


    def test_unlock_OK(self):
        lock_fpath = os.path.join(self.test_dir, 'ingest_worker_job_item_1.lock')

        item_name = 'item_1'
        lock = WorkerJobLock(item_name, self.config)
        lock.unlock()

        self.assertFalse(os.path.isfile(lock_fpath))

        # check that we can make a new lock (ie unlock worked).
        lock = WorkerJobLock(item_name, self.config)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestWorkerJobLock),
    ])

if __name__ == "__main__":
    # This is handy while developing these tests..
    #import logging
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
