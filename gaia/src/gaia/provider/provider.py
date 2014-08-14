import os
from gaia.log.log import Log
from gaia.error import GaiaError, GaiaErrors
from gaia.utils.ftp import FtpError
from gaia.utils.lock import LockError
from gaia.utils.now import now
from gaia.gtp.gtp_site import GtpSite
from gaia.gtp.gtp_status import GtpStatus
from gaia.gtp.manifest import Manifest
from gaia.gtp.manifest_error import MissingManifestError
from gaia.provider.provider_error import ProviderError, TransferError, TransferAbort


class Provider(GtpSite):
    ''' Represents a Provider of Content to the Gaia system.

        Supplies methods to interact with the Provider regarding a specific project.
        Follows the Gaia Transfer Protocol when interacting with the Provider.

        Uses a "transfer_agent" to make file transfers (this is "gaia.utils.Ftp alike).
    '''

    def __init__(self, name, transfer_agent, config):
        GtpSite.__init__(self, config.project_code)
        self.config = config
        self.name = name
        self.transfer_agent = transfer_agent    # eg a gaia.util.Ftp object (or something that supports our File Transfer API)
        self._log = Log.get_logger(self)

        self._empty_file_fpath = self._empty_file()

    def _empty_file(self):
        'Create an empty file to be used for status files '
        fpath = os.path.join(self.config.working_dir, 'empty_file.txt')  # this can be shared.
        if not os.path.exists(fpath):
            f = open(fpath, 'w')
            f.close()  # Note: creates an empty file

        return fpath

    def list_new_items(self):   # raises FtpError
        ''' Get a list of items that we have not seen before.

            items are returned with their group names, ie as (group, item_nmae) pirs.
            (Note that this will mark those items as "processing")

            WARNING: a side_effect of this method is to change the working directory in the transfer_agent.
            Code should be written to cd() whenever required. (?)
        '''
        ta = self.transfer_agent
        new_items = []

        for group in ta.ls(self.items_dir):  # for group in groups
            group_dir = '%s/%s' % (self.items_dir, group)

            for item_name in ta.ls(group_dir):
                item_dir = '%s/%s/%s' % (self.items_dir, group, item_name)
                fnames = ta.ls(item_dir)

                if GtpStatus.is_ready(fnames):
                    ta.cd(item_dir)
                    ta.put(self._empty_file_fpath, remote_fname=GtpStatus.PROCESSING_FNAME)  # change the status to "processing" (from "ready")
                    new_items.append((group, item_name))
                else:
                    if GtpStatus.is_processing(fnames):
                        self._log.info('item "%s" is already being processed' % item_name)
                    else:
                        self._log.debug('item "%s" is NOT ready yet (fnames="%s")' % (item_name, str(fnames)))

        self._log.info('Provider "%s": new items "%s"' % (self.name, str(new_items)))
        return new_items

    def get_item(self, group, item_name, inbox, _manifest_class=Manifest):
        ''' Transfer a set of files for ONE item (within a group) to the inbox.

            Return the newly pulled assets (for reference).
            or raise a AbortTransfer exception if we cannot do anything at all (eg if item is locked).
        '''
        self._log.info(item_name=item_name)
        ta = self.transfer_agent
        new_assets = []
        errors = []

        try:
            inbox.lock(item_name)
            item_dir = self.item_dir(group, item_name)
            ta.cd(item_dir)

            remote_fnames = ta.ls()

            self._log.info('# A: get the manifest file (and info) first')
            fname = Manifest.fname
            if fname not in remote_fnames:
                raise MissingManifestError(group, item_name)

            new_asset = inbox.new_asset(fname, item_name)  # TODO: review and revise copy() method????? TUSH
            ta.copy(fname, new_asset)
            manifest = _manifest_class(new_asset.fpath)
            checksums = manifest.checksums()  # from manifest

            manifest_fnames = checksums.keys()

            # delete the manifest file from the inbox (we're done with it)
            #inbox.delete_asset(new_asset, item_name)

            self._log.info('# B: get the files referenced in the manifest and check their checksums (Note: ignores any files that are not in the manifest)')
            for fname in manifest_fnames:
                self._log.info(fname)

                if fname not in remote_fnames:
                    errors.append(TransferError('A file ("%s") is in the manifest but is NOT available in item folder "%s", group "%s"!' % (fname, item_name, group)))
                    continue    # pick up all possible errors in one pass

                # Hmm.. not sure that we should copy things if there are already errors...
                # The benefit is that we can checksum them..but we know we'll throw them away later.
                # is better for reporting errors, but is a waste of resources. TODO: review.

                try:
                    new_asset = inbox.new_asset(fname, item_name)
                    ta.copy(fname, new_asset, checksums[fname])  # copy the remote file "into" the inbox (and confirm the checksum)

                    new_assets.append(new_asset)
                    inbox.lock_renew(item_name)
                except LockError, e:
                    self._log.error(e)
                    raise   # if the renew lock fails, we need to abort (see below)
                except GaiaError, e:
                    self._log.warn(e)
                    errors.append(TransferError(str(e)))  # find as many errors as possible (rather than aborting on first one).

        except LockError, e:
            raise TransferAbort(str(e))  # Note that this will be raised (unlike the other errors) to ABORT this operation (rather than a "normal" failure)
        except GaiaErrors, e:
            errors.extend(e.errors)
        except GaiaError, e:    # includes LockError
            errors.append(e)
        finally:
            inbox.unlock(item_name)

        self._log.exit(num_new_assets=len(new_assets), num_errors=len(errors))
        return new_assets, errors

    def delete_item(self, group, item_name):
        ' Delete an item from the Providers site. '
        self._log.enter()
        ta = self.transfer_agent

        # Q: can you just do an rmdir and it delete the file sin the folder?? TODO
        try:
            ta.cd('%s/%s/%s' % (self.items_dir, group, item_name))
            fnames = ta.ls()
            for fname in fnames:
                ta.delete(fname)

            ta.cd('..')
            ta.rmdir(item_name)
        except FtpError, e:
            msg = 'Error deleting item "%s" from provider "%s" (err="%s")' % (item_name, self.name, e)
            self._log.error(msg)
            self._log.exit()
            raise ProviderError(msg)

        self._log.exit()

    def ok(self, group, item_name, report_fpath):
        ''' Write a "good" report for an item and delete the item
            (as per the Gaia Transfer Protocol)
        '''
        self._log.enter()
        self._report(item_name, report_fpath, is_good=True)
        self.delete_item(group, item_name)
        self._log.exit()

    def failed(self, group, item_name, report_fpath):
        ''' Write a "bad" report for an item and delete the item
            (as per the Gaia Transfer Protocol)
        '''
        self._log.enter()
        self._report(item_name, report_fpath, is_good=False)
        self.delete_item(group, item_name)
        self._log.exit()

    def _report(self, item_name, report_fpath, is_good):
        if is_good:
            self.transfer_agent.cd(self.reports_good_dir)
        else:
            self.transfer_agent.cd(self.reports_bad_dir)

        remote_fname = '%s_%s.txt' % (item_name, now())
        self.transfer_agent.put(report_fpath, remote_fname)
