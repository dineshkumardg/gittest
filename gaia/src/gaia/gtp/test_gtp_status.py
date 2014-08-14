import unittest
from testing.gaia_test import GaiaTest
from gaia.gtp.gtp_status import GtpStatus


class TestGtpStatus(GaiaTest):

    def test_properties(self):
        # Check the properties exist and are as expected
        expected_ready = 0
        expected_processing = 1
        expected_not_ready = 2
        expected_ready_fname = '_status_READY.txt'
        expected_processing_fname = '_status_PROCESSING.txt'
        
        self.assertEqual(expected_ready, GtpStatus.READY)
        self.assertEqual(expected_processing, GtpStatus.PROCESSING)
        self.assertEqual(expected_not_ready, GtpStatus.NOT_READY)
        self.assertEqual(expected_ready_fname, GtpStatus.READY_FNAME)
        self.assertEqual(expected_processing_fname, GtpStatus.PROCESSING_FNAME)        
        
    def test_str(self):
        # Check str works with instances
        status = GtpStatus(GtpStatus.READY)
        self.assertEqual('READY', str(status))
        
        status = GtpStatus(GtpStatus.PROCESSING)
        self.assertEqual('PROCESSING', str(status))
        
        status = GtpStatus(GtpStatus.NOT_READY)
        self.assertEqual('NOT_READY', str(status))
        
    def test_STATUS_OK_ready(self):
        test_fnames = ('_status_READY.txt', 'some_file.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.READY, actual_status)

    def test_STATUS_OK_processing(self):
        test_fnames = ('_status_READY.txt', 'somefile.txt', '_status_PROCESSING.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.PROCESSING, actual_status)

    def test_STATUS_OK_not_ready(self):
        test_fnames = ('afile.txt', 'some_file.txt', 'other_file.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.NOT_READY, actual_status)

    def test_STATUS_BAD_ready(self):
        test_fnames = ('_status_REAY.txt', 'some_file.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.NOT_READY, actual_status)

    def test_STATUS_BAD_processing(self):
        test_fnames = ('afile.txt', 'somefile.txt', '_status_PROC.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.NOT_READY, actual_status)

    def test_STATUS_BAD_both(self):
        test_fnames = ('_status_REAY.txt', '_status_PROC.txt')

        actual_status = GtpStatus.status(test_fnames)

        self.assertEqual(GtpStatus.NOT_READY, actual_status)

    def test_IS_READY_ready(self):
        test_fnames = ('_status_READY.txt', 'some_file.txt')
        
        self.assertTrue(GtpStatus.is_ready(test_fnames))

    def test_IS_READY_processing(self):
        test_fnames = ('_status_READY.txt', '_status_PROCESSING.txt')
        
        self.assertFalse(GtpStatus.is_ready(test_fnames))

    def test_IS_READY_not_ready(self):
        test_fnames = ('not_status.txt', 'not_ready.txt')
        
        self.assertFalse(GtpStatus.is_ready(test_fnames))

    def test_IS_PROCESSING_processing(self):
        test_fnames = ('some_file.txt', '_status_PROCESSING.txt')
        
        self.assertTrue(GtpStatus.is_processing(test_fnames))

    def test_IS_PROCESSING_ready(self):
        test_fnames = ('_status_READY.txt', 'not_PROCESSING.txt')
        
        self.assertFalse(GtpStatus.is_processing(test_fnames))

    def test_PROCESSING_not_ready(self):
        test_fnames = ('not_status.txt', 'not_ready.txt')
        
        self.assertFalse(GtpStatus.is_ready(test_fnames))


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGtpStatus),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
