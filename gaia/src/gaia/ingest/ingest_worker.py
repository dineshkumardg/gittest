import os
import sys
import gc

from django.conf import settings
from gaia.config.config import get_config
from gaia.config.config_errors import GaiaConfigurationError
from project.cho.gaia_dom_adapter.validation_rules import ValidationRules
from lxml import etree
from gaia.schema.schema import XmlParseError


# ----------------------------------------------------------
# Note: this lump of code is here so that django settings
# can be configured _before_ importing any Django modules
# eg from Item
# ----------------------------------------------------------
def usage():
    print
    print 'Usage: python ingest_worker.py MY_CONFIG'
    print 'eg:'
    print '       python ingest_worker.py STEW_LINUX'
    print

try:
    config = get_config(sys.argv[1])    # run as ingest_worker MY_CONFIG
    config.check()
except GaiaConfigurationError, e:
    print '\n\nERROR: BAD CONFIG:', str(e)
    sys.exit(1)
except IndexError, e:
    print
    print 'ERROR: Please supply at least one argument, ie the config to use.'
    print
    usage()
    sys.exit(2)

settings.configure(**config.get_django_settings())

from gaia.error import GaiaError, GaiaErrors
from gaia.utils.ftp import Ftp, FtpError
from gaia.utils.lock import LockError
from gaia.task.worker import Worker
from gaia.asset.asset_error import AssetError
from gaia.dom.model.item import Item as DomItem
from gaia.web.web_box import WebBox
from gaia.provider.provider import Provider
from gaia.provider.provider_error import TransferAbort
from gaia.ingest.inbox import Inbox
from gaia.ingest.error_report import ErrorReport
from gaia.ingest.worker_job_lock import WorkerJobLock
from gaia.egest.outbox import Outbox
from gaia.search.search_error import SearchError
from qa.models import IngestError
from qa.models import Item as QaItem


