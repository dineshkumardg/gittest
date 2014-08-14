import os
import shutil
from gaia.dom.store.lockable_versioned_item_store import LockableVersionedItemStore
from gaia.asset.asset import Asset
from gaia.store.store_error import StoreError


class DocBox(LockableVersionedItemStore):            
    ''' This is a staging area to collect together gift DOCument instances
        prior to transfer.

        *** THIS IS A HACK! ***

        We're re-using the dom store class LockableVersionedItemStore
        and instead of a version, we're using group-name, and the item
        is a "transfer_item", where:
            item.assets = the assets are document_instances.
            item.dom_name = the item name + version

        Here's the interface (instead of a version_id, we're using a group_name):
            lock(item_name, feed_group_name):
            lock_renew(item_name, feed_group_name):
            unlock(item_name, feed_group_name)

            #add_item(item, feed_group_name):    # or item+name? TODO
            add_asset(asset, item_name, feed_group_name):
            assets(item_name, feed_group_name):
            new_asset(asset_fname, item_name, feed_group_name):

            delete_item(item_name, group):
            exists(item_name, group):   - does this group exist for this item

        WARNING: This is less-optimally grouped by item/feed_group rather than
        group/item which might be more appropraite for thos DocBox (this is a hacky quick win! :( ) TODO?
        However, this might be useful for tracking?

    '''
    def transfer_item_names(self):
        ' return a list of transfer-item names '
        return os.listdir(self._root_dir)
    
    def real_item_names(self):
        ' return a mapping from "transfer_item_names" to "real" item_name '
        return {item_name_with_version: item_name_with_version.rsplit('_', 1)[0] for item_name_with_version in os.listdir(self._root_dir)} # YUK: TODO: refactor/change/remove this hacky class!
        #return [item_version.rsplit('_', 1)[0] for item_version in os.listdir(self._root_dir)] # YUK: TODO: refactor/change/remove this hacky class!
    
    def delete_item(self, item_name, group):
        ' delete the assets for one group within an item '
        item_dir = os.path.join(self._root_dir, item_name)
        group_dir = os.path.join(item_dir, group)

        shutil.rmtree(group_dir)

        if not os.listdir(item_dir):    # if there are no groups left, delete the item folder as well.
            shutil.rmtree(item_dir)


    def exists(self, item_name, group):
        ' does this group exist for this item '
        group_dir = os.path.join(self._root_dir, item_name, group)
        return os.path.exists(group_dir)

    # ***** TODO ******
    # NOTE WELL: TODO: This is temporarily ioverridden here to fix feed fiel generation.
    # We should move this fix (for "Too many open files) to the base classes
    # in gaia/dom/store and run full system testing (ie especially of webbox)
    #
    # (there are more than 1024 document instances in one feed).
    # the fix is in gaia/store/item_store, but not in similar classes in gaia/dom/store! )
    # ***** TODO ******
    def assets(self, item_name, version_id):    # @override to fix Too Many Open Files (ref EG-277)
        ' Get all the assets for item_name '
        assets = []

        item_dir = self._item_dir(item_name, version_id)
        try:
            
            fnames = self._get_asset_fnames(item_dir)
    
            #for fname in fnames:
                #fpath = os.path.join(item_dir, fname)
                #assets.append(Asset(fpath))
                
            for fname in fnames:
                 fpath = os.path.join(item_dir, fname)
                 asset = Asset(fpath) # open the file for reading, then close it immediately.
                 asset.close()        # .. as we only really need the fname! - Need to do this otherwise could encounter 'Too many open files' error (file descriptor limit) ref: ulimit -n xxx
                 assets.append(asset)

        except (OSError, IOError), e:
            raise StoreError('Error getting assets from item_dir "%s". Err: "%s"' % (item_dir, str(e)))

        return assets
