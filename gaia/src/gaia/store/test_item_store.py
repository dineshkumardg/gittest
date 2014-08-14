import os
import unittest
from testing.gaia_test import GaiaTest
from gaia.store.item_store import ItemStore
from gaia.store.store_error import StoreError
from gaia.asset.asset import Asset
from mock import patch, create_autospec
from gaia.dom.model.item import Item

class TestItemStore(GaiaTest):
    
    def setUp(self):
        GaiaTest.setUp(self)
        self.src_dir = os.path.join(self.test_dir, 'src')
        self.store_dir = os.path.join(self.test_dir, 'store')
        os.mkdir(self.src_dir)
        os.mkdir(self.store_dir)
        
    @patch('gaia.log.log.Log.get_logger')
    def test__init__(self, get_logger):
        root_dir = os.path.join(self.test_dir, 'WILL_BE_CREATED')
        self.assertFalse(os.path.exists(root_dir))
        ItemStore(root_dir)
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
        item.dom_name = 'ITEM_NAME'
        item.assets = assets
        
        # Expectations
        expected_fpaths = [os.path.join(self.store_dir, item.dom_name, fname) for fname in asset_fnames]
        expected_item_dir = os.path.join(self.store_dir, item.dom_name)
        
        # Test
        item_store = ItemStore(self.store_dir)
        item_store.add_item(item)
        
        actual_paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.store_dir):
            for filename in filenames:
                actual_paths.append(os.path.join(dirpath, filename))
                
        # Assertions
        self.assertListEqual(sorted(expected_fpaths), sorted(actual_paths))

        self.assertEqual(expected_item_dir, item_store.item_dir(item))

    @patch('gaia.log.log.Log.get_logger')
    def test_delete_item(self, get_logger):
        # Set up
        asset_fnames = [ 'file1.xml', 'file2.jpg', 'file3.mp3', 'file4.tif', ]
        assets = []
        for fname in asset_fnames:
            asset = Asset(os.path.join(self.src_dir, fname), 'wb')
            asset.close()
            assets.append(asset)
        
        item = create_autospec(Item, instance=True)
        item.dom_name = 'ITEM_NAME'
        item.assets = assets
        
        expected_fpaths = [os.path.join(self.store_dir, item.dom_name, fname) for fname in asset_fnames]
        
        item_store = ItemStore(self.store_dir)
        item_store.add_item(item)
        
        actual_paths = []
        for (dirpath, dirnames, filenames) in os.walk(self.store_dir):
            for filename in filenames:
                actual_paths.append(os.path.join(dirpath, filename))
                
        self.assertListEqual(sorted(expected_fpaths), sorted(actual_paths))
        
        # NOW TEST DELETE...
        item_store.delete_item(item)

        item_dir = os.path.join(self.store_dir, item.dom_name)
        self.assertFalse(os.path.exists(item_dir))

    @patch('gaia.log.log.Log.get_logger')
    def test_add_asset(self, get_logger):
        item_name = 'ITEM_NAME'
        fname = 'TEST_ASSET.jpg'
        asset_fpath = os.path.join(self.src_dir, fname)
        asset = Asset(asset_fpath, 'wb')
        asset.close()
        item_store = ItemStore(self.store_dir)

        expected_fpath = os.path.join(self.store_dir, item_name, fname)
        
        item_store.add_asset(asset, item_name)
        assets = item_store.assets(item_name)
        
        self.assertEqual(1, len(assets))
        self.assertEqual(expected_fpath, assets[0].fpath)

    @patch('shutil.copy')
    @patch('gaia.log.log.Log.get_logger')
    def test_add_asset_RAISES(self, get_logger, copy):
        copy.side_effect = IOError('Euston, we have a problem')
        item_name = 'ITEM_NAME'
        fname = 'TEST_ASSET.jpg'
        asset_fpath = os.path.join(self.src_dir, fname)
        asset = Asset(asset_fpath, 'wb')
        asset.close()
        item_store = ItemStore(self.store_dir)

        self.assertRaises(StoreError, item_store.add_asset, asset, item_name)

    @patch('gaia.log.log.Log.get_logger')
    def test_new_asset_NEW(self, get_logger):
        asset_fname = 'asset_name.xml'
        item_name = 'ITEM_NAME'
        item_store = ItemStore(self.store_dir)
        asset = item_store.new_asset(asset_fname, item_name)
        
        expected_fpath = os.path.join(self.store_dir, item_name, asset_fname)
        
        self.assertTrue(isinstance(asset, Asset))
        
        assets = item_store.assets(item_name)
        
        self.assertEqual(1, len(assets))
        self.assertEqual(expected_fpath, assets[0].fpath)
        
    @patch('gaia.log.log.Log.get_logger')
    def test_new_asset_ASSET_ALREADY_EXISTS(self, get_logger):
        # Set up
        asset_fname = 'asset_name.xml'
        item_name = 'ITEM_NAME'
        item_store = ItemStore(self.store_dir)
        os.mkdir(os.path.join(self.store_dir, item_name))
        
        asset_fpath = os.path.join(self.store_dir, item_name, asset_fname)

        f = open(asset_fpath, 'w')
        f.write('THIS SHOULD BE OVERWRITTEN')
        f.close()
        
        # Test
        asset = item_store.new_asset(asset_fname, item_name)

        # Expectations
        expected_content = ''
        
        # Get actual content
        f = open(asset_fpath, 'r')
        content = f.read()
        
        # Assertions
        self.assertTrue(isinstance(asset, Asset))
        
        assets = item_store.assets(item_name)
        
        self.assertEqual(1, len(assets))
        self.assertEqual(asset_fpath, assets[0].fpath)
        
        self.assertEqual(expected_content, content)
        
    @patch('gaia.log.log.Log.get_logger')
    def test_delete_asset(self, get_logger):
        # Set up
        asset_fname = 'asset_name.xml'
        item_name = 'ITEM_NAME'
        item_store = ItemStore(self.store_dir)
        os.mkdir(os.path.join(self.store_dir, item_name))
        
        asset_fpath = os.path.join(self.store_dir, item_name, asset_fname)
        asset = Asset(asset_fpath, 'wb')
        asset.close()
        
        self.assertEqual(1, len(item_store.assets(item_name)))
        self.assertTrue(os.path.exists(asset_fpath))
        
        # Test
        item_store.delete_asset(asset, item_name)

        # Assertions
        self.assertEqual(0, len(item_store.assets(item_name)))
        self.assertFalse(os.path.exists(asset_fpath))
        
    @patch('gaia.log.log.Log.get_logger')
    def test_assets(self, get_logger):
        item_name = 'ITEM_NAME'
        os.mkdir(os.path.join(self.store_dir, item_name))
        asset_fpaths = [ os.path.join(self.store_dir, item_name, 'test.xml'),
                         os.path.join(self.store_dir, item_name, 'test1.jpg'),
                         os.path.join(self.store_dir, item_name, 'test2.jpg'),
                         os.path.join(self.store_dir, item_name, 'test3.jpg'), ]
        
        for fpath in asset_fpaths:
            open(fpath, 'w').close()
        
        item_store = ItemStore(self.store_dir)
        assets = item_store.assets(item_name)
        
        self.assertEqual(len(asset_fpaths), len(assets))
        for asset in assets:
            self.assertIsInstance(asset, Asset)

    @patch('gaia.log.log.Log.get_logger')
    def test_assets_NO_ITEM_DIR(self, get_logger):
        item_name = 'NON_EXISTENT_ITEM'

        item_store = ItemStore(self.store_dir)
        assets = item_store.assets(item_name)

        self.assertEqual(0, len(assets))
            
    @patch('gaia.log.log.Log.get_logger')
    def test_assets_WITH_DIRECTORY_RAISES(self, get_logger):
        item_name = 'ITEM_NAME'
        os.mkdir(os.path.join(self.store_dir, item_name))
        
        os.mkdir(os.path.join(self.store_dir, item_name, 'EXTRA_DIRECTORY'))
        
        asset_fpaths = [ os.path.join(self.store_dir, item_name, 'test.xml'),
                         os.path.join(self.store_dir, item_name, 'test1.jpg'),
                         os.path.join(self.store_dir, item_name, 'test2.jpg'),
                         os.path.join(self.store_dir, item_name, 'test3.jpg'), ]
        
        for fpath in asset_fpaths:
            open(fpath, 'w').close()
        
        item_store = ItemStore(self.store_dir)
        self.assertRaises(StoreError, item_store.assets, item_name)
    
    @patch('gaia.log.log.Log.get_logger')
    def test__item_dir(self, get_logger):
        item_store = ItemStore(self.test_dir)
        item_name = 'ITEM_NAME'
        
        expected_item_dir = os.path.join(self.test_dir, item_name)

        self.assertFalse(os.path.exists(expected_item_dir))
        
        item_dir = item_store._item_dir(item_name)
        
        self.assertTrue(os.path.exists(expected_item_dir))
        self.assertEqual(expected_item_dir, item_dir)
        

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestItemStore),
    ])

if __name__ == '__main__':
    import testing
    testing.main(suite)
