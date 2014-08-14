import time
import os.path
import ftplib
import hashlib
from gaia.log.log import Log
from gaia.error import GaiaError
import cStringIO


class FtpError(GaiaError):
    pass


class Ftp:
    # 5 days worth of attempts = every 5 mins, 1440 times
    def __init__(self, server, uid, pwd, initial_dir=None, timeout_secs=10 * 60, retry_counter=1440, retry_timer=320):  # TODO change retry_counter to use project_counter.retry_counter
        self._log = Log.get_logger(self)
        self._log.info('connecting to server "%s", uid="%s", pwd="****")' % (server, uid))
        self.server = server
        self.uid = uid
        self.pwd = pwd
        self.initial_dir = initial_dir
        self._connected = False
        self._cwd = '/'  # track the current working directory on the server
        self._file = None   # Used by get method
        self._hash = None
        self.ftp = None
        self.timeout = timeout_secs

        self.retry_counter = int(retry_counter)  # to retry an ftp connection after its 'lost'
        self.retry_connection_attempts = 0
        self.retry_timer = int(retry_timer)  # time gap between each retry

    def open(self):
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not connect to FTP Server (server="%s", uid="%s", pwd="****")' % (self.server, self.uid))

        while not self._connected:
            try:
                self._log.info("Connecting to FTP Server %s; retrying after %s seconds; attempt %s/%s" % (self.server, self.retry_timer, self.retry_connection_attempts, self.retry_counter))
                # Note: SO_LINGER will make the socket.close() or shutdown() calls eventually timeout.
                # but ftplib seems to not use this, so close() calls WILL (potentially) hang.
                # ref: http://linux.die.net/man/7/socket
                # All other data calls will use the main timeout value below.

                self.ftp = ftplib.FTP(self.server, timeout=self.timeout)
                #self.ftp.set_debuglevel(self.debug_level) # 2 = max, 1 = 1 line per request; 0 = none
                self.ftp.login(self.uid, self.pwd)
                self._connected = True
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not connect to FTP Server (server="%s", uid="%s", pwd="****", err="%s")' % (self.server, self.uid, str(e)))

                self._log.warn("Unable to connect to FTP Server %s" % self.server)
                time.sleep(self.retry_timer)

        if self.initial_dir:
            self.cd(self.initial_dir)

        self._cwd = self._get_cwd()

    def _get_cwd(self):
        ' check the current working directory on the server '
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not get the current working directory on FTP Server (server="%s", uid="%s", pwd="****")' % (self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:

            try:
                cwd = self.ftp.pwd()    # Note ftp uses "present" working directory; we're using the os.getcwd() style "current" working directory convention
                self._log.info('cwd on the server is reported as "%s"' % cwd)
                return cwd
            except  ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not get the current working directory on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def close(self):
        try:
            if self._connected:
                self._log.info('quitting')
                self.ftp.voidcmd('QUIT')

        except  ftplib.all_errors, e:
            self._log.warning('Could not cleanly quit the connection to the FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (self.server, self.uid, str(e)))
        finally:
            self._connected = False

            if self.ftp.file is not None:
                self.ftp.file.close()
            if self.ftp.sock is not None:
                self.ftp.sock.close()
            self.ftp.file = self.ftp.sock = None

    def cd(self, path):
        ' change to a directory on the _server_ '
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not cd to directory "%s" on FTP Server (server="%s", uid="%s", pwd="****")"' % (path, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('cd to "%s"; attempt %s/%s' % (path, self.retry_connection_attempts, self.retry_counter))

            try:
                self.ftp.cwd(path)
                self._cwd = path
                break
            except  ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not cd to directory "%s" on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (path, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def ls(self, dir_path=None):
        ''' List names of files _and_ directories in the current folder (or dir_path) on the remote server

            If dir_path is supplied it must exist on the remote server (else FtpError("Directory Not Found") )
        '''
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('ls command failed (server="%s", uid="%s", pwd="****")' % (self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            try:
                if dir_path:
                    fpaths = self.ftp.nlst(dir_path)
                    self._log.info('ls (dir_path="%s"): got fpaths="%s"; attempt %s/%s' % (dir_path, str(fpaths), self.retry_connection_attempts, self.retry_counter))
                    len_prefix = len(dir_path)
                    return [fpath[len_prefix + 1:] for fpath in fpaths]  # strip the leading path component.
                else:
                    fpaths = self.ftp.nlst()
                    self._log.info('ls (dir_path="%s"): got fpaths="%s"; attempt %s/%s' % (dir_path, str(fpaths), self.retry_connection_attempts, self.retry_counter))
                    return fpaths
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('ls command failed (server="%s", uid="%s", pwd="****"), err="%s"' % (self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def get(self, source_fname, target_fpath):
        ' Get file (source_fname) from the current working directory and save it to target_fpath'
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not get file "%s" from FTP Server (server="%s", uid="%s", pwd="****")' % (source_fname, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('getting file "%s" into target path "%s"; attempt %s/%s' % (source_fname, target_fpath, self.retry_connection_attempts, self.retry_counter))
            try:
                self._file = open(target_fpath, 'wb')
                self.ftp.retrbinary('RETR ' + source_fname, self._handle_blocks)

                try:
                    self._file.close()
                except Exception as e:
                    self._log.info(str(e), message=e.message)

                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not get file "%s" from FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (source_fname, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def put(self, fpath, remote_fname=None):
        ' Take a file and put the file into the current working dir on the server (with an optional remote name: defaults to same as source fname)'
        # Note that we always (only) use BINARY transfers.
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not create remote file "%s" in directory "%s" (from "%s") on FTP Server (server="%s", uid="%s", pwd="****")' % (remote_fname, self._cwd, fpath, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            if not remote_fname:
                remote_fname = os.path.basename(fpath)

            try:
                self._log.info('putting "%s" into dir "%s" with remote fname "%s"; attempt: %s/%s' % (fpath, self._cwd, remote_fname, self.retry_connection_attempts, self.retry_counter))
                f = open(fpath, 'rb')
                self.ftp.storbinary('STOR %s' % remote_fname, f)
                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not create remote file "%s" in directory "%s" (from "%s") on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (remote_fname, self._cwd, fpath, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def write(self, fname, contents):
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not create remote file "%s" in directory "%s" (from "%s") on FTP Server (server="%s", uid="%s", pwd="****")' % (fname, self._cwd, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            try:
                self._log.info('write "%s" into dir "%s"; attempt: %s/%s' % (fname, self._cwd, self.retry_connection_attempts, self.retry_counter))
                self.ftp.storbinary('STOR %s' % fname, cStringIO.StringIO(contents))
                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not create remote file "%s" in directory "%s" (from "%s") on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (fname, self._cwd, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def copy(self, source_fname, to_file, required_checksum=None):
        ''' Get file (source_fname) from the current working directory and copy it to
            the to_file (should be an open ('wb' mode) file object)

            If a required_checksum is provided, it will be checked to
            make sure the transfer worked, and that the checksum of the
            file after the transfer matches the required_checksum.
        '''
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not get file "%s" from FTP Server (server="%s", uid="%s", pwd="****")' % (source_fname, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('copying file "%s" into target file "%s"; attempt: %s/%s' % (source_fname, to_file.name, self.retry_connection_attempts, self.retry_counter))
            self._file = to_file

            if required_checksum:
                self._hash = hashlib.md5()

            try:
                self.ftp.retrbinary('RETR ' + source_fname, self._handle_blocks)
                if required_checksum:
                    file_checksum = self._hash.hexdigest()
                    if required_checksum != file_checksum:
                        raise FtpError('Checksum mismatch for file "%s" (required checksum="%s", but this file has checksum="%s")' % (to_file.name, required_checksum, file_checksum))

                try:
                    self._file.close()
                except Exception as e:
                    self._log.info(str(e), message=e.message)

                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1
                self._hash = None

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not get file "%s" from FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (source_fname, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def delete(self, fpath):
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not delete file "%s" from directory "%s" on FTP Server (server="%s", uid="%s", pwd="****")' % (fpath, self._cwd, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('deleting "%s"; attempt: %s/%s' % (fpath, self.retry_connection_attempts, self.retry_counter))

            try:
                self.ftp.delete(fpath)
                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not delete file "%s" from directory "%s" on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (fpath, self._cwd, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def rmdir(self, dir_path):
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not delete directory "%s" from directory "%s" on FTP Server (server="%s", uid="%s", pwd="****")' % (dir_path, self._cwd, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('deleting directory "%s"; attempt: %s/%s' % (dir_path, self.retry_connection_attempts, self.retry_counter))

            try:
                self.ftp.rmd(dir_path)
                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not delete directory "%s" from directory "%s" on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (dir_path, self._cwd, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def rename(self, from_name, to_name):
        if self.retry_connection_attempts > self.retry_counter:
            raise FtpError('Could not rename "%s" to "%s" on FTP Server (server="%s", uid="%s", pwd="****")' % (from_name, to_name, self.server, self.uid))

        while self.retry_connection_attempts < self.retry_counter:
            self._log.info('renaming "%s" to "%s"; attempt: %s/%s' % (from_name, to_name, self.retry_connection_attempts, self.retry_counter))

            try:
                self.ftp.rename(from_name, to_name)
                break
            except ftplib.all_errors, e:
                self.retry_connection_attempts += 1

                if self.retry_connection_attempts >= self.retry_counter:
                    raise FtpError('Could not rename "%s" to "%s" on FTP Server (server="%s", uid="%s", pwd="****"), err="%s"' % (from_name, to_name, self.server, self.uid, str(e)))
                else:
                    self.close()
                    self.open()

    def _handle_blocks(self, block):
        self._file.write(block)

        if self._hash:
            self._hash.update(block)

    # aliases for unix-like method naming
    rm = delete
    mv = rename
    cp = copy
