import os
from gaia.utils.try_cmd import try_cmd, CommandError, CommandStartError
from gaia.error import GaiaError

class ArchiveError(GaiaError):
    _7z_ERROR_CODES = {
                      1: 'Warning (Non fatal error(s)). For example, one or more files were locked by some other application, so they were not compressed.',
                      2: 'Fatal error',
                      7: 'Command line error',
                      8: 'Not enough memory for operation',
                    255: 'User stopped the process',
                    }

class Archive:

    archive_file_ext = '7z'

    def __init__(self, zip_fpath):
        self.zip_fpath = zip_fpath

    def create(self, directory_to_zip, out_dir, archive_name):
        ' Zip root_dir into zip_fpath'
        destination_zip_fpath = os.path.join(out_dir, '%s.%s' % (archive_name, self.archive_file_ext))
        cmd = [self.zip_fpath, 'a', '-t7z', destination_zip_fpath, directory_to_zip]

        err_msg = self._run_zipcmd(cmd)

        if not err_msg:
            # Test the archive (because 7zip can fail silently on create :( )
            err_msg = self._test_zip_file(destination_zip_fpath)

        if err_msg:
            raise ArchiveError('Error when attempting to zip directory', dir=directory_to_zip, err=err_msg)
        
        return destination_zip_fpath
    
    def _run_zipcmd(self, cmd):
        err_msg = None

        try:
            try_cmd(*cmd)
        except CommandStartError, e:
            err_msg = '*** FAILED TO EXECUTE COMMAND "%s"' % ' '.join(cmd)
        except CommandError, e:
            retcode = e.retcode
            err_msg = '*** COMMAND ERROR "%s"' % ' '.join(cmd)
            if retcode in ArchiveError._7z_ERROR_CODES:
                err_msg += ' (%s)' % ArchiveError._7z_ERROR_CODES[retcode]
            else:
                err_msg += ' (%s)' % str(e)

        return err_msg

    def _test_zip_file(self, fpath):
        cmd = [self.zip_fpath, 't', fpath]
        err_msg = self._run_zipcmd(cmd)

        if err_msg:
            err_msg = '*** ZIP ERROR: zip file is corrupt, "test" of "%s" failed! (err="%s")' % (fpath, err_msg)

        return err_msg  # is None on success
