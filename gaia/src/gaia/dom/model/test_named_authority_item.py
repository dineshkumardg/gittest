from logilab.common import date
from testing.gaia_django_test import GaiaDjangoTest
_test = GaiaDjangoTest()
_test.setUp()


import os
import unittest
import datetime
from mock import MagicMock
from shutil import copyfile
from gaia.asset.asset import Asset
from gaia.dom.model.test_item import AdapterFactory
from gaia.dom.model.named_authority_item import NamedAuthorityItem
from testing.gaia_test import GaiaTest


class TestNamedAuthorityItem(GaiaTest):
    def test_named_authority(self):
        expected_named_authority_info = [
            {'asset_id': 'KIENAK437152297', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Front Matter', 'article_id': 1, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'BJJEAU610688494', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Front Matter', 'article_id': 2, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'MATGHT085830543', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Front Matter', 'article_id': 3, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'EMTTUP120181217', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'United States', 'article_id': 4, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'LDJPJT514545430', 'gift_author': u'A. Elliot-Smith', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on U. S. A. Round Table Topic I, August 16, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 5},
            {'asset_id': 'FZPWCL660056375', 'gift_author': u'H. Belshaw', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on U. S. A. Round Tables, August 17, 1936, 8: 00 pm', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 6},
            {'asset_id': 'XLMNYS148824144', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Japan', 'article_id': 7, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'WYTSFL533685354', 'gift_author': u'Sir Kenneth Wigram', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on Japan round Table Topic II, August 18, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 8},
            {'asset_id': 'NTYFWL589979488', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Report of the General Rapporteur on round Table Topic II', 'article_id': 9, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'NXCDGK733115662', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'USSR', 'article_id': 10, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'YHNEWX237227065', 'gift_author': u'V. Motylov', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on U. S. S. R. - Round Table Topic III August 21, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 11},
            {'asset_id': 'NZYDDP552399354', 'gift_author': u'Mrs. Barbara Wootton', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on U. S. S. R. Round Table Topic III, August 22, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 12},
            {'asset_id': 'QCOOAV145199131', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'China', 'article_id': 13, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'GCSJMA272461276', 'gift_author': u'Lord Snell', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session on China Round Table Topic IV, August 24, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 14},
            {'asset_id': 'WARVPR507002176', 'ingest_date': '2003-08-04 12:30:45', 'gift_author': '', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'gift_article_title': u'Changing balance of Forces in the Pacific and the Possiblities of Peaceful Adjustment', 'article_id': 15, 'psmid': 'cho_iprx_1936_0016_000_0000a'},
            {'asset_id': 'PLJSSP317656808', 'gift_author': u'K. Yoshizawa', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement for Plenary Session of round Table Topic V August 26, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 16},
            {'asset_id': 'XQVNOO375760276', 'gift_author': u'Etionne Donnory', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'Statement at Plenary Session on round Table Topic V, August 29, 1936', 'psmid': 'cho_iprx_1936_0016_000_0000a', 'item_id': 'cho_iprx_1936_0016_000_0000a', 'article_id': 17}
            ]

        dom_id = 'cho_iprx_1936_0016_000_0000a'  # ~/GIT_REPOS/gaia/src/scripts/reports/mai/author_search/rose_reports/gift_htc_raw/conference_series_gift_raw.csv
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

        class Chunk:
            def __init__(self, dom_id, final_id):
                self.dom_id = dom_id
                self.final_id = final_id
            def get_final_id(self):  # maintain interface on final_id
                return self.final_id

        chunks = [  # text and binary
                  Chunk(u'1', 'KIENAK437152297'),
                  Chunk(u'2', 'YHNEWX237227065'),
                  Chunk(u'3', 'NZYDDP552399354'),
                  Chunk(u'4', 'QCOOAV145199131'),
                  Chunk(u'5', 'GCSJMA272461276'),
                  Chunk(u'6', 'WARVPR507002176'),
                  Chunk(u'7', 'PLJSSP317656808'),
                  Chunk(u'8', 'XQVNOO375760276'),
                  Chunk(u'9', 'YECLFH842756648'),
                  Chunk(u'10', 'BJJEAU610688494'),
                  Chunk(u'11', 'MATGHT085830543'),
                  Chunk(u'12', 'EMTTUP120181217'),
                  Chunk(u'13', 'LDJPJT514545430'),
                  Chunk(u'14', 'FZPWCL660056375'),
                  Chunk(u'15', 'XLMNYS148824144'),
                  Chunk(u'16', 'WYTSFL533685354'),
                  Chunk(u'17', 'NTYFWL589979488'),
                  Chunk(u'18', 'NXCDGK733115662'),
                  ]
        date = datetime.datetime(2003, 8, 4, 12, 30, 45)
        is_live = True

        named_authority_item = NamedAuthorityItem(dom_id, dom_id, assets, config, chunks=chunks, date=date, is_live=is_live)
        actual_named_authority_info = named_authority_item.named_authority_details()

        for i in range(0, len(expected_named_authority_info) -1):
            self.assertDictEqual(expected_named_authority_info[i], actual_named_authority_info[i])

    def test_named_authority_cho_meet_1949_1655_000_0000(self):
        expected_named_authority_info = [
            {'asset_id': 'ABCD', 'gift_author': u'Mr. Donald H. McLachlan O. B. E.', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'America and Power Politics', 'psmid': 'cho_meet_1949_1655_000_0000', 'item_id': 'cho_meet_1949_1655_000_0000', 'article_id': 1}
        ]

        dom_id = 'cho_meet_1949_1655_000_0000'
        xml_fname = '%s.xml' % dom_id

        copyfile(os.path.join(os.path.dirname(__file__), '../../../project/cho/test_samples/%s' % xml_fname), os.path.join(self.test_dir, xml_fname))

        xml_asset = Asset(os.path.join(self.test_dir, xml_fname), 'r')
        assets = []
        assets.append(xml_asset)

        schema_fpath = os.path.join('/', 'schema', 'fpath.xsd')
        config = MagicMock()
        config.dom_adapter_factory = AdapterFactory
        config.schema_fpath = schema_fpath

        class Chunk:
            def __init__(self, dom_id, final_id):
                self.dom_id = dom_id
                self.final_id = final_id
            def get_final_id(self):
                return self.final_id

        chunks = [  # text and binary
                  Chunk(u'1', 'ABCD'),
                  ]
        date = datetime.datetime(2003, 8, 4, 12, 30, 45)
        is_live = True

        named_authority_item = NamedAuthorityItem(dom_id, dom_id, assets, config, chunks=chunks, date=date, is_live=is_live)
        actual_named_authority_info = named_authority_item.named_authority_details()

        self.assertDictEqual(expected_named_authority_info[0], actual_named_authority_info[0])

    def test_named_authority_cho_meet_1960_2715_000_0000(self):
        expected_named_authority_info = [
            {'asset_id': 'ABCD', 'gift_author': u'Professor Max Beloff', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'The Monckton Commission Report', 'psmid': 'cho_meet_1960_2715_000_0000', 'item_id': 'cho_meet_1960_2715_000_0000', 'article_id': 1},
            {'asset_id': 'ABCD', 'gift_author': u'Professor S. Herbert Frankel', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'The Monckton Commission Report', 'psmid': 'cho_meet_1960_2715_000_0000', 'item_id': 'cho_meet_1960_2715_000_0000', 'article_id': 1},
            {'asset_id': 'ABCD', 'gift_author': u'Philip Mason C. I. E., O. B. E', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'The Monckton Commission Report', 'psmid': 'cho_meet_1960_2715_000_0000', 'item_id': 'cho_meet_1960_2715_000_0000', 'article_id': 1},
            {'asset_id': 'ABCD', 'gift_author': u'Sir Ronald Prain O. B. E', 'ingest_date': '2003-08-04 12:30:45', 'gift_article_title': u'The Monckton Commission Report', 'psmid': 'cho_meet_1960_2715_000_0000', 'item_id': 'cho_meet_1960_2715_000_0000', 'article_id': 1}
        ]

        dom_id = 'cho_meet_1960_2715_000_0000'
        xml_fname = '%s.xml' % dom_id

        copyfile(os.path.join(os.path.dirname(__file__), '../../../project/cho/test_samples/%s' % xml_fname), os.path.join(self.test_dir, xml_fname))

        xml_asset = Asset(os.path.join(self.test_dir, xml_fname), 'r')
        assets = []
        assets.append(xml_asset)

        schema_fpath = os.path.join('/', 'schema', 'fpath.xsd')
        config = MagicMock()
        config.dom_adapter_factory = AdapterFactory
        config.schema_fpath = schema_fpath

        class Chunk:
            def __init__(self, dom_id, final_id):
                self.dom_id = dom_id
                self.final_id = final_id
            def get_final_id(self):
                return self.final_id

        chunks = [
                  Chunk(u'1', 'ABCD'),
                  ]
        date = datetime.datetime(2003, 8, 4, 12, 30, 45)
        is_live = True

        named_authority_item = NamedAuthorityItem(dom_id, dom_id, assets, config, chunks=chunks, date=date, is_live=is_live)
        actual_named_authority_info = named_authority_item.named_authority_details()

        self.assertDictEqual(expected_named_authority_info[0], actual_named_authority_info[0])

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestNamedAuthorityItem),
    ])

_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
