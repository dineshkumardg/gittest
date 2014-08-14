import os
from gaia.utils.lock import Lock
from gaia.store.item_store import ItemStore

class LockableItemStore(ItemStore):
    ''' A lockable ItemStore: items can be locked to ensure single access

        Note that the user is responsible for locking and unlocking.
    '''
    _lock_fname = '_lock.lock'   # for want of a better name!... :)

    def __init__(self, root_dir, lock_mins=30):
        ItemStore.__init__(self, root_dir)
        self.lock_mins = lock_mins # the time after which to consider an item lock expired (in minutes)
        self._locks = {}

    def lock(self, item_name):
        ''' Try to get a lock on the item. If the item cannot be locked, this will raise a LockError.

            Use this *before* adding assets (and make sure it is always UNlocked later!)
        '''
        item_dir = self._item_dir(item_name)
        lock_fpath = os.path.join(item_dir, self._lock_fname)
        lock = Lock(lock_fpath, self.lock_mins)   # try to grab a lock    # throws LockError on fail
        self._locks[item_name] = lock

    def lock_renew(self, item_name):
        if self._locks.has_key(item_name):
            self._locks[item_name].renew()

    def unlock(self, item_name):
        if self._locks.has_key(item_name):
            self._locks[item_name].unlock()
            del self._locks[item_name]

    def _get_asset_fnames(self, item_dir):
        fnames = os.listdir(item_dir)
        return [fname for fname in fnames if not fname == self._lock_fname]
