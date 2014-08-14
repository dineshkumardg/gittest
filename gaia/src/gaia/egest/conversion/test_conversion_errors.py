import unittest
from gaia.egest.conversion.conversion_errors import ConversionError, DialogBConversionError


class TestConversionError(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'ConversionError: This is an error msg'
        
        self.assertEqual(expected_err_msg, str(ConversionError('This is an error msg')))
        
class TestDialogBConversionError(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'DialogBConversionError: Problem converting "Item Name"'
        
        self.assertEqual(expected_err_msg, str(DialogBConversionError('Item Name')))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestConversionError),
    unittest.TestLoader().loadTestsFromTestCase(TestDialogBConversionError),
    ])

if __name__ == "__main__":
    unittest.main()
