from gaia.callisto.ftp import CallistoFtp
from gaia.callisto.callisto_zip import CallistoZip
from gaia.egest.adapter.egest_adapter import EgestAdapter, EgestAdapterError
from gaia.error import GaiaError
from gaia.utils.work_area import WorkArea


class CallistoExportError(EgestAdapterError):
    pass


class CallistoEgestAdapter(EgestAdapter):
    platform_name = 'callisto'
    ftp_class = CallistoFtp

    def egest(self, transfer_prep_dir, item, item_index, release_type, *item_changes):
        self.log.enter(item=item)

        try:
            if release_type == 'callisto' or release_type == 'both':
                work_area = WorkArea(self.config, 'egest_'+self.platform_name)

                package = CallistoZip(self.config)
                package.create(item, work_area.path)

                self._transfer(work_area.ls())
                work_area.remove()

        except GaiaError, e:
            self.log.exit('FAILED', err=e)
            raise EgestAdapterError('Failed to transfer files to an export platform', error=e)

        self.log.exit()

    def flush(self, transfer_prep_dir):
        return
