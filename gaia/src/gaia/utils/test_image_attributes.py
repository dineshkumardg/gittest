import unittest
from gaia.utils.image_attributes import ImageAttributes, JpegImageAttributes, TiffImageAttributes, PngImageAttributes


class TestImageAttributes(unittest.TestCase):

    def test__init__(self):
        image_attributes = ImageAttributes(ImageAttributes.TIFF_FORMAT, (400, 400), 1, 'jpg', compression_quality=None)
        
        self.assertEqual(ImageAttributes.TIFF_FORMAT, image_attributes.format)
        self.assertEqual((400, 400), image_attributes.dpi)
        self.assertEqual(1, image_attributes.depth)
        self.assertEqual(None, image_attributes.compression_quality)
        
    # Call __cmp__
    # Check the explicit return value
    # Check ==
    # Check !=
    # Check > & < NOTE: NOT TESTING THESE AS WE NEED TO UNDERSTAND WHETHER TO IMPLEMENT OR NOT
        
    def test_comparison_SAME(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (500,500), 1, 'jpg', compression_quality=None)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (500,500), 1, 'jpg', compression_quality=None)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_DIFFERENT_QUALITY(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=80)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg')
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_NONE_FOR_ATT1(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=None)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_NONE_FOR_ATT2(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=None)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_NONE_FOR_ATT2_IN_LIST(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=None)
        
        att2_list = [att2,]
        self.assertNotIn(att1, att2_list)
        
    def test_comparison_QUALITY_NONE_ZERO_FOR_ATT2_IN_LIST(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=None)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=70)
        
        att2_list = [att2,]
        self.assertIn(att1, att2_list)
        
    def test_comparison_QUALITY_ZERO_FOR_ATT2_IN_LIST(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=None)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=0)
        
        att2_list = [att2,]
        self.assertIn(att1, att2_list)
                
    def test_comparison_DIFFERENT_DPIS(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg')
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (200,200), 1, 'jpg')
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1) 
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2_BY_KWARG(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg')
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=80)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)

    def test_comparison_QUALITY_ONLY_FOR_ATT1_BY_KWARG(self):
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=90)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg')
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_ZERO_ONLY_FOR_ATT1_BY_KWARG(self):
        # These should compare equally - ImageMagick returns 'None' string when no compression type found
        att1 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=0)
        att2 = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg')
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test__str__(self):
        expected_str = 'Format: %s, DPI: %s, Bit depth: %s, File extension: %s, Compression quality: %s' % (ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', 80)
        attrs = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=80)
        
        self.assertEqual(expected_str, str(attrs))
        
    # Note: Format given from ImageMagick, not file_ext
    def test_is_tiff(self):
        image_attributes = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'tif')
        self.assertTrue(image_attributes.is_tiff())
        self.assertFalse(image_attributes.is_jpeg())
        
    # Note: Format given from ImageMagick, not file_ext    
    def test_is_jpeg(self):
        image_attributes = ImageAttributes(ImageAttributes.JPEG_FORMAT, (300,300), 1, 'jpg')
        self.assertTrue(image_attributes.is_jpeg())
        self.assertFalse(image_attributes.is_tiff())


