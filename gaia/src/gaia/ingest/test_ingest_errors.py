import unittest
from testing.gaia_test import GaiaTest
from gaia.error import GaiaError
from gaia.ingest.ingest_errors import IngestError

class TestIngestError(GaiaTest):

    def test_str(self):
        expected_err = 'IngestError: An error message'
        err = IngestError('An error message')
        self.assertEqual(expected_err, str(err))
        self.assertIsInstance(err, GaiaError)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestIngestError),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
