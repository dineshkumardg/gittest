from time import time
from collections import OrderedDict

class JobQueue:
    ''' A queue of jobs waiting to be handled.

        Keeps track of waiting times and number of outstanding jobs

        threshold = the number of outstanding jobs that are allowed
        expiry_period = the time in _seconds_ after which a job is considered
        to have "expired" ie it should have already been dealt with.
    '''

    def __init__(self, max_size, expiry_period):
        self.max_size = max_size
        self.expiry_period = expiry_period
        self._jobs = OrderedDict()

    def append(self, job):
        self._jobs[job] = time()

    def remove(self, job):
        del self._jobs[job] # raises ValueError if not in queue

    def size(self):
        return len(self._jobs)

    def __len__(self):
        return len(self._jobs)

    def is_full(self):
        return self.size() > self.max_size

    def expired(self):
        ' remove any jobs that have expired, and return them in a list '
        now = time()
        expired_jobs = []

        for job in self._jobs:
            if now - self._jobs[job] > self.expiry_period:
                expired_jobs.append(job)
                del self._jobs[job]
            else:
                break # Note: due to Ordering, the rest of the list will be okay

        return expired_jobs

    def __str__(self):
        return str(self._jobs.keys())

    def __iter__(self):
        return self

    def next(self):
        try:
            job, time = self._jobs.popitem(last=False) # FIFO, not LIFO
            return job
        except KeyError, e: # if dictionary is empty
            raise StopIteration