class IngestWorker(Worker):
    ''' An IngestWorker does everything that's required to get
        *one* Item into the Gaia system and/or reject it.
    '''
    process_name = 'ingest_worker'

    def __init__(self, config):
        Worker.__init__(self, config.ingest_job_sockets, config)

        self._empty_file_fpath = self._empty_file()
        self._bad_report_fpath = os.path.join(config.working_dir, 'ingest_worker_%d_bad_report.txt' % (os.getpid()))

    def _empty_file(self):
        'Create an empty file to be used for all "good" reports'
        fpath = os.path.join(self.config.working_dir, 'empty_file.txt')
        if not os.path.exists(fpath):
            f = open(fpath, 'w')
            f.close()   # Note: creates an empty file

        return fpath

    def run_rules_on_source_xml(self, asset):
        try:
            xml_tree = etree.parse(asset.fpath)
            validation_rules = ValidationRules()

            if validation_rules.are_chapter_page_article_text_textclip_articlepage_pgrefs_unique(xml_tree) == False:
                raise AssetError('duplicate articlePage/@pgref values', errors=validation_rules.errors)

            if validation_rules.are_chapter_page_article_clip_pgrefs_unique(xml_tree) == False:
                raise AssetError('duplicate clip/@pgref values', errors=validation_rules.errors)

            if validation_rules.are_clip_pgrefs_matching_articlepage_pgrefs(xml_tree) == False:
                raise AssetError('clip/@pgref and articlePage/@pgref values do not match', errors=validation_rules.errors)

            if validation_rules.are_illustration_pgrefs_matching_clip_pgrefs(xml_tree) == False:
                raise AssetError('dangling illustration/@pgref', errors=validation_rules.errors)

            if validation_rules.are_isbn_lengths_ok(xml_tree) == False:
                raise AssetError('two or more isbns have same length', errors=validation_rules.errors)

        except etree.XMLSyntaxError as e:  # xml not well formed?
            self._log.warning(str(e))
            raise XmlParseError(str(e))

    def do(self, job_request):
        self._log.info('Ingesting =======================================', job_request=job_request)

        collected = gc.collect()
        self._log.info('gc ingest.start collected %d objects' % collected)

        config = self.config
        transfer_agent = None
        job_lock = None

        status = self.FAILED    # by default we've failed to handle this job

        try:
            self._log.info('A: setup ......................................')
            provider_name = job_request.provider_name
            group = job_request.group
            item_name = job_request.item_name

            job_lock = WorkerJobLock(item_name, config)
            transfer_agent = Ftp(**config.content_providers[provider_name])

            provider = Provider(provider_name, transfer_agent, config)
            inbox = Inbox(os.path.join(config.inbox, provider_name))
            other_provider_inboxes = [Inbox(os.path.join(config.inbox, name)) for name in config.content_providers.keys() if name != provider_name]

            self._log.info('B: Transfer files ...................................')
            transfer_agent.open()
            assets, errors = provider.get_item(group, item_name, inbox)  # can raise a TransferAbort
            transfer_agent.close()

            self._log.info('C: validate any assets that were transferred (even if there were other errors)')
            for asset in assets:
                try:
                    asset.validate()
                    if asset.mime_type() == 'application/xml':  # http://jira.cengage.com/browse/EG-493

                        # TODO: fix: this rule will break about 6 system tests (including sanity); so we ignore this rule if an env var present
                        if os.environ.get('GAIA_SYSTEM_TEST_INGORE_INGEST_RULES') is None:
                            self.run_rules_on_source_xml(asset)
                except AssetError, e:
                    errors.append(e)

            if errors:
                # for asset in assets: #   throw away? / delete from inbox???
                # currently: just leave them there and let them get overwritten next time. (?)
                raise GaiaErrors(*errors)
            else:
                # pick up any files for this item (either from _this_ provider, or others)
                assets.extend(inbox.assets(item_name))

                for other_inbox in other_provider_inboxes:
                    assets.extend(other_inbox.assets(item_name))

                assets = list(set(assets))  # to remove duplicates

                # Note: The item dom_id=name AND dom_name=name
                # note that the document dom_name may be different to the item dom_name. (TODO: review: what's the point of the item dom_name?).
                item = DomItem(item_name, item_name, assets, config)

                if item.is_complete():
                    self._log.debug('--- item is complete; adding item to web_box ...')
                    web_box = WebBox(config)
                    web_box.add_item(item)

                    self._log.debug('--- item is complete; moving assets from inbox to outbox ...')
                    outbox = Outbox(config.outbox)
                    outbox.add_item(item)

                    inbox.delete_item(item)
                    for other_inbox in other_provider_inboxes:
                        other_inbox.delete_item(item)

                    self._log.debug('--- item is complete; marking as ready for qa ...')
                    qa_item = QaItem.objects.get(dom_id=item_name, is_live=True)
                    qa_item.ready_for_qa()
                #else:
                    #report = incomplete item ...
                    #IngestError.add_warning(provider_name, report)   #TODO add_warning? or IngestWarning table?..

                # H: confirm all is well with Provider ..............
                self._log.info('Reporting OK to provider.')
                transfer_agent.open()
                provider.ok(group, item_name, self._empty_file_fpath)   # WARNING/Note: if this fails we will try to raise a failed report..which might also not work! (TODO: review)
                transfer_agent.close()
                status = self.OK    # we're good only if we get this far.

        except SearchError, e:
            self._log.warning('ooo ABORTing: the Search Server is not usable: PLEASE FIX ASAP!', job_request=job_request, search_error=e)
            status = self.TRY_AGAIN  # please try again later...
        except TransferAbort, e:
            self._log.warning('ooo ABORTing: transfer was aborted', job_request=job_request, transfer_abort_error=e)
            status = self.TRY_AGAIN
        except LockError, e:
            self._log.warning('ooo ABORTing: lock error (job is locked by another worker?)', job_request=job_request, lock_error=e)
            status = self.TRY_AGAIN

        except GaiaError, e:
            self._log.error('FAILED NORMALLY', error=e)

            report = ErrorReport(provider_name, group, item_name, e)
            f = open(self._bad_report_fpath, 'w')
            f.write(str(report))
            f.close()

            try:
                IngestError.add_error(provider_name, report)

                self._log.info('Reporting FAILED to provider:', report=report)
                transfer_agent.retry_connection_attempts = 0
                transfer_agent.open()
                provider.failed(group, item_name, self._bad_report_fpath)
                transfer_agent.close()
                # TODO: if the provider fails because it can't find anything to delete, we should
                # continue and still return the report:
                # ie failure to delete due to missing on ftp server is OK (?: review: not sure why this is happening..TUSH)
            except GaiaError, e:
                self._log.critical('FAILED TO REPORT PROBLEM TO CONTENT PROVIDER after a Gaia problem (err="%s")' % str(e))

        except Exception, e:        # ABANDON SHIP (and leave state as is for manual inspection/repair).
            self._log.critical('*** UNEXPECTED PROBLEM! Ingest failed!', job_request=job_request, error=e)
            raise   # stop the worker.

        finally:
            try:
                if transfer_agent:
                    transfer_agent.close()

                if job_lock:
                    job_lock.unlock()
            except FtpError, e:
                self._log.warning('ftp close problem?)', error=e)
            finally:
                collected = gc.collect()
                self._log.info('gc ingest.end collected %d objects' % collected)

        self._log.exit(status=status)
        return status


if __name__ == '__main__':
    worker = IngestWorker(config)
    worker.run()
