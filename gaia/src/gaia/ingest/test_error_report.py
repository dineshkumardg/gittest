import unittest
from testing.gaia_test import GaiaTest
from gaia.error import GaiaError, GaiaErrors
from gaia.ingest.error_report import ErrorReport


class TestErrorReport(GaiaTest):

    def test__init__(self):
        provider = 'PROVIDER'
        group = 'GROUP'
        item = 'item1'

        expected_header = 'Error Report for PROVIDER\nProblem with Item "item1" in Group "GROUP"'

        errors = [GaiaError('Error 1'), GaiaError('Error 2'), GaiaError('Error 3')]
        report = ErrorReport(provider, group, item, errors)
        self.assertIsInstance(report, ErrorReport)
        self.assertEqual(expected_header, report.header)

    def test_str(self):
        expected_report = '''Error Report for HTC
Problem with Item "item1" in Group "all"
GaiaError: Error 1
Error 2
GaiaError: Error 3
Report Date: '''

        errors = [GaiaError('Error 1'), Exception('Error 2'), GaiaError('Error 3')]
        err = GaiaErrors(*errors)
        report = ErrorReport('HTC', 'all', 'item1', err)
        text = str(report)

        text_without_date = text[:-len(str(report._utcnow()))]

        self.assertEqual(expected_report, text_without_date)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestErrorReport),
    ])

if __name__ == '__main__':
    import testing
    testing.main(suite)
