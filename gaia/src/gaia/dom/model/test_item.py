import os
import unittest
from mock import MagicMock, patch
from testing.gaia_test import GaiaTest
from gaia.asset.asset import Asset
from gaia.dom.adapter.gaia_dom_adapter import GaiaDomAdapter
from gaia.dom.model.dom_error import GaiaDomError
from gaia.dom.model.document import Document
from gaia.dom.model.item import ItemError, NoDocument, ItemIncompleteWarning, Item
from gaia.dom.model.link import AssetLink, DocumentLink
from gaia.dom.model.chunk import Chunk
from shutil import copyfile


class TestAdapter(GaiaDomAdapter):
    expected_asset_links = [AssetLink(dom_id='7', dom_name='link7', info={}, asset_fname='an_asset.jpg'),]
    expected_document_links = [DocumentLink(dom_id='8', dom_name='link8', info={}, source={'chunk': None, 'page': '1'}, target={'document':'a_document_name2', 'chunk': '2', 'page': '2'})]

    def _asset_fnames(self):
        return ['cho_iaxx_0000_0000_0000.xml',
                     'cho_iaxx_0000_0000_0000.jpg',
                     'cho_iaxx_0000_0000_0001.jpg',
                     'cho_iaxx_0000_0000_0002.jpg',
                     'cho_iaxx_0000_0000_0003.jpg',
                     'cho_iaxx_0000_0000_0000.mp3', ]

    def _get_chunks(self):
        pass

    def _get_clips(self):
        pass

    def _get_document(self):
        dom_name = 'cho_iaxx_0000_0000_0000'
        dom_id = dom_name
        info = {}
        return Document(dom_id, dom_name, info)

    def _get_links(self):
        all_links = []
        all_links.extend(self.expected_asset_links)
        all_links.extend(self.expected_document_links)
        return all_links

    def _get_pages(self):
        pass


class AdapterFactory:
    @classmethod
    def adapter_class(cls, xml_asset_fname):
        return TestAdapter


class LinkTestAdapter(TestAdapter):
    def __init__(self):
        self._data = {}

class LinkTestableItem(Item):
    ' this is just used to test links ' # WARNING: this is not a full testable object!
    def __init__(self):
        return # no need to run the initializer for the link tests

    def _get_dom_adapter(self):
        return LinkTestAdapter()


class TestItemErrors(unittest.TestCase):
    def test__init__ItemError(self):
        e = ItemError()
        self.assertIsInstance(e, GaiaDomError)

    def test__init__NoDocument(self):
        e = NoDocument()
        self.assertIsInstance(e, ItemError)

    def test__init__ItemIncompleteWarning(self):
        e = ItemIncompleteWarning()
        self.assertIsInstance(e, ItemError)


