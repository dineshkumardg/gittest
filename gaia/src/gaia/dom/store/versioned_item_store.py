import os
import shutil
from gaia.log.log import Log
from gaia.asset.asset import Asset
from gaia.store.store_error import StoreError

class VersionedItemStore:
    ''' A container for Storage of VERSIONS OF Items .

        Items are groups of asset files optionally with data objects.

        This implementation groups files by item in the file system.
        This implementation supports VERSIONS of items
    '''
    def __init__(self, root_dir):
        self._log = Log.get_logger(self)
        self._root_dir = root_dir
        if not os.path.exists(root_dir):
            os.makedirs(root_dir)

        #Hmm.. when used in a django app this is a different logger!! :((((
        #self._log.debug(root_dir=root_dir)

    def add_item(self, item, version_id):
        self._log.enter()

        for asset in item.assets:
            self.add_asset(asset, item.dom_id, version_id)

        self._log.exit()

    def add_asset(self, asset, item_name, version_id):
        ' put an asset (for an item) into this container '
        item_dir = self._item_dir(item_name, version_id)
        try:
            self._log.debug('adding asset "%s" into "%s"' % (asset.fpath, item_dir))
            shutil.copy(asset.fpath, item_dir)
        except IOError, e:
            raise StoreError('Error adding asset "%s" to item "%s". Err: "%s"' % (asset.fpath, item_name, e))

    def new_asset(self, asset_fname, item_name, version_id, is_binary=True):
        ' create a new writable asset(file) in this container and return it '
        item_dir = self._item_dir(item_name, version_id)

        fpath = os.path.join(item_dir, asset_fname)
        if is_binary:
            asset = Asset(fpath, 'wb')
        else:
            asset = Asset(fpath, 'w')

        return asset

    def assets(self, item_name, version_id):
        ' Get all the assets for item_name '
        assets = []

        item_dir = self._item_dir(item_name, version_id)
        try:
            
            fnames = self._get_asset_fnames(item_dir)
    
            for fname in fnames:
                fpath = os.path.join(item_dir, fname)
                assets.append(Asset(fpath))
                
        except (OSError, IOError), e:
            raise StoreError('Error getting assets from item_dir "%s". Err: "%s"' % (item_dir, str(e)))
        
        return assets

    def _item_dir(self, item_name, version_id, *args):
        ''' Return the item directory for an item and create it if necessary.
            Can be used in subclasses (a "friend" function) with extra path args
            to return an "extended" path relative to the item_dir.
        '''
        path_args = [self._root_dir, str(item_name), str(version_id)]
        path_args.extend([str(arg) for arg in args])
        item_dir = os.path.join(*path_args)

        if not os.path.exists(item_dir):
            os.makedirs(item_dir)

        return item_dir

    def _item_url(self, item_name, version_id):# can be used in subclasses (a "friend" function)
        ' return the root-relative item url for a version of an  item '
        return "%s/%s" % (str(item_name), str(version_id))

    def _get_asset_fnames(self, item_dir):
        return os.listdir(item_dir)
