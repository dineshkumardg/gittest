import os
import unittest
from testing.gaia_test import GaiaTest
from gaia.asset.asset import Asset, AssetError


class TestAsset(GaiaTest):
    def test__init___FAILS_if_not_exists(self):
        fpath = os.path.join(self.test_dir, 'cho_item_001.jpg')
        self.assertRaises(IOError, Asset, fpath)

    def test_write(self):
        expected_ftype = 'jpg'
        fname = 'cho_item_001.jpg'
        fpath = os.path.join(self.test_dir, fname)

        asset = Asset(fpath, 'wb')
        asset.write('hello')
        asset.close()

        self.assertEqual(fpath, asset.fpath) # Gaia standard naming
        self.assertEqual(fname, asset.fname) # Gaia standard naming
        self.assertEqual(expected_ftype, asset.ftype) # Gaia standard naming

        self.assertEqual(fpath, asset.name)  # WARNING: preserves file() - like interface. DO NOT USE!

    def test_checksum(self):
        expected_checksum = 'eb733a00c0c9d336e65691a37ab54293'
        fpath = os.path.join(self.test_dir, 'cho_item_001.jpg')

        asset = Asset(fpath, 'wb')
        asset.write('test data')
        asset.close()

        checksum = asset.checksum()

        self.assertEqual(expected_checksum, checksum)

    def _test_mime_type(self, expected_mime_type, file_ext):
        fpath = os.path.join(self.test_dir, 'cho_item_001.' + file_ext)

        asset = Asset(fpath, 'wb')
        asset.write('hello')
        asset.close()

        self.assertEqual(expected_mime_type, asset.mime_type())

    def test_mime_type(self):
        # ref: http://www.iana.org/assignments/media-types/index.html
        self._test_mime_type('text/plain', 'txt')
        self._test_mime_type('application/xml', 'xml') # Windows: 'text/xml' ??
        self._test_mime_type('application/xml', 'XML') # Windows: 'text/xml' ??

        self._test_mime_type('image/jpeg', 'JPG') #?? image/pjpeg ??
        self._test_mime_type('image/jpeg', 'jpg') #?? image/pjpeg ??
        self._test_mime_type('image/tiff', 'tiff')

        self._test_mime_type('audio/mpeg', 'mp3')  #??? audio/x-mpg ??

    def test__file_type_latex_centos_correction(self):
        fpath = os.path.join(os.path.dirname(__file__), 'test_files/centos-latex.xml')
        file_type = Asset(fpath, 'rb')._file_type()

        self.assertEqual('application/xml', file_type)

    def test__file_type_minix_centos_correction(self):
        fpath = os.path.join(os.path.dirname(__file__), 'test_files/minix_filesystem.jpg')
        file_type = Asset(fpath, 'rb')._file_type()

        self.assertEqual('image/jpeg', file_type)

    #@unittest.skipIf(sys.platform.startswith("win"), 'requires the unix magic library and python extension')
    def test__file_type_BINARY(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        expectations = [(os.path.join(test_dir, 'test_tiff.tif'), 'image/tiff'),
                        (os.path.join(test_dir, 'test_jpeg.jpg'), 'image/jpeg'),
                        (os.path.join(test_dir, 'test_mp3.mp3'), 'audio/mpeg'),]

        for fpath, mime in expectations:
            self.assertEqual(mime, Asset(fpath, 'rb')._file_type())

    def _write_xml(self, xml):
        fpath = os.path.join(self.test_dir, 'test_xml.xml')
        f = open(fpath, 'wb')
        f.write(xml)
        f.close()
        return fpath

    #@unittest.skipIf(sys.platform.startswith("win"), 'requires the unix magic library and python exstension')
    def test__file_type_XML_WITH_PI(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
   </book>
<catalog>"""

        fpath = self._write_xml(xml)
        asset = Asset(fpath, 'rb')
        self.assertEqual('application/xml', asset._file_type())

    #@unittest.skipIf(sys.platform.startswith("win"), 'requires the unix magic library and python exstension')
    def test__file_type_XML_NO_XML_PI(self):
        xml = """<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
   </book>
<catalog>"""

        fpath = self._write_xml(xml)
        asset = Asset(fpath, 'rb')
        self.assertEqual('text/plain', asset._file_type()) # NOTE!

    #@unittest.skipIf(sys.platform.startswith("win"), 'requires the unix magic library and python exstension')
    def test_validate(self):

        xml = """<?xml version="1.0" encoding="UTF-8"?>
<catalog>
   <book id="bk101">
      <author>Gambardella, Matthew</author>
   </book>
<catalog>"""

        xml_fpath = self._write_xml(xml)

        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        test_files = [os.path.join(test_dir, 'test_tiff.tif'),
                      os.path.join(test_dir, 'test_jpeg.jpg'),
                      os.path.join(test_dir, 'test_mp3.mp3'),
                      xml_fpath]

        for fpath in test_files:
            try:
                Asset(fpath, 'rb').validate()
            except AssetError, e:
                self.fail('UNEXPECTEDLY FAILED with AssetError (err="%s")' % str(e))

    #@unittest.skipIf(sys.platform.startswith("win"), 'requires the unix magic library and python exstension')
    def test_validate_NOT_OK(self):
        test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
        fpath = os.path.join(test_dir, 'test_mp3_incorrect_ext.jpg')

        self.assertRaises(AssetError, Asset(fpath, 'rb').validate)

    def test_cmp_NONE(self):
        fname = 'asset.txt'
        fpath = os.path.join(self.test_dir, fname)

        asset1 = Asset(fpath, 'wb')

        self.assertFalse(asset1 == None)   # test the equals operator (in all its flavours)
        self.assertTrue(asset1 != None)
        self.assertFalse(asset1 is None)
        self.assertTrue(not asset1 is None)
        self.assertTrue(asset1) # is not None
        self.assertFalse(not asset1) # is None

        self.assertTrue(asset1 > None)   # test the alphabetical order
        self.assertFalse(asset1 < None)

    def test_cmp_SAME_FPATH(self):
        fname = 'asset.txt'
        fpath = os.path.join(self.test_dir, fname)

        asset1 = Asset(fpath, 'wb')
        asset2 = Asset(fpath, 'wb')

        self.assertTrue(asset1 == asset2)   # test the equals operator
        self.assertFalse(asset1 != asset2)
        self.assertFalse(asset1 > asset2)   # test the alphabetical order
        self.assertFalse(asset1 < asset2)

    def test_cmp_DIFFERENT_FPATH(self):
        fname = 'asset1.jpg'
        fpath = os.path.join(self.test_dir, fname)

        asset1 = Asset(fpath, 'wb')

        fname = 'asset2.jpg'
        fpath = os.path.join(self.test_dir, fname)

        asset2 = Asset(fpath, 'wb')

        self.assertTrue(asset1 != asset2)   # test the equals operator
        self.assertFalse(asset1 == asset2)
        self.assertFalse(asset1 > asset2)   # test the alphabetical order
        self.assertTrue(asset1 < asset2)

    def test_cmp_SAME_FPATH_DIFFERENT_MODE(self):
        fname = 'asset.txt'
        fpath = os.path.join(self.test_dir, fname)

        asset_wb = Asset(fpath, 'wb')
        asset_r  = Asset(fpath, 'r')

        self.assertTrue(asset_wb == asset_r)   # test the equals operator
        self.assertFalse(asset_wb != asset_r)
        self.assertFalse(asset_wb > asset_r)    # test the alphabetical order
        self.assertFalse(asset_wb < asset_r)

    def test_list_set_MULTIPLE_ASSET(self):
        fname = 'asset.txt'
        fpath = os.path.join(self.test_dir, fname)

        assets = [Asset(fpath, 'wb'), Asset(fpath, 'r'), Asset(fpath, 'r'), Asset(fpath, 'r'), Asset(fpath, 'r'), Asset(fpath, 'r')]
        assets_dict = {Asset(fpath, 'wb'):1, Asset(fpath, 'r'):1, Asset(fpath, 'r'):1, Asset(fpath, 'r'):1, Asset(fpath, 'r'):1, Asset(fpath, 'r'):1}

        self.assertEquals(1, len(set(assets)))
        self.assertEquals(1, len(assets_dict.keys()))

    def _test_fd(self):
        print '*** This test check how many open Asset/files can be created simultaneously'
        fpath = os.path.join(self.test_dir, 'test_file.txt')

        assets = [] # defeat garbage collection
        for i in range(0, 2000):    # 1024 is a typical, default max-open-fileslimit
            print i
            assets.append(Asset(fpath, 'w'))

    def test_image_for_cmyk(self):
        sRGB_asset = Asset(os.path.join(os.path.dirname(__file__), 'test_files/sRGB.jpg'), 'rb')
        sRGB_asset.validate()

        CMYK_asset = Asset(os.path.join(os.path.dirname(__file__), 'test_files/CMYK.jpg'), 'rb')
        # identify -format '%[colorspace]' xxx
        self.assertRaises(AssetError, CMYK_asset.validate)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestAsset),
    ])

if __name__ == '__main__':
    import testing
    testing.main(suite)
