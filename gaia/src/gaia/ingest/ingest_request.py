from gaia.task.msg.job_request import JobRequest

class IngestRequest(JobRequest):
    def __init__(self, provider_name, group, item_name):
        job_name = '%s|%s|%s' % (provider_name, group, item_name)
        JobRequest.__init__(self, job_name, provider_name=provider_name, group=group, item_name=item_name)
