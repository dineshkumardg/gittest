class GtpSite:
    def __init__(self, project_code):
        self.items_dir = '/%s/items' % project_code  # FTP-path, so no need for os.path.join
        self.reports_bad_dir = '/%s/reports/bad' % project_code
        self.reports_good_dir = '/%s/reports/good' % project_code
        self.reports_reject_dir = '/%s/reports/reject' % project_code

    def item_dir(self, group, item_name):
        ' return the path on a Site for an item in a group'
        return '%s/%s/%s' % (self.items_dir, group, item_name)