class TestJpegImageAttributes(unittest.TestCase):

    def test__init__(self):
        image_attributes = JpegImageAttributes(400, 1)
        
        self.assertEqual(ImageAttributes.JPEG_FORMAT, image_attributes.format)
        self.assertEqual((400, 400), image_attributes.dpi)
        self.assertEqual(1, image_attributes.depth)
        self.assertEqual(JpegImageAttributes.FILE_EXT, image_attributes.file_ext)
        self.assertEqual(None, image_attributes.compression_quality)
        
    def test_comparison_SAME(self):
        att1 = JpegImageAttributes(500, 1, None)
        att2 = JpegImageAttributes(500, 1, None)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_DIFFERENT_QUALITY(self):
        att1 = JpegImageAttributes(300, 1, compression_quality=80)
        att2 = JpegImageAttributes(300, 1, compression_quality=70)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2(self):
        att1 = JpegImageAttributes(300, 1)
        att2 = JpegImageAttributes(300, 1, compression_quality=70)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_DIFFERENT_DPIS(self):
        att1 = JpegImageAttributes(300, 1)
        att2 = JpegImageAttributes(200, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1) 
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2_BY_KWARG(self):
        att1 = JpegImageAttributes(300, 1)
        att2 = JpegImageAttributes(300, 1, compression_quality=80)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)

    def test_comparison_QUALITY_ONLY_FOR_ATT1_BY_KWARG(self):
        att1 = JpegImageAttributes(300, 1, compression_quality=90)
        att2 = JpegImageAttributes(300, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_ZERO_ONLY_FOR_ATT1_BY_KWARG(self):
        # These should compare equally - ImageMagick returns 'None' string when no compression type found
        att1 = JpegImageAttributes(300, 1, compression_quality=0)
        att2 = JpegImageAttributes(300, 1)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test__str__(self):
        expected_str = 'Format: %s, DPI: %s, Bit depth: %d, File extension: %s, Compression quality: %d' % (ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', 80)
        attrs = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', compression_quality=80)
        
        self.assertEqual(expected_str, str(attrs))
        
    def test_is_type(self):
        image_attributes = JpegImageAttributes(300, 1)
        self.assertTrue(image_attributes.is_jpeg())
        self.assertFalse(image_attributes.is_tiff())
        

class TestTiffImageAttributes(unittest.TestCase):

    def test__init__(self):
        image_attributes = TiffImageAttributes(400, 1, None)
        
        self.assertEqual(ImageAttributes.TIFF_FORMAT, image_attributes.format)
        self.assertEqual((400, 400), image_attributes.dpi)
        self.assertEqual(1, image_attributes.depth)
        self.assertEqual(None, image_attributes.compression_quality)
        
    def test_comparison_SAME(self):
        att1 = TiffImageAttributes(500, 1, None)
        att2 = TiffImageAttributes(500, 1, None)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_DIFFERENT_QUALITY(self):
        att1 = TiffImageAttributes(300, 1, 80)
        att2 = TiffImageAttributes(300, 1, 70)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2(self):
        att1 = TiffImageAttributes(300, 1)
        att2 = TiffImageAttributes(300, 1, compression_quality=70)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_DIFFERENT_DPIS(self):
        att1 = TiffImageAttributes(300, 1)
        att2 = TiffImageAttributes(200, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1) 
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2_BY_KWARG(self):
        att1 = TiffImageAttributes(300, 1)
        att2 = TiffImageAttributes(300, 1, compression_quality=80)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)

    def test_comparison_QUALITY_ONLY_FOR_ATT1_BY_KWARG(self):
        att1 = TiffImageAttributes(300, 1, compression_quality=90)
        att2 = TiffImageAttributes(300, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_ZERO_ONLY_FOR_ATT1_BY_KWARG(self):
        # These should compare equally - ImageMagick returns 'None' string when no compression type found
        att1 = TiffImageAttributes(300, 1, compression_quality=0)
        att2 = TiffImageAttributes(300, 1)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test__str__(self):
        expected_str = 'Format: %s, DPI: %s, Bit depth: %s, File extension: jpg, Compression quality: %s' % (ImageAttributes.TIFF_FORMAT, (300,300), 1, 80)
        attrs = ImageAttributes(ImageAttributes.TIFF_FORMAT, (300,300), 1, 'jpg', 80)
        
        self.assertEqual(expected_str, str(attrs))
        
    def test_is_type(self):
        image_attributes = TiffImageAttributes(300, 1)
        self.assertTrue(image_attributes.is_tiff())
        self.assertFalse(image_attributes.is_jpeg())
        

class TestPngImageAttributes(unittest.TestCase):

    def test__init__(self):
        image_attributes = PngImageAttributes(400, 1, None)
        
        self.assertEqual(ImageAttributes.PNG_FORMAT, image_attributes.format)
        self.assertEqual((400, 400), image_attributes.dpi)
        self.assertEqual(1, image_attributes.depth)
        self.assertEqual(None, image_attributes.compression_quality)
        
    def test_comparison_SAME(self):
        att1 = PngImageAttributes(500, 1, None)
        att2 = PngImageAttributes(500, 1, None)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_DIFFERENT_QUALITY(self):
        att1 = PngImageAttributes(300, 1, 80)
        att2 = PngImageAttributes(300, 1, 70)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2(self):
        att1 = PngImageAttributes(300, 1)
        att2 = PngImageAttributes(300, 1, compression_quality=70)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_DIFFERENT_DPIS(self):
        att1 = PngImageAttributes(300, 1)
        att2 = PngImageAttributes(200, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1) 
        
    def test_comparison_QUALITY_ONLY_FOR_ATT2_BY_KWARG(self):
        att1 = PngImageAttributes(300, 1)
        att2 = PngImageAttributes(300, 1, compression_quality=80)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(-1, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertFalse(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertTrue(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertTrue(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)

    def test_comparison_QUALITY_ONLY_FOR_ATT1_BY_KWARG(self):
        att1 = PngImageAttributes(300, 1, compression_quality=90)
        att2 = PngImageAttributes(300, 1)
        
        self.assertEqual(-1, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertFalse(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertTrue(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertTrue(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test_comparison_QUALITY_ZERO_ONLY_FOR_ATT1_BY_KWARG(self):
        # These should compare equally - ImageMagick returns 'None' string when no compression type found
        att1 = PngImageAttributes(300, 1, compression_quality=0)
        att2 = PngImageAttributes(300, 1)
        
        self.assertEqual(0, att1.__cmp__(att2))
        self.assertEqual(0, att2.__cmp__(att1))
        
        self.assertTrue(att1 == att2)
        self.assertTrue(att2 == att1)
        
        self.assertFalse(att1 != att2)
        self.assertFalse(att2 != att1)
        
        self.assertFalse(att1 < att2)
        self.assertFalse(att2 < att1)
        self.assertFalse(att1 > att2)
        self.assertFalse(att2 > att1)
        
    def test__str__(self):
        expected_str = 'Format: %s, DPI: %s, Bit depth: %s, File extension: jpg, Compression quality: %s' % (ImageAttributes.PNG_FORMAT, (300,300), 1, 80)
        attrs = ImageAttributes(ImageAttributes.PNG_FORMAT, (300,300), 1, 'jpg', 80)
        
        self.assertEqual(expected_str, str(attrs))
        
    def test_is_type(self):
        image_attributes = PngImageAttributes(300, 1)
        self.assertTrue(image_attributes.is_png())
        self.assertFalse(image_attributes.is_jpeg())
        self.assertFalse(image_attributes.is_tiff())
        

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestImageAttributes),
    unittest.TestLoader().loadTestsFromTestCase(TestJpegImageAttributes),
    unittest.TestLoader().loadTestsFromTestCase(TestTiffImageAttributes),
    ])

if __name__ == '__main__':
    unittest.main()
