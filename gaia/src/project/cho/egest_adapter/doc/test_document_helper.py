import os
from lxml import etree
from cStringIO import StringIO
from gaia.xml.cached_xml_dict import CachedXmlDict
from test_utils.test_helper import TestHelper
from mock import Mock
from project.cho.egest_adapter.entity_reference import EntityReference
from gaia.asset.asset import Asset
from project.cho.gaia_dom_adapter.cho import Cho
from gaia.xml.xml_dict import XmlDict
from qa.models import MCodes
from django.test import TestCase


class TestDocumentHelper(TestCase):
    ''' Provides utility functions that allow us to compare generated gift with expected gift - see JAMES comment '''
    maxDiff = None

    def setUp(self):
        #self.test_tmp_dir, self.log_fpath, self.log_fname, self.config = TestHelper.setUp(output_dir=os.path.join(os.path.dirname(__file__), ',tmp'))  # JAMES comment when in master
        self.test_tmp_dir, self.log_fpath, self.logger_fname, self.config = TestHelper.setUp()  # JAMES uncomment when in master

    def tearDown(self):
        #pass  # JAMES comment when in master
        TestHelper.tearDown(self.test_tmp_dir)  # JAMES uncomment when in master

    def _dump_to_file(self, fname, suffix, content):
        fpath = os.path.join(self.test_tmp_dir, '%s%s' % (fname, suffix))
        f = open(fpath, 'w')
        f.write(content.encode('utf-8'))
        f.close()

    def source_xml(self, source_test_data_fname):
        # represents the source xml that gets converted into gift - see: ~/GIT_REPOS/gaia/src/project/cho/test_samples
        return open(os.path.join(os.path.dirname(__file__), 'test_data/%s' % source_test_data_fname)).read()

    def _extra_args_binary_chunks(self, source_fname):
        # expand extra_args to include an 'illustrations' dictionary to see if we can bypass xml_dict 'empty element' with attributes returning 'None' behaviour
        asset = Asset(source_fname)
        dom_adapter = Cho(asset)
        return [chunk for chunk in dom_adapter.chunks() if chunk.is_binary]

    def _create_document_instances(self, source_fname, feed_type, extra_args, create_date='20121202'):
        # returns expected gift, that a document instance should match - see:  ~/GIT_REPOS/gaia/src/project/cho/egest_adapter/doc/test_data 

        source_fname = os.path.join(os.path.dirname(__file__), '../../test_samples/%s' % source_fname)
        source_xml = open(source_fname).read()
        source_xml_dict = CachedXmlDict(etree.parse(StringIO(source_xml)))

        # supply correct # of illustrations, we're interested in their attributes later
        extra_args['illustrations'] = self._extra_args_binary_chunks(source_fname)

        # patch out Original xml date attribute
        mocked_feed_type = feed_type(self.config, source_xml_dict, extra_args)
        mocked_feed_type.creation_date = Mock(return_value=create_date)

        return mocked_feed_type

    def _escape_create_document_instances(self, document_instances):
        actual_xml_pretty_printed = ''
        for document_instance in document_instances:
            actual_xml_pretty_printed += document_instance
        return EntityReference.unescape(actual_xml_pretty_printed)

    def _document(self, xml=None, extra_args=None):
        # make sure we can create a Document
        if xml is None:
            xml = '''<chapter>
        <metadataInfo>
            <PSMID>1234</PSMID>
        </metadataInfo>
        <page>p1</page>
    </chapter>'''
        tree =  etree.parse(StringIO(xml))
        return XmlDict(tree), extra_args

    def _create_mcode_for_psmid(self, mcode, psmid, publication_title):
        try:
            mcodes = MCodes.objects.get(psmid=psmid)
            mcodes.delete()
        except Exception, e:
            mcodes = MCodes(mcode=mcode, psmid=psmid, publication_title=publication_title)
            mcodes.save()
