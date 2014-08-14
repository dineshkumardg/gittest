from gaia.report.report import Report


class ErrorReport(Report):
    def __init__(self, provider_name, group, item_name, error):
        # Note that error can be a single error or a GaiaErrors object.
        header = 'Error Report for %s\nProblem with Item "%s" in Group "%s"' % (provider_name, item_name, group)

        Report.__init__(self, report_data=error, header=header)
