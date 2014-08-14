import unittest
from gaia.report.report import Report
import datetime


class TestReport(unittest.TestCase):
    def test__init__(self):
        data = 'This is some report content'
        header = 'A heading'
        footer = 'A footer'
        report = Report(data, header=header, footer=footer)
        self.assertEqual(data, report.report_data)
        self.assertEqual(header, report.header)
        self.assertEqual(footer, report.footer)

    def test_str_NO_FOOTER(self):
        expected_report_data = 'This is some report content'
        header = 'A heading'
        report = Report(expected_report_data, header=header)
        output = str(report)
        expected_output = 'A heading\nThis is some report content\nReport Date: '
        self.assertTrue(output.startswith(expected_output))

    def test_str_WITH_FOOTER(self):
        expected_report_data = 'This is some report content'
        header = 'A heading'
        footer = 'A footer'
        report = Report(expected_report_data, header=header, footer=footer)
        output = str(report)
        expected_output = 'A heading\nThis is some report content\nA footer'
        self.assertEqual(expected_output, output)

    def test_utcnow(self):
        expected_date = datetime.datetime.utcnow().strftime('%d %b %Y, %I:%M %p')
        report = Report('something to report on!')
        self.assertEqual(expected_date, report._utcnow())

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestReport),
    ])
