import sys
from django.conf import settings
from gaia.config.config import get_config
from gaia.config.config_errors import GaiaConfigurationError
from gaia.error import GaiaCodingError
from gaia.egest.egest_request import EgestRequest
from gaia.egest.jobs_done_request import JobsDoneRequest
import gc

# ----------------------------------------------------------
# Note: this lump of code is here so that django settings
# can be configured _before_ importing any Django modules
# eg from Item
# ----------------------------------------------------------
def usage():
    print
    print 'Usage: python egest_worker.py MY_CONFIG'
    print 'eg:'
    print '       python egest_worker.py STEW_LINUX'
    print

try:
    config = get_config(sys.argv[1])
    config.check()
except GaiaConfigurationError, e:
    print 'ERROR: BAD CONFIG:', str(e)
    usage()
    sys.exit(1)
except IndexError, e:
    print
    print 'ERROR: Please supply at least one argument, ie the config to use.'
    print
    usage()
    sys.exit(2)

settings.configure(**config.get_django_settings())

from qa.models import Item as QaItem
from gaia.dom.model.item import Item as DomItem
from gaia.error import GaiaError
from gaia.task.worker import Worker
from gaia.utils.lock import LockError
from gaia.utils.import_class import import_class
from gaia.web.web_box import WebBox
from gaia.egest.outbox import Outbox


class EgestWorker(Worker):
    process_name = 'egest_worker'

    def __init__(self, config):
        Worker.__init__(self, config.egest_job_sockets, config)

        self.config.max_requests_outstanding = config.egest_max_requests_outstanding
        self.config.response_threshold = config.egest_response_threshold
        self.config.poll_interval = config.egest_poll_interval   

        # instantiate one of each of the configured egest adapters
        self.adapters = []
        for adapter_class_name, adapter_params in self.config.egest_adapters:
            adapter = import_class(adapter_class_name)(self.config, **adapter_params)
            self.adapters.append(adapter)

    def do(self, job_request):
        self._log.info('Egesting =======================================', job_request=job_request)

        collected = gc.collect()
        self._log.info('gc egest.start collected %d objects' % collected)

        if isinstance(job_request, JobsDoneRequest):
            status = self.do_jobs_done()
        elif isinstance(job_request, EgestRequest):
            status = self.do_jobs(job_request)
        else:
            raise GaiaCodingError('egest_worker received unexpected message type', job_request=job_request, class_type=job_request.__class__)

        collected = gc.collect()
        self._log.info('gc egest.end collected %d objects' % collected)

        self._log.exit(status=status)
        return status

    def do_jobs(self, egest_request):
        status = self.FAILED    # by default we've failed to handle this job

        try:
            item_id = egest_request.item_id 
            item_name = egest_request.item_name
            release_type = egest_request.release_type

            outbox = Outbox(self.config.outbox)
            outbox.lock(item_name)

            assets = outbox.assets(item_name)
            item = DomItem(item_name, item_name, assets, self.config)

            # Fixes are made within the info objects held in the WebBox.
            # Not all of this content will have been changed, but it all _may_ be changed
            # (effectively a cache of _potentially_ "dirty" data)
            web_box = WebBox(self.config)
            item_changes = web_box.get_changes(item)    # Note: plain dicts (not json objects)
            item_index = web_box.item_index(item)

            # The transfer_prep_dir is a staging area (if required).
            # eg it's used by the CHO xml adapter to store intermediate gift document instances
            # but not used by the callisto adapter at all.
            for adapter in self.adapters:
                adapter.egest(self.config.transfer_prep_dir, item, item_index, release_type, *item_changes)  # uses: xml_egest_adapter and a callisto_egest_adapter

            if release_type == 'xml' or release_type == 'both':
                QaItem.set_released(item_id)
            elif release_type == 'callisto':
                # SH wants it so that if only we release to callisto then item moves back to QA state
                QaItem.set_qa(item_id)

            status = self.OK    # we're good only if we get this far.
            self._log.exit('Egesting success :-)')

            outbox.unlock(item_name)

        except LockError, e:
            self._log.warning('ooo ABORTing (TRY_AGAIN): lock error (job/outbox is locked by another worker?)', job_request=egest_request, lock_error=e)
            status = self.TRY_AGAIN

        except GaiaError, e:
            self._log.error('FAILED (putting item into error state):', item_name=item_name, error=e)
            QaItem.set_error(item_id, e.__class__.__name__, str(e)) # note: we use the class name as an error type here.

        except Exception, e:
            self._log.critical('*** UNEXPECTED PROBLEM! Egest failed!', job_request=egest_request, error=e)

            QaItem.set_error(item_id, 'UnexpectedExportProblem', str(e))

        self._log.exit(status=status)
        return status

    def do_jobs_done(self):
        self._log.enter()
        status = self.FAILED

        try:
            for adapter in self.adapters:
                adapter.flush(self.config.transfer_prep_dir)  # uses: xml_egest_adapter and a callisto_egest_adapter

            status = self.OK

        except Exception, e:
            self._log.critical('*** UNEXPECTED PROBLEM! Egest failed (while trying to create a final feed file!', error=e)
            raise   # stop the worker (nothing gets reported to the user!)

        self._log.exit(status=status)
        return status


if __name__ == '__main__':
    worker = EgestWorker(config)
    worker.run()
