from gaia.report.report import Report


class RejectReport(Report):
    ''' A fully self contained report for Rejected Items.

        Note that this contains everything for Providers, and us, to interpret the errors.
    '''
    _reject_report_type = 'Item Rejected'

    def __init__(self, reject_reason, item_index_id, item_dom_id, item_dom_name, user_name, page_id=None, reject_report_filename=None, reject_xml_filename=None):
        header = '%s\n' % self._reject_report_type

        header += '-' * 10

        header += '\nItem: %s\n' % item_dom_name
        if reject_report_filename is not None and reject_xml_filename is not None:
            header += 'XML (with fixes if avail.): %s\n' % reject_xml_filename
            header += 'Report: %s\n' % reject_report_filename

        header += 'User: %s' % user_name

        report = '-' * 10
        report += '\n' + reject_reason + '\n'
        report += '-' * 10

        Report.__init__(self, report, header)


class BulkRejectReport(RejectReport):
    _reject_report_type = 'Bulk Rejection'