class TestItem(GaiaTest):
    def test_str(self):
        item = Item('dom_id', 'dom_name', MagicMock(), MagicMock())
        expected_str = 'Item (dom_id="dom_id", dom_name="dom_name")'
        self.assertEqual(expected_str, str(item))

    def test_documemt(self):
        item = Item('dom_id', 'dom_name', MagicMock(), MagicMock())
        item._get_dom_adapter = MagicMock()
        item.document()
        item._get_dom_adapter.return_value.document.assert_called_once_with()

    def test_pages(self):
        item = Item('dom_id', 'dom_name', MagicMock(), MagicMock())
        item._get_dom_adapter = MagicMock()
        item.pages()
        item._get_dom_adapter.return_value.pages.assert_called_once_with()

    def test_chunks(self):
        item = Item('dom_id', 'dom_name', MagicMock(), MagicMock())
        item._get_dom_adapter = MagicMock()
        item.chunks()
        item._get_dom_adapter.return_value.chunks.assert_called_once_with()

    def test_clips(self):
        item = Item('dom_id', 'dom_name', MagicMock(), MagicMock())
        item._get_dom_adapter = MagicMock()
        item.clips()
        item._get_dom_adapter.return_value.clips.assert_called_once_with()

    def test_asset_links(self):
        item = LinkTestableItem()
        links = item.asset_links()
        self.assertEqual(TestAdapter.expected_asset_links, links)

    def test_document_links(self):
        item = LinkTestableItem()
        links = item.document_links()
        self.assertEqual(TestAdapter.expected_document_links, links)

    @patch('gaia.dom.adapter.gaia_dom_adapter.etree.parse') # Patch etree in GaiaDomAdapter otherwise we'll have to write some XML :)
    @patch('gaia.dom.model.item.Xsd.validate')
    @patch('gaia.dom.model.item.Log.get_logger') # Patch logging otherwise we must call Log.configure_logging()
    def test_is_complete_OK(self, get_logger, validate, parse):
        assets = []
        actual_fnames = [ 'cho_iaxx_0000_0000_0000.xml',
                          'cho_iaxx_0000_0000_0000.jpg',
                          'cho_iaxx_0000_0000_0001.jpg',
                          'cho_iaxx_0000_0000_0002.jpg',
                          'cho_iaxx_0000_0000_0003.jpg',
                          'cho_iaxx_0000_0000_0000.mp3', ]

        xml_asset = Asset(os.path.join(self.test_dir, actual_fnames[0]), 'wb')
        assets.append(xml_asset)

        for fname in actual_fnames[1:]:
            asset = Asset(os.path.join(self.test_dir, fname), 'wb')
            assets.append(asset)
            asset.close()

        schema_fpath = os.path.join('/', 'schema', 'fpath.xsd')
        config = MagicMock()
        config.dom_adapter_factory = AdapterFactory
        config.schema_fpath = schema_fpath

        dom_id = 'cho_iaxx_0000_0000_0000'
        item = Item(dom_id, 'dom_name', assets, config)

        complete = item.is_complete()

        self.assertTrue(complete)
        validate.assert_called_once_with(xml_asset.fpath, schema_fpath)

    @patch('gaia.dom.adapter.gaia_dom_adapter.etree.parse') # Patch etree in GaiaDomAdapter otherwise we'll have to write some XML :)
    @patch('gaia.dom.model.item.Xsd.validate')
    @patch('gaia.dom.model.item.Log.get_logger') # Patch logging otherwise we must call Log.configure_logging()
    def test_is_complete_NO_XML_FILE(self, get_logger, validate, parse):
        assets = []
        actual_fnames = [ # No XML Document
                          'cho_iaxx_0000_0000_0000.jpg',
                          'cho_iaxx_0000_0000_0001.jpg',
                          'cho_iaxx_0000_0000_0002.jpg',
                          'cho_iaxx_0000_0000_0003.jpg',
                          'cho_iaxx_0000_0000_0000.mp3', ]

        for fname in actual_fnames:
            asset = Asset(os.path.join(self.test_dir, fname), 'wb')
            assets.append(asset)
            asset.close()

        config = MagicMock()

        item = Item('dom_id', 'dom_name', assets, config)

        self.assertFalse(item.is_complete())

    @patch('gaia.dom.adapter.gaia_dom_adapter.etree.parse') # Patch etree in GaiaDomAdapter otherwise we'll have to write some XML :)
    @patch('gaia.dom.model.item.Xsd.validate')
    @patch('gaia.dom.model.item.Log.get_logger') # Patch logging otherwise we must call Log.configure_logging()
    def test_is_complete_INCOMPLETE(self, get_logger, validate, parse):
        dom_id = 'cho_iaxx_0000_0000_0000'
        fnames = [ 'cho_iaxx_0000_0000_0000.xml',
                          'cho_iaxx_0000_0000_0000.jpg',
                          'cho_iaxx_0000_0000_0001.jpg',
                          #'cho_iaxx_0000_0000_0002.jpg',   # missing
                          'cho_iaxx_0000_0000_0003.jpg',
                          'cho_iaxx_0000_0000_0000.mp3', ]

        xml_asset = Asset(os.path.join(self.test_dir, fnames[0]), 'wb')
        assets = []
        assets.append(xml_asset)

        for fname in fnames[1:]:
            asset = Asset(os.path.join(self.test_dir, fname), 'wb')
            assets.append(asset)
            asset.close()

        schema_fpath = os.path.join('/', 'schema', 'fpath.xsd')
        config = MagicMock()
        config.dom_adapter_factory = AdapterFactory
        config.schema_fpath = schema_fpath

        item = Item(dom_id, 'dom_name', assets, config)

        complete = item.is_complete()

        self.assertFalse(complete)
        validate.assert_called_once_with(xml_asset.fpath, schema_fpath)

    def _get_item(self, dom_id, asset_fnames):
        assets = []
        for fname in asset_fnames:
            asset = Asset(os.path.join(self.test_dir, fname), 'wb')
            assets.append(asset)
            asset.close()

        config = MagicMock()
        return Item(dom_id, 'dom_name', assets, config)

    def test_xml_asset(self):
        expected_xml_asset_fname = 'cho_iaxx_0000_0000_0000.xml'

        dom_id = 'cho_iaxx_0000_0000_0000'
        asset_fnames = [ expected_xml_asset_fname, 'cho_iaxx_0000_0000_0000.jpg', ]
        item = self._get_item(dom_id, asset_fnames)

        actual_xml_fname = item.xml_asset().fname
        self.assertEquals(expected_xml_asset_fname, actual_xml_fname)

    def test_image_assets(self):
        asset_fnames = ['a.jpg', 'a.mp3', 'a.xml', 'b.jpg']
        dom_id = 'a'
        item = self._get_item(dom_id, asset_fnames)

        assets = item.image_assets()

        self.assertEquals(['a.jpg', 'b.jpg'], [asset.fname for asset in assets])

    def test_audio_video_assets(self):
        asset_fnames = ['a.jpg', 'a.mp3', 'a.xml', 'b.mp3']
        dom_id = 'a'
        item = self._get_item(dom_id, asset_fnames)

        assets = item.audio_video_assets()

        self.assertEquals(['a.mp3', 'b.mp3'], [asset.fname for asset in assets])

    def test_binary_assets(self):
        asset_fnames = ['a.jpg', 'a.mp3', 'a.xml', 'b.mp3']
        dom_id = 'a'
        item = self._get_item(dom_id, asset_fnames)

        assets = item.binary_assets()

        self.assertEquals(['a.jpg', 'a.mp3', 'b.mp3'], [asset.fname for asset in assets])

    def test_etoc_info(self):
        # see: test_parent_conference_series.py
        expected_etoc_info = [{'article_title': 'Front Matter', 'asset_id': u'KIENAK437152297', 'article_id': 1, 'article_type_text': 'front_matter', 'etoc_indentation': '', 'etoc_id': '1', 'article_id_real': '1'},
                              {'article_title': 'Front Matter', 'asset_id': u'BJJEAU610688494', 'article_id': 2, 'article_type_text': 'front_matter', 'etoc_indentation': '++++', 'etoc_id': '2', 'article_id_real': '2'},
                              {'article_title': 'Introduction', 'asset_id': u'MATGHT085830543', 'article_id': 3, 'article_type_text': 'article', 'etoc_indentation': '++++', 'etoc_id': '2', 'article_id_real': '3'},
                              {'article_title': 'Preface', 'asset_id': u'EMTTUP120181217', 'article_id': 4, 'article_type_text': 'front_matter', 'etoc_indentation': '++++++++', 'etoc_id': '3', 'article_id_real': '4'},
                              {'article_title': 'Table of Contents', 'asset_id': u'LDJPJT514545430', 'article_id': 5, 'article_type_text': 'front_matter', 'etoc_indentation': '++++++++', 'etoc_id': '3', 'article_id_real': '5'},
                              {'article_title': 'Societies and Organizations in Great Britain', 'asset_id': u'FZPWCL660056375', 'article_id': 6, 'article_type_text': 'part', 'etoc_indentation': '++++++++++++', 'etoc_id': '4', 'article_id_real': '6'},
                              {'article_title': 'I. Official', 'asset_id': u'XLMNYS148824144', 'article_id': 7, 'article_type_text': 'part', 'etoc_indentation': '++++++++++++++++', 'etoc_id': '5', 'article_id_real': '7'},
                              {'article_title': 'League of Nations Office', 'asset_id': u'WYTSFL533685354', 'article_id': 8, 'article_type_text': 'article', 'etoc_indentation': '++++', 'etoc_id': '2', 'article_id_real': '8'},
                              {'article_title': 'International Labour Office', 'asset_id': u'NTYFWL589979488', 'article_id': 9, 'article_type_text': 'article', 'etoc_indentation': '++++', 'etoc_id': '2', 'article_id_real': '9'},
                              {'article_title': '2. The Study of International Affairs in General', 'asset_id': u'NXCDGK733115662', 'article_id': 10, 'article_type_text': 'part', 'etoc_indentation': '++++++++', 'etoc_id': '3', 'article_id_real': '10'},
                              {'article_title': '(a) I. British Co-Ordinating Committee for International Studies', 'asset_id': u'YHNEWX237227065', 'article_id': 11, 'article_type_text': 'article', 'etoc_indentation': '++++++++++++', 'etoc_id': '4', 'article_id_real': '11'}]

        dom_id = 'cho_bcrc_1938_cleeve_001_0000'
        xml_fname = '%s.xml' % dom_id

        # make sure some xml exists in the test_dir
        copyfile(os.path.join(os.path.dirname(__file__), '../../../project/cho/test_samples/%s' % xml_fname), os.path.join(self.test_dir, xml_fname))

        xml_asset = Asset(os.path.join(self.test_dir, xml_fname), 'r')
        assets = []
        assets.append(xml_asset)

        schema_fpath = os.path.join('/', 'schema', 'fpath.xsd')
        config = MagicMock()
        config.dom_adapter_factory = AdapterFactory  # gives us  etree
        config.schema_fpath = schema_fpath

        # we need chunk information as well :-( as we use the gdom on a link in the ui
        item = Item(dom_id, dom_id, assets, config)
        chunks = []
        for i in range(1, 14):
            chunks.append(Chunk(dom_id = i, dom_name=str(i), info={}, page_ids=[str(i)]))
        item.chunks = MagicMock(return_value=chunks)

        ordered_asset_ids = [
            u'KIENAK437152297',
            u'BJJEAU610688494',
            u'MATGHT085830543',
            u'EMTTUP120181217',
            u'LDJPJT514545430',
            u'FZPWCL660056375',
            u'XLMNYS148824144',
            u'WYTSFL533685354',
            u'NTYFWL589979488',
            u'NXCDGK733115662',
            u'YHNEWX237227065'
            ]

        actual_etoc_info = item.etoc_info(ordered_asset_ids)

        self.assertListEqual(expected_etoc_info, actual_etoc_info)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestItem),
    unittest.TestLoader().loadTestsFromTestCase(TestItemErrors),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
