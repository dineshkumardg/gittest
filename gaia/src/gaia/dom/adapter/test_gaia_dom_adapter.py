import unittest
from StringIO import StringIO
from mock import create_autospec, MagicMock, call
from gaia.asset.asset import Asset
from gaia.error import GaiaError
from gaia.dom.document_error import DocumentError
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from lxml import etree
from gaia.dom.model.document import Document


class TestXml:
    xml = '''<?xml version="1.0"?>
<catalog doctype="booklisting">
   <book id="bk101">
      <author>Gambardella, Matthew</author>
      <title>XML Developer's Guide</title>
      <genre>Computer</genre>
      <price>44.95</price>
      <publish_date>2000-10-01</publish_date>
      <description>An in-depth look at creating applications with XML.</description>
      <interest_level>Rubbish</interest_level>
   </book>
   <book id="bk102">
      <author>Corets, Eva</author>
      <title>Maeve Ascendant</title>
      <genre>Political</genre>
      <price>5.95</price>
      <publish_date>2000-11-17</publish_date>
      <description>After the collapse of society in England, the young survivors lay the foundation for a new society.</description>
      <interest_level>Moderate</interest_level>
   </book>
   <book id="bk103">
      <author>Ralls, Kim</author>
      <title>Ninja Dudes</title>
      <genre>Factual</genre>
      <price>5.95</price>
      <publish_date>2000-12-16</publish_date>
      <description>A former architect-turned-ninja battles 1001 other ninjas to become king ninja.</description>
      <interest_level>Awesome</interest_level>
   </book>
</catalog>
'''
    @classmethod
    def tree(self):
        return etree.parse(StringIO(TestXml.xml))

class SampleGaiaDomAdapter(GaiaDomAdapter):
    
    def __init__(self, xml_asset=TestXml.xml, match_doc_id=True):
    
        ''' Overriding init to bypass etree stuff/logger etc
            Note: Therefore need to provide initialised variables in tests
                  e.g. self._etree (hint: a Mock :) )
        '''
        self._data = {}

        self.xml_asset = create_autospec(Asset, spec_set=True, instance=True)
        self.xml_asset.fbase = 'fpath'# '/tmp/test/fpath.xml'

        if match_doc_id:
            dom_id = self.xml_asset.fbase
        else:
            dom_id = 'a dom id not matching the file name'
        dom_name = 'DOM_NAME'
        info = {'some': 'info'}
        self._expected_document= Document(dom_id, dom_name, info)
    
        self._document_called = False

    def _asset_fnames(self):
        pass
    
    def _get_chunks(self):
        pass
    
    def _get_clips(self):
        pass
    
    def _get_document(self):
        if self._document_called:
            raise Exception('THIS SHOULD NOT BE CALLED MORE THAN ONCE')
        else:
            self._document_called = True
            return self._expected_document
    
    def _get_links(self):
        pass
    
    def _get_pages(self):
        pass
    
class TestGaiaDomAdapter(unittest.TestCase):

    def test_document(self):
        adapter = SampleGaiaDomAdapter()
        self.assertEqual(adapter._expected_document, adapter.document())

        # check repeated access returns the same, cached, document...
        self.assertEqual(adapter._expected_document, adapter.document())
        self.assertEqual(adapter._expected_document, adapter.document())
        self.assertEqual(adapter._expected_document, adapter.document())


    def test_document_MISMATCH_DOC_ID(self):
        adapter = SampleGaiaDomAdapter(match_doc_id=False)
        self.assertRaises(DocumentError, adapter.document)

    def test_document_CACHED__get_document_RAISES(self):
        xml_fpath = '/tmp/test/fpath.xml' 
        xml_asset = create_autospec(Asset, spec_set=True, instance=True)
        xml_asset.fpath = xml_fpath
        adapter = SampleGaiaDomAdapter()
        adapter._get_document = MagicMock()
        adapter._get_document.side_effect = GaiaError('Oops')
        adapter.xml_asset = xml_asset
        
        self.assertRaises(DocumentError, adapter.document)
        
    def test_pages_CACHED(self):
        self._test_dom_func('pages', cached=True)

    def test_pages_NOT_CACHED(self):
        self._test_dom_func('pages', cached=False)

    def test_chunks_CACHED(self):
        self._test_dom_func('chunks', cached=True)

    def test_chunks_NOT_CACHED(self):
        self._test_dom_func('chunks', cached=False)

    def test_clips_CACHED(self):
        self._test_dom_func('clips', cached=True)

    def test_clips_NOT_CACHED(self):
        self._test_dom_func('clips', cached=False)

    def test_links_CACHED(self):
        self._test_dom_func('links', cached=True)

    def test_links_NOT_CACHED(self):
        self._test_dom_func('links', cached=False)

    def test_asset_fnames_CACHED(self):
        self._test_dom_func('asset_fnames', cached=True)

    def test_asset_fnames_NOT_CACHED(self):
        self._test_dom_func('asset_fnames', cached=False)
        
    def _test_dom_func(self, func_to_test_name, cached):
        adapter = SampleGaiaDomAdapter()
        
        data_val = 'the data'
        
        if cached:
            adapter._data['document'] = data_val
            adapter._data['pages'] = data_val
            adapter._data['chunks'] = data_val
            adapter._data['clips'] = data_val
            adapter._data['links'] = data_val
            adapter._data['asset_fnames'] = data_val
        else:
            adapter._get_document = MagicMock()
            adapter._get_pages = MagicMock()
            adapter._get_chunks = MagicMock()
            adapter._get_clips = MagicMock()
            adapter._get_links = MagicMock()
            adapter._asset_fnames = MagicMock()

            adapter._get_document.return_value = data_val
            adapter._get_pages.return_value = data_val
            adapter._get_chunks.return_value = data_val
            adapter._get_clips.return_value = data_val
            adapter._get_links.return_value = data_val
            adapter._asset_fnames.return_value = data_val
        
        self.assertEqual(data_val, getattr(adapter, func_to_test_name)())

    def test_write_NO_FPATH_ARG(self):
        xml_fpath = '/tmp/test/fpath.xml'
        xml_asset = create_autospec(Asset, spec_set=True, instance=True)
        xml_asset.fpath = xml_fpath
        
        adapter = SampleGaiaDomAdapter()
        adapter._etree = MagicMock()
        adapter.xml_asset = xml_asset
        
        expected__etree_calls = [call.write(xml_fpath, xml_declaration=True, encoding='utf-8')]
        
        adapter.write()
        
        self.assertListEqual(expected__etree_calls, adapter._etree.method_calls)

    def test_write_WITH_FPATH_ARG(self):
        xml_fpath = '/tmp/test/fpath.xml'
        
        adapter = SampleGaiaDomAdapter()
        adapter._etree = MagicMock()
        
        expected__etree_calls = [call.write(xml_fpath, xml_declaration=True, encoding='utf-8')]
        
        adapter.write(xml_fpath)
        
        self.assertListEqual(expected__etree_calls, adapter._etree.method_calls)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaDomAdapter),
    ])

if __name__ == "__main__":
    unittest.main()
