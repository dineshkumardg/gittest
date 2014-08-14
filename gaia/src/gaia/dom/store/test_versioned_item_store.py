import os
import unittest
from testing.gaia_test import GaiaTest
from gaia.store.store_error import StoreError
from gaia.dom.store.versioned_item_store import VersionedItemStore
from gaia.asset.asset import Asset
from mock import patch, create_autospec
from gaia.dom.model.item import Item

class TestVersionedItemStore(GaiaTest):
    
    def setUp(self):
        GaiaTest.setUp(self)
        self.src_dir = os.path.join(self.test_dir, 'src')
        self.store_dir = os.path.join(self.test_dir, 'store')
        os.mkdir(self.src_dir)
        os.mkdir(self.store_dir)
        self.version_id = '27'

        asset_fpath = os.path.join(self.test_dir, 'asset1.xml')
        self.item_name = 'an_item_1'
        self.asset = Asset(asset_fpath, 'wb')
        self.asset.close()
        
    @patch('gaia.log.log.Log.get_logger')
    def test__init__(self, get_logger):
        root_dir = os.path.join(self.test_dir, 'WILL_BE_CREATED')
        self.assertFalse(os.path.exists(root_dir))
        VersionedItemStore(root_dir)
        self.assertTrue(os.path.exists(root_dir))
    
    @patch('gaia.log.log.Log.get_logger')
    def test_add_item(self, get_logger):
        # Set up
        asset_fnames = [ 'file1.xml',
                         'file2.jpg',
                         'file3.mp3',
                         'file4.tif', ]
        
        assets = []
        for fname in asset_fnames:
            asset = Asset(os.path.join(self.src_dir, fname), 'wb')
            asset.close()
            assets.append(asset)
        
        item = create_autospec(Item, instance=True)
        item.dom_id = 'ITEM_NAME'
        item.assets = assets
        
        # Expectations
        expected_fpaths = [os.path.join(self.store_dir, item.dom_id, self.version_id, fname) for fname in asset_fnames]
        
        # Test
        item_store = VersionedItemStore(self.store_dir)
        item_store.add_item(item, self.version_id)
        
        actual_paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.store_dir):
            for filename in filenames:
                actual_paths.append(os.path.join(dirpath, filename))
                
        # Assertions
        self.assertListEqual(sorted(expected_fpaths), sorted(actual_paths))
        
    @patch('gaia.log.log.Log.get_logger')
    def test_add_and_get_assets(self, get_logger):
        item_name = 'ITEM_NAME'
        asset_fpaths = []
        expected_fpaths = []

        item_store = VersionedItemStore(self.store_dir)

        for i in range(0, 3):
            fname = 'TEST_ASSET_%d.jpg' % i
            asset_fpath = os.path.join(self.src_dir, fname)
            asset_fpaths.append(asset_fpath)
            asset = Asset(asset_fpath, 'wb')
            asset.close()
            expected_fpaths.append(os.path.join(self.store_dir, item_name, self.version_id, fname))

            item_store.add_asset(asset, item_name, self.version_id)

            assets = item_store.assets(item_name, self.version_id)
            self.assertEqual(i+1, len(assets))

            for asset in assets:
                self.assertIsInstance(asset, Asset)
        
            asset_fpaths = [asset.fpath for asset in assets]
            self.assertEqual(set(expected_fpaths), set(asset_fpaths))

    @patch('shutil.copy')
    @patch('gaia.log.log.Log.get_logger')
    def test_add_asset_RAISES(self, get_logger, copy):
        copy.side_effect = IOError('Euston, we have a problem')

        item_store = VersionedItemStore(self.store_dir)

        self.assertRaises(StoreError, item_store.add_asset, self.asset, 'a_name', self.version_id)

    @patch('gaia.log.log.Log.get_logger')
    def test_new_asset_NEW(self, get_logger):
        asset_fname = 'asset_name.xml'
        item_name = 'ITEM_NAME'
        expected_fpath = os.path.join(self.store_dir, item_name, self.version_id, asset_fname)

        item_store = VersionedItemStore(self.store_dir)
        asset = item_store.new_asset(asset_fname, item_name, self.version_id)
        self.assertTrue(isinstance(asset, Asset))
        
        assets = item_store.assets(item_name, self.version_id)
        
        self.assertEqual(1, len(assets))
        self.assertEqual(expected_fpath, assets[0].fpath)
        
    # Note: no delete functionality exists (yet?)
    #@patch('gaia.log.log.Log.get_logger')
    #def test_delete_asset(self, get_logger):
        ## Set up
#
        ##item_store = VersionedItemStore(self.store_dir)
        ##os.mkdir(os.path.join(self.store_dir, item_name))
#
        #item_store.add_asset(self.asset, self.item_name, self.version_id)
        #self.assertEqual(1, len(item_store.assets(self.item_name, self.version_id)))
        #
        ## Test
        #item_store.delete_asset(self.asset)
#
        ## Assertions
        #self.assertEqual(0, len(item_store.assets(self.item_name, self.version_id)))
        #
    @patch('gaia.log.log.Log.get_logger')
    def test__item_dir(self, get_logger):
        item_store = VersionedItemStore(self.test_dir)
        item_name = 'ITEM_NAME'
        
        expected_item_dir = os.path.join(self.test_dir, item_name, str(self.version_id))

        self.assertFalse(os.path.exists(expected_item_dir))
        
        item_dir = item_store._item_dir(item_name, self.version_id)
        
        self.assertTrue(os.path.exists(expected_item_dir))
        self.assertEqual(expected_item_dir, item_dir)
        
    @patch('gaia.log.log.Log.get_logger')
    def test__item_dir_WITH_EXTRA_ARGS(self, get_logger):
        item_store = VersionedItemStore(self.test_dir)
        item_name = 'ITEM_NAME'
        
        args = ['a', 'b', 'c', 12, 'd']
        expected_item_dir = os.path.join(self.test_dir, item_name, self.version_id, 'a/b/c/12/d')

        self.assertFalse(os.path.exists(expected_item_dir))
        
        item_dir = item_store._item_dir(item_name, self.version_id, *args)
        
        self.assertEqual(os.path.abspath(expected_item_dir), os.path.abspath(item_dir))
        self.assertTrue(os.path.exists(expected_item_dir))
        

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestVersionedItemStore),
    ])


if __name__ == '__main__':
    import testing
    testing.main(suite)
