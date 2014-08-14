import os
import unittest
from testing.gaia_test import GaiaTest
from gaia.gtp.manifest import Manifest
from gaia.gtp.manifest_error import ManifestError

class TestManifest(GaiaTest):

    def test__manifest_fname(self):
        self.assertEqual('manifest.md5', Manifest.fname)

    def test__init__MISSING_MANIFEST_FILE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__EMPTY_MANIFEST(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_SHORT_CHECKSUM(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a68  file1.txt') # < 32 chars in checksum
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_LONG_CHECKSUM(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a680202  file1.txt') # > 32 chars in checksum
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_BAD_CHECKSUM_CHARS(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('aaaaaaaaaaGaaaaaaaaaaaaaaaaaaaaaaa  file1.txt') # 'G' in checksum
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_BAD_TYPE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802 ?file1.txt') # '?' for type
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_NO_FNAME(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802  ') # No filename!
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__BAD_MANIFEST_FORMAT_NO_CHECKSUM(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('  file1.txt') # No checksum!
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)

    def test__init__IGNORE_INITIAL_BLANK_LINE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('\n')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt')
        f.close()

        manifest = Manifest(fname)
        self.assertEqual(1, len(manifest.checksums()))

    def test__init__IGNORE_FINAL_BLANK_LINE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n\n')
        f.close()

        manifest = Manifest(fname)
        self.assertEqual(1, len(manifest.checksums()))

    def test__init__IGNORE_MID_BLANK_LINE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n')
        f.write('c58322543625d7558e73457822376716 *test_img.jpg\n\n')
        f.write('6ff29096ae0c8f974ef89beb53260336  test_img.png\n')
        f.close()

        manifest = Manifest(fname)
        self.assertEqual(3, len(manifest.checksums()))

    def test__init__IGNORE_COMMENT_LINE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('#Test that a comment line is ignored\n')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n')
        f.write('c58322543625d7558e73457822376716 *test_img.jpg\n\n')
        f.write('#c58322543625d7558e73457822376716 *test_img.jpg\n') # Ignore a line in the middle, too.
        f.write('6ff29096ae0c8f974ef89beb53260336  test_img.png\n')
        f.close()

        manifest = Manifest(fname)
        self.assertEquals(3, len(manifest.checksums()))

    def test__init__IGNORE_STATUS_FILES(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('#Test that a comment line is ignored\n')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n')
        f.write('c58322543625d7558e73457822376716  _status_READY.txt\n\n')
        f.write('c58322543625d7558e73457822376716  _status_PROCESSING.txt\n\n')
        f.write('6ff29096ae0c8f974ef89beb53260336  test_img.png\n')
        f.close()

        manifest = Manifest(fname)
        self.assertEquals(2, len(manifest.checksums()))

    def test__init__BAD_COMMENT_LINE(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('=Test that a bad comment line marker is reported\n')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n')
        f.close()

        self.assertRaises(ManifestError, Manifest, fname)
        
    def test__init__WINDOWS_LINE_ENDING(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\r') # \r for windows line ending
        f.close()

        expected_checksums = {'file1.txt': 'b755e61c76f3786d326dd278c98a6802'}
        
        manifest = Manifest(fname)
        self.assertDictEqual(expected_checksums, manifest.checksums())

    def test_checksums(self):
        fname = os.path.join(self.test_dir, 'manifest.md5')
        f = open(fname, 'w')
        f.write('b755e61c76f3786d326dd278c98a6802  file1.txt\n')
        f.write('c58322543625d7558e73457822376716 *test_img.jpg\n')
        f.write('6ff29096ae0c8f974ef89beb53260336  test_img.png\n')
        f.close()

        expected_checksums = {'file1.txt': 'b755e61c76f3786d326dd278c98a6802',
                              'test_img.jpg': 'c58322543625d7558e73457822376716',
                              'test_img.png': '6ff29096ae0c8f974ef89beb53260336'}

        manifest = Manifest(fname)
        self.assertDictEqual(expected_checksums, manifest.checksums())


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestManifest),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
