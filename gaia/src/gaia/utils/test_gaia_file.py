import os.path
import unittest
from testing.gaia_test import GaiaTest
from gaia.utils.gaia_file import GaiaFile

class TestGaiaFile(GaiaTest):

    def test(self):
        expected_ftype = 'txt'
        fname = 'hello.txt'
        fpath = os.path.join(self.test_dir, fname)

        f = self._create_gaia_file(fname)

        self.assertEqual(fpath, f.fpath)
        self.assertEqual(fname, f.fname)
        self.assertEqual(expected_ftype, f.ftype)   # the file extension without a leading dot

        self.assertEqual(fpath, f.name) # WARNING: this is for file() compatibility and should NOT be used in Gaia code!

    def test_fbase(self):
        fname = 'hello.txt'
        f = self._create_gaia_file(fname)

        self.assertEqual('hello', f.fbase)

    def test_fbase_NO_EXT(self):      
        fname = 'hello'
        f = self._create_gaia_file(fname)
        
        self.assertEqual('hello', f.fbase)
    
    def _create_gaia_file(self, fname):
        fpath = os.path.join(self.test_dir, fname)

        return GaiaFile(fpath, 'w')
        
    def test_is_image(self):
        for ext in ['jpeg', 'jpg', 'tiff', 'tif', 'png',
                    'JPEG', 'JPG', 'TIFF', 'TIF', 'PNG']:
            fname = 'hello.' + ext
            f = self._create_gaia_file(fname)
            self.assertTrue(f.is_image())

    def test_is_image_NOT(self):
        for ext in ['txt', 'xml', 'csv', 'xsl']:
            fname = 'hello.' + ext
            f = self._create_gaia_file(fname)
            self.assertFalse(f.is_image())

    def test_is_web_image(self):
        for ext in ['jpeg', 'jpg', 'png',
                    'JPEG', 'JPG', 'PNG']:
            fname = 'hello.' + ext
            f = self._create_gaia_file(fname)
            self.assertTrue(f.is_web_image())

    def test_is_web_image_NOT(self):
        for ext in ['txt', 'xml', 'csv', 'xsl', 'tiff', 'tif']:
            fname = 'hello.' + ext
            f = self._create_gaia_file(fname)
            self.assertFalse(f.is_web_image())
            

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaFile),
    ])

if __name__ == "__main__":
   import testing
   testing.main(suite)
