import os
import time
from gaia.log.log import Log
from datetime import datetime, timedelta
from gaia.error import GaiaError


class LockError(GaiaError):
    pass


class Lock():
    ''' A Lock is a file on disk that is used to provide locking functionality. 
        The lock is obtained when the lock object is created.
        The lock will expire after a given amount of time (in seconds) or when it's unlocked.

        The expiry time can be extended by "renew"ing the lock.
        Some information is stored in the file purely for informational/debugging purposes.
    '''

    def __init__(self, lock_fpath, lock_period):
        self._log = Log.get_logger(self)
        self.lock_fpath = lock_fpath
        self.lock_period = timedelta(seconds=lock_period)

        if self._is_locked() and not self. _is_expired():
            msg = 'Already locked: %s' % self.lock_fpath
            self._log.warn('lock FAILED: ' + msg)
            raise LockError(msg)

        self._lock()

    def unlock(self):
        if self._is_locked():
            try:
                os.remove(self.lock_fpath)
                self._log.debug('Unlocked: %s' % self.lock_fpath)
            except OSError, e:  # Windwos will raise WindowsError(OSError) sometimes :( (unix is fine!)
                self._log.warning('Unlocking: %s FAILED & ignored (error="%s")' % (self.lock_fpath, str(e)))

    def renew(self):
        ' Anyone can renew the lock (callers MUST try to get a lock and have a lock before trying to renew!) '
        self._lock()

    def _is_locked(self):
        return os.path.isfile(self.lock_fpath)

    def _is_expired(self):
        lock_time, pid = self._read()
        return (datetime.utcnow() - lock_time) > self.lock_period

    def _lock(self):
        self._log.debug('Locking: %s' % self.lock_fpath)
        try:
            lock_file = open(self.lock_fpath, 'w+')
            lock_time = time.time()
            lock_file.write('%f\n%d' % (lock_time, os.getpid()))
            lock_file.close()
        except IOError, e:
            raise LockError('Error writing lock file "%s" (err="%s")' % (self.lock_fpath, str(e)))

    def _read(self):
        try:
            lock_file = open(self.lock_fpath, 'r')
        except IOError, e:
            raise LockError('Error reading lock file "%s" (err="%s")' % (self.lock_fpath, str(e)))

        lines = lock_file.readlines()
        if len(lines) != 2:
            raise LockError('Wrong number of lines (%d) read from lock file in "%s"' % (len(lines), self.lock_fpath))
        else:
            try:
                ts = float(lines[0])
                lock_time = datetime.utcfromtimestamp(ts) # check gmtime range of values
            except ValueError, e:
                raise LockError('Unable to read timestamp from file "%s" (Line="%s")' % (self.lock_fpath, lines[0]))

            try:
                pid = int(lines[1])
            except ValueError, e:
                raise LockError('Unable to read PID from file "%s" (Line="%s")' % (self.lock_fpath, lines[1]))

        return lock_time, pid
