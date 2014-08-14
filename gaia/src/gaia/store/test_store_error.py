import unittest
from gaia.error import GaiaError
from gaia.store.store_error import StoreError

class TestStoreError(unittest.TestCase):

    def test_str(self):
        err = StoreError('An error', err='Oops')
        self.assertIsInstance(err, GaiaError)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestStoreError),
    ])

if __name__ == "__main__":
    unittest.main()
