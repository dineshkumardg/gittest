
from gaia.task.msg.job_request import JobRequest

class JobsDoneRequest(JobRequest):
    ' Used to flag that processing of jobs has completed '
    # This isn't really a job-request, but it is (currently) sent as another job-request, hence the confusing base class and job_name
    # TODO: re-design and change all the flush/feed-building stuff now that we know the requirements!

    def __init__(self):
        JobRequest.__init__(self, job_name='_JOBS_DONE_')
