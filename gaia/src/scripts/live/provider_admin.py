from gaia.gtp.gtp_status import GtpStatus
from gaia.provider.provider import Provider

# WARNING: UNTESTED!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!! DO NOT USE!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class ProviderStatus:
    ' A Data Object to encapsulate status data '

    def add(self, item_name, item_status, group, item_dir):
        self._items[item_name] = (item_status, item_dir, group)

    def items_name(self):
        ' return just the names of all the items on the Provider '
        return self._items.keys()

    def items_name_status(self):
        ' return name, status for all the items on the Provider '
        return [(item_name, self._items[item_name][0]) for item_name in self._items]

    def items_fpath(self):
        ' return the provider (remote) path of all items '
        return [(item_name, self._items[item_name][1]) for item_name in self._items]

    def items_status_processing(self):
        ' return a list of all items which are in status PROCESSING '
        return [item_name for item_name in self._items if self._items[item_name][0] == GtpStatus.PROCESSING]

    def items_status_ready(self):
        ' return a list of all items which are in status READY '
        return [item_name for item_name in self._items if self._items[item_name][0] == GtpStatus.READY]

    def items_status_not_ready(self):
        ' return a list of all items which are in status NOT_READY '
        return [item_name for item_name in self._items if self._items[item_name][0] == GtpStatus.NOT_READY]

    def item_dir(self, item_name):
        ' return the directory path (dpath?( for an item on the provider site '
        return self._items[item_name][1]


class ProviderAdmin(Provider):
    ''' A ProviderAdmin adds management/administration capablity to a Provider.
    
        This is separated from the Provider because normal usage
        should *not* require any management features, these are typically
        for troubleshooting; fixing; unusual maintenance sceanrios only.

        Remember that the Provider is *** someone else's FTP site! ***
    '''

    def __init__(self, name, transfer_agent, config):
        Provider.__init__(self, name, transfer_agent, config)

    def status(self):   # raises FtpError
        ''' Check the status of all items that are present on the Provider's site.

            Returns a ProviderStatus object

            (WARNING: a side_effect of this method is to change the working directory in the transfer_agent.
             Code should be written to cd() whenever required. (?))
        '''
        ta = self.transfer_agent
        status = ProviderStatus()

        for group in ta.ls(self.items_dir): # for group in groups
            group_dir = '%s/%s' % (self.items_dir, group)

            for item_name in ta.ls(group_dir):
                item_dir = '%s/%s/%s' % (self.items_dir, group, item_name)
                fnames = ta.ls(item_dir)

                item_status = GtpStatus.status(fnames)
                status.add(item_name, item_status, group, item_dir)

        return status

    def revert_from_processing_to_ready(self):
        status = self.status()
        processing_items = status.items_status_processing()

        for item_name in processing_items:
            self._revert_to_ready(item_name, status.item_dir(item_name))

    def _revert_to_ready(self, item_name, item_dir):
        print "TODO: remove _status_PROCESSING.txt from: ", item_dir
