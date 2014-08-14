import os
import unittest
from test_utils.gaia_test import GaiaTest
from gaia.utils.gaia_folder import GaiaFolder

class TestGaiaFolder(GaiaTest):
    
    def setUp(self):
        GaiaTest.setUp(self)
        
    def tearDown(self):
        GaiaTest.tearDown(self)
        
    def test_size(self):
        store_dir = os.path.join(self.test_dir, 'store_root')
        os.makedirs(store_dir)
        self.assertEqual(0, GaiaFolder.size(store_dir))

        fsize = 3
        num_assets = 5

        for i in range(0, num_assets):
            fpath = os.path.join(store_dir, 'asset_%d.txt' % i)
            f = open(fpath, 'w+')
            f.write('abc') # fsize bytes
            f.close()

        expected_size = num_assets * fsize
        self.assertEqual(expected_size, GaiaFolder.size(store_dir))

        sub_dir = os.path.join(store_dir, 'sub_folder')
        os.makedirs(sub_dir)

        fsize = 5
        for i in range(0, num_assets):
            fpath = os.path.join(sub_dir, 'asset_%d.txt' % i)
            f = open(fpath, 'w+')
            f.write('defgh') # fsize bytes
            f.close()

        sub_size = num_assets * fsize
        self.assertEqual(sub_size, GaiaFolder.size(sub_dir))
        self.assertEqual(expected_size + sub_size, GaiaFolder.size(store_dir))

    def test_ls_fpaths(self):
        store_dir = os.path.join(self.test_dir, 'store_root')
        os.makedirs(store_dir)
        num_assets = 5

        expected_fpaths = []
        for i in range(0, num_assets):
            fname = 'asset_%d.txt' % i
            fpath = os.path.join(store_dir, fname)
            f = open(fpath, 'w+')
            f.write('abc')
            f.close()
            expected_fpaths.append(fpath)

        self.assertEqual(sorted(expected_fpaths), sorted(GaiaFolder.ls(store_dir)))

        sub_dir = os.path.join(store_dir, 'sub_folder')
        os.makedirs(sub_dir)

        for i in range(0, num_assets):
            fpath = os.path.join(sub_dir, 'asset_%d.txt' % i)
            f = open(fpath, 'w+')
            f.write('defgh') # fsize bytes
            f.close()
            expected_fpaths.append(fpath)

        self.assertEqual(sorted(expected_fpaths), sorted(GaiaFolder.ls(store_dir)))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaFolder),
    ])

if __name__ == '__main__':
    unittest.main()
