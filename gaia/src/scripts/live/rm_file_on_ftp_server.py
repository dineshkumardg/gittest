'''
Script to recursively delete a specific file on a ftp server. 
'''
from gaia.log.log import Log
from gaia.utils.ftp import Ftp
import os
import logging
import socket


class Config:
    log_dir = os.path.dirname(__file__)
    log_fname = ',%s' % os.path.basename(__file__)
    log_level = logging.INFO
    #ftp_server = {'server':'127.0.0.1', 'uid':'htc', 'pwd':'qwerty123', 'group_dir':'/cho/items'}
    ftp_server = {'server':'ftp.htcindia.com', 'uid':'clemea-gaia', 'pwd':'CL3m3@123', 'group_dir':'/cho/items'}
    ftp_fname = '_status_PROCESSING.txt'


# Note: to be replaced (eventually) with a driver that uses the ProviderAdmin class: TODO
class RmFileOnFtpServer:
    def __init__(self, config):
        Log.configure_logging(config.log_fname, config, rollover=False)
        self._log = Log.get_logger(self)
        self._ftp_server = config.ftp_server
        self._config = config

    def find_file(self):
        self._log.enter()
        ftp = Ftp(self._ftp_server['server'], self._ftp_server['uid'], self._ftp_server['pwd'], initial_dir=self._ftp_server['group_dir'])

        found_file_list = []

        ftp.open()
        group_folders = ftp.ls()
        cwd = ftp._get_cwd()
        for group_folder in group_folders:
            group_cwd = '%s/%s' % (cwd, group_folder)
            ftp.cd(group_cwd)

            item_folders = ftp.ls()
            for item_folder in item_folders:
                item_cwd = '%s/%s' % (group_cwd, item_folder)
                ftp.cd(item_cwd)

                if self._config.ftp_fname in ftp.ls():
                    found_fpath = '%s/%s' % (ftp._get_cwd(), self._config.ftp_fname)
                    msg = 'FOUND: %s' % found_fpath
                    self._log.info(msg)
                    # print msg
                    found_file_list.append(found_fpath)

        ftp.close()
        self._log.exit()
        return found_file_list

    def rm_file(self, files_to_rm):
        self._log.enter()
        ftp = Ftp(self._ftp_server['server'], self._ftp_server['uid'], self._ftp_server['pwd'], initial_dir=self._ftp_server['group_dir'])
        ftp.open()

        for fpath_to_rm in files_to_rm:
            rdir = fpath_to_rm[0: fpath_to_rm.index(self._config.ftp_fname)]
            ftp.cd(rdir)
            self._log.info('DELETE: %s' % fpath_to_rm)
            ftp.delete(fpath_to_rm)

        ftp.close()
        self._log.exit()

if __name__ == '__main__':
    rm_file_on_ftp_server = RmFileOnFtpServer(Config)
    files_to_rm = rm_file_on_ftp_server.find_file()
    rm_file_on_ftp_server.rm_file(files_to_rm)
