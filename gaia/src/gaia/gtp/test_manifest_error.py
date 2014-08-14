import unittest
from testing.gaia_test import GaiaTest
from gaia.error import GaiaError
from gaia.gtp.manifest_error import ManifestError, MissingManifestError

class TestManifestError(GaiaTest):

    def test__str__(self):
        expected_err_str = 'ManifestError: A problem'
        expected_err_msg = 'A problem'
        
        err = ManifestError(expected_err_msg)

        self.assertEqual(expected_err_str, str(err))
        self.assertEqual(expected_err_msg, err.msg)
        self.assertIsInstance(err, GaiaError)
    
class TestMissingManifestError(GaiaTest):

    def test__str__(self):
        expected_err_str = 'MissingManifestError: No manifest file for item "cho_1234" in group "all"'
        
        group = 'all'
        item_name = 'cho_1234'
        err = MissingManifestError(group, item_name)

        self.assertEqual(expected_err_str, str(err))
        self.assertIsInstance(err, ManifestError)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestManifestError),
    unittest.TestLoader().loadTestsFromTestCase(TestMissingManifestError),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
