import os
import os.path

class GaiaFolder:
    ''' A utility class for working with Directories/Folders
    '''
    @staticmethod
    def size(root_dir):
        ' return the total size of file-data within a folder'
        size = 0

        # but make sure we exclude any _lock.lock files, as a race condition might mean are no longer in os.walk list
        lock_file = '_lock.lock'
        for root, dirs, fnames in os.walk(root_dir):
            if lock_file in fnames:
                fnames.remove(lock_file)
            size += sum([os.path.getsize(os.path.join(root, fname)) for fname in fnames])

        return size

    @staticmethod
    def ls(root_dir):
        ' return a list of absolute fpaths of files *recursively* within this folder '
        #TODO: add a dont_recurse option (recursive=False)?
        #return os.listdir(root_dir)    # returns folder names too :(
        fpaths = []
        for root, dirs, fnames in os.walk(root_dir):    # Note: root is "." first time round.
            fpaths.extend([os.path.abspath(os.path.join(root, fname)) for fname in fnames])

        return fpaths
