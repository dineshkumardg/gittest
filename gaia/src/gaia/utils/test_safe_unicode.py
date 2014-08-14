import unittest
from test_utils.gaia_test import GaiaTest
from gaia.utils.safe_unicode import safe_unicode, safe_formatted_unicode

class TestSafeUnicode(GaiaTest):
    def test_safe_unicode(self):
        expected_str1 = 'w\xe9\xa1\xb6orld'
        expected_str2 = 'uh\xe3\x91\x96oh'
        unicode_string1 = u'w\u9876orld'.encode('utf-8')
        unicode_string2 = u'uh\u3456oh'.encode('utf-8')
        
        ascii_string = safe_unicode(unicode_string1)
        self.assertEqual(expected_str1, ascii_string)

        ascii_string = safe_unicode(unicode_string2)
        self.assertEqual(expected_str2, ascii_string)

    def test_safe_formatted_unicode(self):
        expected_str = 'any format "w\xe9\xa1\xb6orld" string here "uh\xe3\x91\x96oh"'
        unicode_string1 = u'w\u9876orld'.encode('utf-8')
        unicode_string2 = u'uh\u3456oh'.encode('utf-8')
        
        ascii_string = safe_formatted_unicode('any format "%s" string here "%s"', unicode_string1, unicode_string2)
        self.assertEqual(expected_str, ascii_string)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestSafeUnicode),
    ])

if __name__ == '__main__':
    unittest.main()
