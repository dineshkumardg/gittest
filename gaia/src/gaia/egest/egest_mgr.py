import sys
from django.conf import settings
from gaia.config.config import get_config
from gaia.config.config_errors import GaiaConfigurationError

def usage():
        print
        print 'Usage: python egest_mgr.py MY_CONFIG'
        print 'eg:'
        print '       python egest_mgr.py JAMES_LINUX'
        print

try:
    config = get_config(sys.argv[1])
    config.check()

    # TODO: the old config check is no longer any good.
    # We need something like adapter.check_config(config)
    # which will do whatever it wants to check its params.
    #
    # . something liek this?...
    # for adapter_name, params in config.egest_adapters:
    #   import_class(adapter_name).check_params(params)

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

from gaia.task.mgr import Mgr
from qa.models import Item
from gaia.egest.egest_request import EgestRequest
from gaia.egest.jobs_done_request import JobsDoneRequest

class EgestMgr(Mgr):
    '''
    Monitor an Item's status (in django); when appropriate notify worker to process assets in an item_name (that's in the outbox). 
    
    Egest worker(s) need to be started before this mgr.
    ''' 
    process_name = 'egest_mgr'  # @override
    create_feed = False

    def __init__(self, config):
        Mgr.__init__(self, config.egest_job_sockets, config)

        # override base (ingest) settings with egest settings:
        # (should be parameterised like job_sockets: TODO)
        self.config.max_requests_outstanding = config.egest_max_requests_outstanding
        self.config.response_threshold = config.egest_response_threshold
        self.config.poll_interval = config.egest_poll_interval     

    def jobs(self): 
        self._log.enter()
        
        jobs = []

        # wait for the previous batch finished, and feed file created, then, release next batch 
        if self.create_feed == True and self._jobs_done_handled == False:
            #self.create_feed = False    
            return jobs

        # release_type == xml | callisto | both
        item_ids, item_names, release_type, self.create_feed = Item.release_next(limit=self.config.max_requests_outstanding)  # limit == nuumber of items sent to workers 
        for item_id, item_name, release_type in zip(item_ids, item_names, release_type):
            self._log.info('GOT JOB:', item_id=item_id, item_name=item_name)
            msg = EgestRequest(item_id, item_name, release_type)
            jobs.append(msg)

        self._log.exit()
        return jobs 
                
    def handle_jobs_done(self):
        ''' Each time a "batch" of jobs is released, we will "flush" any remaining
            document instqances into feed files
        '''
        self._log.info('Adding a JOBS DONE request (to flush doc instances into feed files).')
        return [JobsDoneRequest(),]

if __name__ == '__main__':
    mgr = EgestMgr(config)        
    mgr.run()
