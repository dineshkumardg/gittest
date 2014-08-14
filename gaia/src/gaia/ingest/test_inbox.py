import unittest
import time
from testing.gaia_test import GaiaTest
from gaia.utils.lock import LockError
from gaia.ingest.inbox import Inbox

class TestInbox(GaiaTest):
    def test__init__OK(self):
        inbox = Inbox(self.test_dir, 10)

        self.assertEqual(10, inbox.lock_mins)

    def test_lock_SINGLE_ITEM_OK(self):
        item_name = 'test_item'
        inbox = Inbox(self.test_dir)
        inbox.lock(item_name)

        self.assertRaises(LockError, inbox.lock, item_name)

    def test_lock_MULTIPLE_ITEMS_OK(self):
        item_name1 = 'item_1'
        item_name2 = 'item_2'

        inbox = Inbox(self.test_dir)

        inbox.lock(item_name1)
        inbox.lock(item_name2)

        self.assertRaises(LockError, inbox.lock, item_name1)
        self.assertRaises(LockError, inbox.lock, item_name2)

    def test_lock_renew_SINGLE_ITEM(self):
        item_name = 'test_item'

        inbox = Inbox(self.test_dir)

        inbox.lock(item_name)
        time.sleep(1) # 1 second
        inbox.lock_renew(item_name)

        self.assertRaises(LockError, inbox.lock, item_name)

    def test_lock_renew_MULTIPLE_ITEMS(self):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        inbox = Inbox(self.test_dir)

        inbox.lock(item_name1)
        inbox.lock(item_name2)

        time.sleep(1) # 1 second
        inbox.lock_renew(item_name1)
        inbox.lock_renew(item_name2)

        self.assertRaises(LockError, inbox.lock, item_name1)
        self.assertRaises(LockError, inbox.lock, item_name2)

    def test_lock_renew_NOT_LOCKED(self):
        item_name = 'test_item'

        inbox = Inbox(self.test_dir)
        inbox.lock_renew(item_name) # renewing an item that was not locked is safe and harmless

    def test_unlock_OK(self):
        item_name = 'test_item'

        inbox = Inbox(self.test_dir)
        inbox.lock(item_name)

        # Confirm the lock was acquired
        self.assertIn(item_name, inbox._locks.keys())

        inbox.unlock(item_name)

        self.assertNotIn(item_name, inbox._locks.keys())

    def test_unlock_MULTIPLE_LOCKS(self):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        expected_lock_keys = ['test_item1', 'test_item2']

        inbox = Inbox(self.test_dir)
        inbox.lock(item_name1)
        inbox.lock(item_name2)

        # Confirm the locks were acquired
        self.assertListEqual(expected_lock_keys, inbox._locks.keys())

        inbox.unlock(item_name1)

        self.assertNotIn(item_name1, inbox._locks.keys())

        inbox.unlock(item_name2)

        self.assertNotIn(item_name2, inbox._locks.keys())

    def test_unlock_NOT_LOCKED(self):
        item_name = 'test_item'

        inbox = Inbox(self.test_dir)
        inbox.unlock(item_name) # unlocking an item that was not locked is safe and harmless


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestInbox),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
