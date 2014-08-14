import os
import shutil
import unittest
import time
from datetime import datetime, timedelta
from gaia.utils.lock import Lock
from gaia.utils.lock import LockError

class TestLockError(unittest.TestCase):
    # Some of the tests have unused variable warnings; these are necessary to ensure the class is tested correctly.

    def test__str__(self):
        expected_err_str = 'LockError: A problem'

        err_str = 'A problem'

        lock_err = LockError(err_str)

        self.assertEqual(expected_err_str, str(lock_err))

class TestLock(unittest.TestCase):

    def setUp(self):
        self.test_dir = os.path.join('/tmp', 'gaia_tests', 'gaia', 'utils', 'test_lock')
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir)

        os.makedirs(self.test_dir)

    def tearDown(self):
        shutil.rmtree(os.path.join('/tmp', 'gaia_tests'))

    def test__init__OK(self):
        expected_lock_period = timedelta(seconds=100)
        lock_fpath = os.path.join(self.test_dir, 'test.lock')
        lock = Lock(lock_fpath, 100)

        self.assertEqual(lock_fpath, lock.lock_fpath)
        self.assertEqual(expected_lock_period, lock.lock_period)

    def test_lock_OK(self):
        lock_fpath = os.path.join(self.test_dir, 'test.lock')

        # Acquire a lock
        lock = Lock(lock_fpath, 10)

        # Confirm the lock was successful
        self.assertRaises(LockError, Lock, lock_fpath, 10)

    def test_lock_BAD_PATH(self):
        lock_fpath = os.path.join(self.test_dir, 'BAD', 'test.lock')

        self.assertRaises(LockError, Lock, lock_fpath, 1)

    def test_lock_LOCKED_DIFF_LOCK_OBJS_different_files(self):
        lock1_fpath = os.path.join(self.test_dir, 'test1.lock')
        lock2_fpath = os.path.join(self.test_dir, 'test2.lock')

        # Acquire two different locks
        lock1 = Lock(lock1_fpath, 1)
        lock2 = Lock(lock2_fpath, 1)

        # Confirm both locks were successful
        self.assertRaises(LockError, Lock, lock1_fpath, 1)
        self.assertRaises(LockError, Lock, lock2_fpath, 1)

    def test_lock_LOCK_EXPIRY(self):
        ''' Combines tests for un-expired locks and expired locks '''
        lock_fpath = os.path.join(self.test_dir, 'test.lock')

        # Acquire lock; will succeed
        lock = Lock(lock_fpath, 5) # 5 second
        # Acquire lock; will fail because first lock hasn't expired
        self.assertRaises(LockError, Lock, lock_fpath, 5)

        time.sleep(10) # wait for first lock to expire

        # Acquire lock; will succeed because first lock HAS expired 
        lock2 = Lock(lock_fpath, 5)
        # Acquire lock; will fail because second lock hasn't expired
        self.assertRaises(LockError, Lock, lock_fpath, 5)

    def test_unlock_OK(self):
        lock_fpath = os.path.join(self.test_dir, 'test.lock')

        lock = Lock(lock_fpath, 1)

        lock.unlock()

        self.assertFalse(os.path.isfile(lock_fpath))

    def test_renew_OK(self):
        lock_fpath = os.path.join(self.test_dir, 'test.lock')
        lock = Lock(lock_fpath, 1)

        with open(lock_fpath, 'r') as pre_renew:
            lines = pre_renew.readlines()
            orig_ts = float(lines[0])
            original_lock_time = datetime.utcfromtimestamp(orig_ts)

        time.sleep(2) # Make sure there's a pause before renewing
        lock.renew()

        with open(lock_fpath, 'r') as post_renew:
            lines = post_renew.readlines()
            renewed_ts = float(lines[0])
            renewed_lock_time = datetime.utcfromtimestamp(renewed_ts)

        self.assertTrue(os.path.isfile(lock_fpath))
        self.assertLess(original_lock_time, renewed_lock_time)

    def test__expired_EXPIRED(self):
        lock_fpath = os.path.join(self.test_dir, 'test.lock')        
        
        lock = Lock(lock_fpath, 1)
        time.sleep(5)
        self.assertTrue(lock._is_expired())
        
    def test__expired_NOT_EXPIRED(self):
        lock_fpath = os.path.join(self.test_dir, 'test.lock')

        lock = Lock(lock_fpath, 10)
        self.assertFalse(lock._is_expired())


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLock),
    unittest.TestLoader().loadTestsFromTestCase(TestLockError),
    ])


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
