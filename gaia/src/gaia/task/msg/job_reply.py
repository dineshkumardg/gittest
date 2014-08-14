from gaia.task.msg.reply import Reply

class JobReply(Reply):
    ''' A class for Replies to JobRequests

        replies have a status.
    '''
    OK = 'OK'
    TRY_AGAIN = 'TRY_AGAIN'
    FAILED = 'FAILED'

    def __init__(self, job_request, status):
        Reply.__init__(self, job_request, status=status)

    def is_ok(self):
        return self.status == self.OK

    def is_try_again(self):
        return self.status == self.TRY_AGAIN

    def is_failed(self):
        return self.status == self.FAILED

class OkReply(JobReply):
    def __init__(self, job_request):
        JobReply.__init__(self, job_request, status=JobReply.OK)

class TryAgainReply(JobReply):
    def __init__(self, job_request):
        JobReply.__init__(self, job_request, status=JobReply.TRY_AGAIN)

class FailedReply(JobReply):
    def __init__(self, job_request):
        JobReply.__init__(self, job_request, status=JobReply.FAILED)
