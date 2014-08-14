import unittest
import datetime
import gaia.utils.now
from mock import patch

class TestNow(unittest.TestCase):

    def test_now(self):
        
        replacement_utcnow = datetime.datetime(1999, 12, 31, 23, 59, 59, 999999)
        expected_output = '1999_12_31_23_59_59_999999'
        
        with patch('datetime.datetime') as date_time:
            
            date_time.utcnow.return_value = replacement_utcnow
            
            now = gaia.utils.now.now()
            
            self.assertEqual(expected_output, now)
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestNow),
    ])

if __name__ == "__main__":
    unittest.main()
