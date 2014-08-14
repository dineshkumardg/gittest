from testing.test_suite_common import TestSuiteCommon


import gaia.test_error
import gaia.task.test_job_queue
import gaia.task.msg.test_msg
import gaia.task.msg.test_request
import gaia.task.msg.test_reply
import gaia.task.msg.test_job_request
import gaia.task.msg.test_job_reply
import gaia.callisto.test_callisto_zip
import gaia.config.test_config
import gaia.config.test_config_errors
import gaia.utils.test_archive
import gaia.utils.test_image_attributes
import gaia.utils.test_try_cmd
import gaia.utils.test_ftp
import gaia.utils.test_lock
import gaia.utils.test_gaia_file
import gaia.utils.test_gaia_folder
import gaia.utils.test_now
import gaia.utils.test_errors_mixin
import gaia.utils.test_sliding_window
import gaia.utils.test_import_class
import gaia.utils.test_work_area
import gaia.utils.test_safe_unicode
import gaia.asset.test_asset
import gaia.store.test_item_store
import gaia.store.test_lockable_item_store
import gaia.store.test_store_error
import gaia.ingest.test_ingest_errors
import gaia.ingest.test_worker_job_lock
import gaia.ingest.test_error_report
import gaia.ingest.test_inbox
import gaia.ingest.test_provider_ring
import gaia.gtp.test_manifest
import gaia.gtp.test_manifest_error
import gaia.gtp.test_gtp_site
import gaia.gtp.test_gtp_status
import gaia.report.test_report
import gaia.provider.test_provider
import gaia.web.test_web_box
import gaia.log.test_log
import gaia.schema.test_xsd
import gaia.schema.test_dtd
import gaia.dom.adapter.test_gaia_dom_adapter
import gaia.dom.test_document_error
import gaia.dom.model.test_dom_objects
import gaia.dom.model.test_dom_error
import gaia.dom.model.test_item
import gaia.dom.store.test_dom_file_store
import gaia.dom.store.test_dom_index
import gaia.dom.store.test_versioned_item_store
import gaia.dom.store.test_lockable_versioned_item_store
import gaia.dom.store.test_dom_store
import gaia.dom.index.test_models
import gaia.search.test_query
import gaia.search.adapter.test_chunk_search_adapter
import gaia.egest.test_egest_request
import gaia.egest.test_jobs_done_request
import gaia.egest.conversion.test_conversion_errors
import gaia.egest.adapter.test_callisto_egest_adapter
import gaia.egest.adapter.test_xml_conversion_dict
import gaia.xml.test_xml_dict
import gaia.xml.test_cached_xml_dict


class TestSuiteGaia(TestSuiteCommon):
    def __init__(self):
        TestSuiteCommon.__init__(self)
        #Log.configure_logging(',%s' % self.__class__.__name__, Config())

        self.standard_tests = [
            gaia.test_error.suite,
            gaia.task.test_job_queue.suite,
            gaia.task.msg.test_msg.suite,
            gaia.task.msg.test_request.suite,
            gaia.task.msg.test_reply.suite,
            gaia.task.msg.test_job_request.suite,
            gaia.task.msg.test_job_reply.suite,
            gaia.callisto.test_callisto_zip.suite,
            gaia.config.test_config.suite,
            gaia.config.test_config_errors.suite,
            gaia.utils.test_archive.suite,
            gaia.utils.test_image_attributes.suite,
            gaia.utils.test_try_cmd.suite,
            gaia.utils.test_ftp.suite,
            gaia.utils.test_lock.suite,
            gaia.utils.test_gaia_file.suite,
            gaia.utils.test_gaia_folder.suite,
            gaia.utils.test_now.suite,
            gaia.utils.test_errors_mixin.suite,
            gaia.utils.test_sliding_window.suite,
            gaia.utils.test_import_class.suite,
            gaia.utils.test_work_area.suite,
            gaia.utils.test_safe_unicode.suite,
            gaia.asset.test_asset.suite,
            gaia.store.test_item_store.suite,
            gaia.store.test_lockable_item_store.suite,
            gaia.store.test_store_error.suite,
            gaia.gtp.test_manifest.suite,
            gaia.gtp.test_manifest_error.suite,
            gaia.gtp.test_gtp_site.suite,
            gaia.gtp.test_gtp_status.suite,
            gaia.report.test_report.suite,
            gaia.provider.test_provider.suite,
            gaia.ingest.test_ingest_errors.suite,
            gaia.ingest.test_worker_job_lock.suite,
            gaia.ingest.test_error_report.suite,
            gaia.ingest.test_inbox.suite,
            gaia.ingest.test_provider_ring.suite,
            gaia.log.test_log.suite,
            gaia.schema.test_xsd.suite,
            gaia.schema.test_dtd.suite,
            gaia.dom.adapter.test_gaia_dom_adapter.suite,
            gaia.dom.test_document_error.suite,
            gaia.dom.store.test_dom_file_store.suite,
            gaia.dom.model.test_dom_objects.suite,
            gaia.dom.model.test_dom_error.suite,
            gaia.dom.model.test_item.suite,
            gaia.dom.store.test_versioned_item_store.suite,
            gaia.dom.store.test_lockable_versioned_item_store.suite,
            gaia.search.test_query.suite,
            gaia.search.adapter.test_chunk_search_adapter.suite,
            gaia.egest.test_egest_request.suite,
            gaia.egest.test_jobs_done_request.suite,
            gaia.egest.conversion.test_conversion_errors.suite,
            gaia.egest.adapter.test_callisto_egest_adapter.suite,
            gaia.egest.adapter.test_xml_conversion_dict.suite,
            gaia.xml.test_xml_dict.suite,
            gaia.xml.test_cached_xml_dict.suite,
            gaia.dom.store.test_dom_store.suite,
            gaia.dom.store.test_dom_index.suite,
            gaia.web.test_web_box.suite,
            gaia.dom.index.test_models.suite,
        ]
