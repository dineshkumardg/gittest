import os.path
from gaia.utils.lock import Lock

class WorkerJobLock(Lock):
    def __init__(self, item_name, config):
        lock_fpath = os.path.join(config.working_dir, 'ingest_worker_job_%s.lock' % item_name)
        lock_period = 4 * 60 * 60   # 4 hour expiry (to allow for 1000 page items!)
        Lock.__init__(self, lock_fpath, lock_period)
