import sys
from gaia.task.mgr import Mgr
from gaia.error import GaiaError 
from gaia.ingest.provider_ring import ProviderRing
from gaia.ingest.ingest_request import IngestRequest

class IngestMgr(Mgr):
    ''' gets incoming items
        and sends them as jobs to Validation Workers
        and collects results from workers.

        Workers (at least one) should be started before starting this manager.
    '''
    process_name = 'ingest_mgr' # @override

    def __init__(self, config):
        self._init(config)
        Mgr.__init__(self, config.ingest_job_sockets, config)

    def _init(self, config): # for testability
        self.config = config
        self._providers = ProviderRing(config)
        self._startup_jobs = None


    def jobs(self):
        ' get new jobs from Providers and return a list of IngestRequest jobs '
        self._log.enter()
        provider, transfer_agent = self._providers.next()
        jobs = []

        try:
            transfer_agent.open()
            new_items = provider.list_new_items() # Note: new_items = list of (group, item_name) tuples
            transfer_agent.close()
            
            for (group, item_dir) in new_items:
                self._log.info('GOT JOB:', provider=provider.name, group=group, item=item_dir)
                msg = IngestRequest(provider.name, group, item_dir)
                jobs.append(msg)

        except GaiaError, e: # TODO: .....
            self._log.error('An error occurred getting new items from a Provider FTP site', err=e)
            try:  # possible fix for 'err="[Errno 32] Broken pipe"'
                transfer_agent.close()
            except Exception, e:
                self._log.error('close raised an exception', err=e)

        self._log.exit()
        return jobs


def usage():
        print
        print 'Usage: python ingest_mgr.py MY_CONFIG'
        print 'eg:'
        print '       python ingest_mgr.py STEW_LINUX'
        print

def main():
    from django.conf import settings
    from gaia.config.config import get_config
    from gaia.config.config_errors import GaiaConfigurationError
    
    try:
        config = get_config(sys.argv[1])    # run as ingest_worker MY_CONFIG
        config.check()

        # IMPORTANT!
        # check_providers(config) # TODO? - verify that the providers are setup correctly and that we can connect to them before we start.

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

    mgr = IngestMgr(config)
    mgr.run()

if __name__ == '__main__':
    main()
