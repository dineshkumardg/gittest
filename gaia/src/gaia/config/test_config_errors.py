import unittest
from gaia.config.config_errors import GaiaConfigurationError


class TestGaiaConfigurationError(unittest.TestCase):
    def test_str(self):
        expected_err_msg = 'GaiaConfigurationError: This is an error msg'
        
        self.assertEquals(expected_err_msg, str(GaiaConfigurationError('This is an error msg')))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaConfigurationError),
    ])

if __name__ == "__main__":
    unittest.main()
