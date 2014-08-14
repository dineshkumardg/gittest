import os
from gaia.utils.lock import Lock
from gaia.dom.store.versioned_item_store import VersionedItemStore

class LockableVersionedItemStore(VersionedItemStore):
    ''' A lockable VersionedItemStore: items can be locked to ensure single access

        Note that the user is responsible for locking and unlocking.
    '''
    _lock_fname = '_lock.lock'   # for want of a better name!... :)

    def __init__(self, root_dir, lock_mins=30):
        VersionedItemStore.__init__(self, root_dir)
        self.lock_mins = lock_mins # the time after which to consider an item lock expired (in minutes)
        self._locks = {}

    def lock(self, item_name, version_id):
        ''' Try to get a lock on the item. If the item cannot be locked, this will raise a LockError.

            Use this *before* adding assets (and make sure it is always UNlocked later!)
        '''
        item_dir = self._item_dir(item_name, version_id)
        lock_fpath = os.path.join(item_dir, self._lock_fname)
        lock = Lock(lock_fpath, self.lock_mins)   # try to grab a lock    # throws LockError on fail

        key = item_name + str(version_id)
        self._locks[key] = lock

    def lock_renew(self, item_name, version_id):
        key = item_name + str(version_id)
        if self._locks.has_key(key):
            self._locks[key].renew()

    def unlock(self, item_name, version_id):
        key = item_name + str(version_id)
        if self._locks.has_key(key):
            self._locks[key].unlock()
            del self._locks[key]

    def _get_asset_fnames(self, item_dir):
        fnames = os.listdir(item_dir)
        fnames = sorted(fnames)
        return [fname for fname in fnames if not fname == self._lock_fname]
