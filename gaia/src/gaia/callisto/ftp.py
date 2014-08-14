import os
from gaia.utils.ftp import Ftp

class CallistoFtp(Ftp):

    sending_suffix = '_sending'

    def put(self, fpath): # Override
        ''' Take a file and put the file into the current working dir on the server (with an optional remote name: defaults to same as source fname)
            Append "_sending" to the destination file name while sending then remove it when finished sending. 
        '''

        remote_fname = os.path.basename(fpath)
        remote_fname_sending = remote_fname + self.sending_suffix
        Ftp.put(self, fpath, remote_fname_sending)
        self.rename(remote_fname_sending, remote_fname)
