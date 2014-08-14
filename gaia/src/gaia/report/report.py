import datetime


class Report:
    ''' A report is a nicely formatted, human-readable version of data

        The data should be self-formatting (ie support a str() method).
        If no header is provided, it's left blank.
        If no footer is provided, it shows the report date.
    '''
    def __init__(self, report_data, header=None, footer=None):
        self.header = header
        self.footer = footer
        self.report_data = report_data

    def __str__(self):
        ' return a formatted version of the report_data '

        if self.header:
            report = self.header + '\n'
        else:
            report = ''

        report += str(self.report_data) + '\n'

        if self.footer:
            report += self.footer
        else:
            report += 'Report Date: %s' % str(self._utcnow())

        return report

    def _utcnow(self):  # Helpful for testing purposes
        return datetime.datetime.utcnow().strftime('%d %b %Y, %I:%M %p')
