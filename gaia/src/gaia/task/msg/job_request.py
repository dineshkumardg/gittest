from gaia.task.msg.request import Request

class JobRequest(Request):
    ''' A JobRequest is  a request to do a job.
        The job_name is a string that uniquely identifies the job.
    '''

    def __init__(self, job_name, **kwargs):
        Request.__init__(self, request_type='JOB', job_name=job_name, **kwargs)
