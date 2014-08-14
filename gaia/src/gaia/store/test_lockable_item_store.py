import os
import unittest
import time
from mock import patch
from testing.gaia_test import GaiaTest
from gaia.utils.lock import LockError
from gaia.store.lockable_item_store import LockableItemStore

@patch('gaia.log.log.Log.get_logger')
class TestLockableItemStore(GaiaTest):
    def test__init__OK(self, get_logger):
        item_store = LockableItemStore(self.test_dir, 10)

        self.assertEqual(10, item_store.lock_mins)

    def test_lock_SINGLE_ITEM_OK(self, get_logger):
        item_name = 'test_item'
        item_store = LockableItemStore(self.test_dir)
        item_store.lock(item_name)

        self.assertRaises(LockError, item_store.lock, item_name)

    def test_lock_MULTIPLE_ITEMS_OK(self, get_logger):
        item_name1 = 'item_1'
        item_name2 = 'item_2'

        item_store = LockableItemStore(self.test_dir)

        item_store.lock(item_name1)
        item_store.lock(item_name2)

        self.assertRaises(LockError, item_store.lock, item_name1)
        self.assertRaises(LockError, item_store.lock, item_name2)

    def test_lock_renew_SINGLE_ITEM(self, get_logger):
        item_name = 'test_item'

        item_store = LockableItemStore(self.test_dir)

        item_store.lock(item_name)
        time.sleep(1) # 1 second
        item_store.lock_renew(item_name)

        self.assertRaises(LockError, item_store.lock, item_name)
        
    def test_lock_renew_LOCK_DOES_NOT_EXIST(self, get_logger):
        item_name = 'test_item'

        item_store = LockableItemStore(self.test_dir)

        # This does nothing...
        item_store.lock_renew(item_name)

        try:
            item_store.lock(item_name)
        except LockError, e:
            self.fail('UNEXPECTED LockError: %s' % str(e))

    def test_lock_renew_MULTIPLE_ITEMS(self, get_logger):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        item_store = LockableItemStore(self.test_dir)

        item_store.lock(item_name1)
        item_store.lock(item_name2)

        time.sleep(1) # 1 second
        item_store.lock_renew(item_name1)
        item_store.lock_renew(item_name2)

        self.assertRaises(LockError, item_store.lock, item_name1)
        self.assertRaises(LockError, item_store.lock, item_name2)

    def test_lock_renew_NOT_LOCKED(self, get_logger):
        item_name = 'test_item'

        item_store = LockableItemStore(self.test_dir)
        item_store.lock_renew(item_name) # renewing an item that was not locked is safe and harmless

    def test_unlock_OK(self, get_logger):
        item_name = 'test_item'

        item_store = LockableItemStore(self.test_dir)
        item_store.lock(item_name)

        # Confirm the lock was acquired
        self.assertIn(item_name, item_store._locks.keys())

        item_store.unlock(item_name)

        self.assertNotIn(item_name, item_store._locks.keys())

    def test_unlock_MULTIPLE_LOCKS(self, get_logger):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        expected_lock_keys = ['test_item1', 'test_item2']

        item_store = LockableItemStore(self.test_dir)
        item_store.lock(item_name1)
        item_store.lock(item_name2)

        # Confirm the locks were acquired
        self.assertListEqual(expected_lock_keys, item_store._locks.keys())

        item_store.unlock(item_name1)

        self.assertNotIn(item_name1, item_store._locks.keys())

        item_store.unlock(item_name2)

        self.assertNotIn(item_name2, item_store._locks.keys())

    def test_unlock_NOT_LOCKED(self, get_logger):
        item_name = 'test_item'

        item_store = LockableItemStore(self.test_dir)
        item_store.unlock(item_name) # unlocking an item that was not locked is safe and harmless
        
    def test__get_asset_fnames(self, get_logger):
        store_dir = os.path.join(self.test_dir, 'store_dir')
        os.mkdir(store_dir)
        fnames = ['test.xml', 'test2.jpg', 'test3.jpg', LockableItemStore._lock_fname]
        expected_fnames = ['test.xml', 'test2.jpg', 'test3.jpg']
        
        for fname in fnames:
            open(os.path.join(store_dir, fname), 'wb').close()
            
        lockable_item_store = LockableItemStore(store_dir)
        fnames = lockable_item_store._get_asset_fnames(store_dir)
        
        self.assertListEqual(sorted(expected_fnames), sorted(fnames))


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLockableItemStore),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
