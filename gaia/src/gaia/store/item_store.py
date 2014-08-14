import shutil
import os.path
from gaia.log.log import Log
from gaia.asset.asset import Asset
from gaia.store.store_error import StoreError

class ItemStore:
    ''' A container for Storage of Items .

        Items are groups of asset files optionally with data objects.
        
        An item must have a dom_name.

        This implementation groups files by item in the file system.
        This implementation OVERWRITES existing content (create_or_replace).
    '''
    def __init__(self, root_dir):
        self._log = Log.get_logger(self)
        self._root_dir = root_dir
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        #Hmm.. when used in a django app this is a different logger!! :((((
        #self._log.debug(root_dir=root_dir)

    def add_item(self, item):
        self._log.enter(item=item)

        for asset in item.assets:
            self.add_asset(asset, item.dom_name)

        self._log.exit()

    def delete_item(self, item):
        self._log.enter(item=item)

        item_dir = os.path.join(self._root_dir, item.dom_name)

        if os.path.exists(item_dir):
            try:
                shutil.rmtree(item_dir)
            except (IOError, OSError), e:
                raise StoreError('Could not delete item', item_dir=item_dir, err=str(e))

        self._log.exit()

    def add_asset(self, asset, item_name):
        ' put an asset (for an item) into this container '
        item_dir = self._item_dir(item_name)
        try:
            self._log.debug('adding asset "%s" into "%s"' % (asset.fpath, item_dir))
            shutil.copy(asset.fpath, item_dir)
        except IOError, e:
            raise StoreError('Error adding asset "%s" to item "%s". Err: "%s"' % (asset.fpath, item_name, e))

    def new_asset(self, asset_fname, item_name):
        ' create a new writable asset(file) in this container and return it '
        item_dir = self._item_dir(item_name)

        fpath = os.path.join(item_dir, asset_fname)
        asset = Asset(fpath, 'wb')
        return asset

    def delete_asset(self, asset, item_name):
        ' remove an asset (for an item) from this container '
        item_dir = self._item_dir(item_name)
        fpath = os.path.join(item_dir, asset.fname)

        try:
            os.remove(fpath)
        except (IOError, OSError), e:
            raise StoreError('Error deleting asset "%s" (err="%s")' % (fpath, e))

    def assets(self, item_name):
        ' Get all the assets for item_name: WARNING: these assets are *CLOSED* files! '
        assets = []

        item_dir = os.path.join(self._root_dir, item_name)

        if not os.path.exists(item_dir):
            return []

        try:
            fnames = self._get_asset_fnames(item_dir)
    
            for fname in fnames:
                fpath = os.path.join(item_dir, fname)
                asset = Asset(fpath) # open the file for reading, then close it immediately.
                asset.close()        # .. as we only really need the fname! - Need to do this otherwise could encounter 'Too many open files' error (file descriptor limit)
                assets.append(asset)
                
        except EnvironmentError, e:
            raise StoreError('Error getting assets from item_dir "%s". Err: "%s"' % (item_dir, str(e)))
        
        return assets

    def _get_asset_fnames(self, item_dir):
        return os.listdir(item_dir)

    def item_dir(self, item):
        ' return the item directory for an item '
        return os.path.join(self._root_dir, str(item.dom_name))

    def _item_dir(self, item_name):# can be used in subclasses.
        ' return the item directory for an item and create it if necessary '
        # TODO: maybe in subclasses (eg WebBox) make this split the item name (eg on separators??) - or do the yyyy/mm/dd/ thing for newspapers etc
        item_dir = os.path.join(self._root_dir, str(item_name))

        if not os.path.exists(item_dir):
            os.makedirs(item_dir)

        return item_dir
