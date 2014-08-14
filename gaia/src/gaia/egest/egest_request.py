from gaia.task.msg.job_request import JobRequest

class EgestRequest(JobRequest):
    def __init__(self, item_id, item_name, is_xml):
        job_name = '%s|%s' % (item_id, item_name)
        JobRequest.__init__(self, job_name, item_id=item_id, item_name=item_name, release_type=is_xml)
