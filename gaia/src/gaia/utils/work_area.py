import os
import shutil
import tempfile
from gaia.error import GaiaError
from gaia.log.log import Log

class WorkAreaError(GaiaError):
    pass

class WorkArea:
    ''' A unique, temporary work area (folder) that will be created 
        within the general working_data area (as configured).

        You can find out where the work area has been
        created through the path attribute and then create
        files in that area. list the file paths with ls().

        The work area should be deleted with remove() when
        you've finished.

        You can use the prefix parameter to help traceability
        (eg by using "myfunction1_pid27": defaults to "work_area")
    '''
    
    def __init__(self, config, prefix='work_area'):
        self._log = Log.get_logger(self)
        
        try:
            root_dir = os.path.join(config.working_dir)
            self.path = tempfile.mkdtemp(dir=root_dir, prefix=prefix + '_')
            self._log.debug('created work area', work_area=self.path)
        except OSError, e:
            raise WorkAreaError('Problem creating WorkArea', root_dir=root_dir, err=str(e))
    
    def ls(self):
        ' return fpaths of files within work area '
        fnames = os.listdir(self.path)
        return [os.path.join(self.path, fname) for fname in fnames]
    
    def remove(self):
        try:
            self._log.debug('removing WorkArea', dir=self.path)
            shutil.rmtree(self.path)
        except OSError, e:
            raise WorkAreaError('Could not clean up WorkArea', dir=self.path, err=str(e))
