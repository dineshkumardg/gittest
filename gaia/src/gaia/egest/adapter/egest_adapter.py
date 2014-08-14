from gaia.error import GaiaError
from gaia.log.log import Log
from gaia.utils.ftp import Ftp


class EgestAdapterError(GaiaError):
    pass


class EgestAdapter:
    ftp_class = Ftp

    def __init__(self, config, **adapter_params):
        self.log = Log.get_logger(self)
        self.config = config
        self.params = adapter_params
        self.ftp_args = adapter_params

    def _transfer(self, fpaths): 
        ftp = self.ftp_class(**self.ftp_args)
        ftp.open()

        for fpath in fpaths:
            ftp.put(fpath) # TODO: failures? retry? delete other successfully delivered files?

        ftp.close()
