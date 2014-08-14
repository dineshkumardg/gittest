from gaia.error import GaiaError
from gaia.dom.store.lockable_versioned_item_store import LockableVersionedItemStore
from gaia.dom.store.dom_index import _DomIndex
from gaia.dom.store.dom_file_store import _DomFileStore

class DomStore(LockableVersionedItemStore, _DomFileStore, _DomIndex):
    ''' A container for Storage of Gaia DOM Objects indexed by Item.

        add_item() provides _locked_ access to disallow concurrent access.

        Notes on this implementation:
            * VERSIONS existing content (by adding a new version with all new ids).
            * uses django models in a database as an index.
            * stores data in the filesystem
    '''

    def change_item_info(self, item_index, doc_info_changes, page_info_changes, chunk_info_changes):
        self._log.info('*** CHANGING ITEM ***:', item_index=item_index, doc_changes=doc_info_changes, page_changes=page_info_changes, chunk_changes=chunk_info_changes)

        # TODO think django transaction issues?
        _DomIndex.mark_item_changed(item_index.id)    # test required... TODO
        _DomFileStore.change_item_info(self, item_index.dom_name, item_index.id, doc_info_changes, page_info_changes, chunk_info_changes)

    def get_changes(self, dom_item):
        item_index = _DomIndex._get_live_index(dom_item)
        return _DomFileStore.get_changes(self, dom_item, item_index.id)

    def add_item(self, item):
        self._log.enter(item=item)
        item_index = None

        try:
            item_index, superceded = _DomIndex.add_item(self, item)
        except GaiaError, e:
            self._log.error('Failed to create an index for an item ("%s") in the dom_store ' % str(item), error=e)
            self._log.exit(item=item, error=e)
            raise

        # Note: can't do the following without an index
        try:
            self.lock(item.dom_name, item_index.id) # Note: can't lock until we have the index entry.

            LockableVersionedItemStore.add_item(self, item, item_index.id)
            if superceded:
                self._add_item(item, item_index.id, superceded.id)
            else:
                self._add_item(item, item_index.id, None)

            _DomFileStore.add_item(self, item, item_index.id)

            self.unlock(item.dom_name, item_index.id)

        except GaiaError, e:
            self._log.error('Failed to add an item ("%s") to the dom_store ' % str(item), error=e)
            # remove the entry from the index if anything goes wrong
            # (but note that we leave the files alone: might need to add delete here?). TODO
            # WARNING: this assumes that db ids will NOT be re-created..might not be true for some dbs (eg sqlite).
            _DomIndex.delete_item(self, item_index)
            self.unlock(item.dom_name, item_index.id)   # WARNING: this MUST NOT raise an error!...TODO: review
            raise

        self._log.exit(item=item)

    def _add_item(self, item, item_index_id, superceded_item_index_id):
        pass # template pattern: slot code in here to extend add_item() functionality
