import unittest
import time
from mock import patch
from testing.gaia_test import GaiaTest
from gaia.utils.lock import LockError
from gaia.dom.store.lockable_versioned_item_store import LockableVersionedItemStore
import os

@patch('gaia.log.log.Log.get_logger')
class TestLockableVersionedItemStore(GaiaTest):
    def setUp(self):
        GaiaTest.setUp(self)
        self.version_id = '27'

    def test__init__OK(self, get_logger):
        item_store = LockableVersionedItemStore(self.test_dir, 10)

        self.assertEqual(10, item_store.lock_mins)

    def test_lock_SINGLE_ITEM_OK(self, get_logger):
        item_name = 'test_item'
        item_store = LockableVersionedItemStore(self.test_dir)
        item_store.lock(item_name, self.version_id)

        self.assertRaises(LockError, item_store.lock, item_name, self.version_id)

    def test_lock_MULTIPLE_ITEMS_OK(self, get_logger):
        item_name1 = 'item_1'
        item_name2 = 'item_2'

        item_store = LockableVersionedItemStore(self.test_dir)

        item_store.lock(item_name1, self.version_id)
        item_store.lock(item_name2, self.version_id)

        self.assertRaises(LockError, item_store.lock, item_name1, self.version_id)
        self.assertRaises(LockError, item_store.lock, item_name2, self.version_id)

    def test_lock_renew_SINGLE_ITEM(self, get_logger):
        item_name = 'test_item'

        item_store = LockableVersionedItemStore(self.test_dir)

        item_store.lock(item_name, self.version_id)
        time.sleep(1) # 1 second
        item_store.lock_renew(item_name, self.version_id)

        self.assertRaises(LockError, item_store.lock, item_name, self.version_id)
        
    def test_lock_renew_LOCK_DOES_NOT_EXIST(self, get_logger):
        item_name = 'test_item'

        item_store = LockableVersionedItemStore(self.test_dir)

        # This does nothing...
        item_store.lock_renew(item_name, self.version_id)

        try:
            item_store.lock(item_name, self.version_id)
        except LockError, e:
            self.fail('UNEXPECTED LockError: %s' % str(e))

    def test_lock_renew_MULTIPLE_ITEMS(self, get_logger):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        item_store = LockableVersionedItemStore(self.test_dir)

        item_store.lock(item_name1, self.version_id)
        item_store.lock(item_name2, self.version_id)

        time.sleep(1) # 1 second
        item_store.lock_renew(item_name1, self.version_id)
        item_store.lock_renew(item_name2, self.version_id)

        self.assertRaises(LockError, item_store.lock, item_name1, self.version_id)
        self.assertRaises(LockError, item_store.lock, item_name2, self.version_id)

    def test_lock_renew_NOT_LOCKED(self, get_logger):
        item_name = 'test_item'

        item_store = LockableVersionedItemStore(self.test_dir)
        item_store.lock_renew(item_name, self.version_id) # renewing an item that was not locked is safe and harmless

    def test_unlock_OK(self, get_logger):
        item_name = 'test_item'

        item_store = LockableVersionedItemStore(self.test_dir)
        item_store.lock(item_name, self.version_id)

        # Confirm the lock was acquired
        self.assertIn(item_name + self.version_id, item_store._locks.keys())

        item_store.unlock(item_name, self.version_id)

        self.assertNotIn(item_name + self.version_id, item_store._locks.keys())

    def test_unlock_MULTIPLE_LOCKS(self, get_logger):
        item_name1 = 'test_item1'
        item_name2 = 'test_item2'

        expected_lock_keys = ['test_item127', 'test_item227']

        item_store = LockableVersionedItemStore(self.test_dir)
        item_store.lock(item_name1, self.version_id)
        item_store.lock(item_name2, self.version_id)

        # Confirm the locks were acquired
        self.assertListEqual(expected_lock_keys, item_store._locks.keys())

        item_store.unlock(item_name1, self.version_id)

        self.assertNotIn(item_name1, item_store._locks.keys())

        item_store.unlock(item_name2, self.version_id)

        self.assertNotIn(item_name2, item_store._locks.keys())

    def test_unlock_NOT_LOCKED(self, get_logger):
        item_name = 'test_item'

        item_store = LockableVersionedItemStore(self.test_dir)
        item_store.unlock(item_name, self.version_id) # unlocking an item that was not locked is safe and harmless
        
    def test__get_asset_fnames(self, get_logger):
        store_dir = os.path.join(self.test_dir, 'store_dir')
        os.mkdir(store_dir)
        fnames = ['test.xml', 'test2.jpg', 'test3.jpg', LockableVersionedItemStore._lock_fname]
        expected_fnames = ['test.xml', 'test2.jpg', 'test3.jpg']
        
        for fname in fnames:
            open(os.path.join(store_dir, fname), 'wb').close()
            
        lockable_item_store = LockableVersionedItemStore(store_dir)
        fnames = lockable_item_store._get_asset_fnames(store_dir)
        fnames.sort()
        
        self.assertListEqual(expected_fnames, fnames)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestLockableVersionedItemStore),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
