from scripts.gda.gale_data_archive import GaleDataArchive
import os
import shutil
import tempfile
import unittest


class TestGaleDataArchive(unittest.TestCase):
    """
    ASSUMES:
    . sanity system test run
    . prod. database restored into system test db
    . web_root + outbox nfs'd (read only)
    . run_server.py running
    """
    def setUp(self):
        self._gda = GaleDataArchive()
        self._tmp_test_folder = tempfile.mkdtemp()
        self._outbox = '%s/WORK/cho/outbox' % os.environ.get('SYSTEM_TEST')

    def tearDown(self):
        shutil.rmtree(self._tmp_test_folder, ignore_errors=True)

    def _test_copy_all_item_versions_from_one_folder_to_another_folder(self, live_items, src, dest):
        self._gda.copy_all_item_versions_from_source_to_destination(live_items, src, dest)
        self.assertTrue(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/13626/cho_rpax_1986_goodman_000_0000.xml' % self._tmp_test_folder))
        self.assertTrue(os.path.exists('%s/cho_meet_1935_0389_000_0000/144/cho_meet_1935_0389_000_0000.xml' % self._tmp_test_folder))

    def _get_xml_file_size(self, root_folder, item_dom_name, item_id):
        xml_fname = '%s/%s/%s/%s.xml' % (root_folder, item_dom_name, item_id, item_dom_name)
        return os.stat(xml_fname).st_size

    def test_get_live_items_from_gaia_dv_with_bad_details(self):
        self._gda = GaleDataArchive(db_dns_host=None)
        self.assertRaises(GaleDataArchive.UnableToGetItemsFromGaia, self._gda.get_live_items_from_gaia_db)

    def test_get_live_items_from_gaia_db(self):
        live_items = self._gda.get_live_items_from_gaia_db()
        self.assertIsNotNone(live_items)

    def test_get_fixed_xml_for_item_from_gaia_ws_without_specifying_item(self):
        self.assertRaises(GaleDataArchive.UnableToGetFixedXMLFromGaia, self._gda.get_fixed_xml_from_gaia_ws)

    def test_get_fixed_items_from_gaia_db(self):
        fixed_items = self._gda.get_fixed_items_from_gaia_db()
        self.assertEqual({'3216': 'cho_rpax_1962_memoranda_002_0000'}, fixed_items[0])

    def test_get_released_items_from_gaia_db(self):
        released_items = self._gda.get_released_items_from_gaia_db()
        self.assertEqual({'13347': 'cho_wtxx_1986_0042_000_0000'}, released_items[0])

    def test_get_fixed_xml_for_item_from_gaia_ws(self):
        self._gda.login_to_gaia_website()
        fixed_xml = self._gda.get_fixed_xml_from_gaia_ws('12489')
        self.assertEqual('<chapter xmlns', fixed_xml[:14])

    def test_put_fixed_xml_into_archive_folder(self):
        self._test_copy_all_item_versions_from_one_folder_to_another_folder(
                             [{'13626': 'cho_rpax_1986_goodman_000_0000'}, {'4124': 'cho_meet_1935_0389_000_0000'}],
                             '/mnt/nfs/gaia/web_root',
                             self._tmp_test_folder)

        fixed_items = [{'13626': 'cho_rpax_1986_goodman_000_0000'}]
        item_id, item_dom_name = self._gda.get_dom_id_dom_name(fixed_items[0])

        self.assertEqual(1729769, self._get_xml_file_size(self._tmp_test_folder, item_dom_name, item_id))

        self._gda.login_to_gaia_website()
        fixed_xml = self._gda.get_fixed_xml_from_gaia_ws(item_id)

        self._gda.save_fixed_xml_into_folder(self._tmp_test_folder, item_dom_name, item_id, fixed_xml)
        self.assertEqual(1692326, self._get_xml_file_size(self._tmp_test_folder, item_dom_name, item_id))

    def test_purge_gdom_from_folder(self):
        self._gda.copy_all_item_versions_from_source_to_destination([{'12489': 'cho_rpax_1986_goodman_000_0000'}],
                                                                           '/mnt/nfs/gaia/web_root',
                                                                           self._tmp_test_folder)

        latest_items = [{'12489': 'cho_rpax_1986_goodman_000_0000'}]
        live_item_id, item_dom_name = self._gda.get_dom_id_dom_name(latest_items[0])

        self._gda._rm_gdom_from_a_folder(self._tmp_test_folder, item_dom_name, live_item_id)
        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/12489/manifest.md5' % self._tmp_test_folder))
        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/12489/chunk' % self._tmp_test_folder))
        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/12489/document' % self._tmp_test_folder))
        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/12489/page' % self._tmp_test_folder))
        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000/12452' % self._tmp_test_folder))

    def test_purge_unreleased_items_from_folder(self):
        live_items = [{'13626': 'cho_rpax_1986_goodman_000_0000'}, {'4124': 'cho_meet_1935_0389_000_0000'}]
        self._gda.copy_all_item_versions_from_source_to_destination(
                             live_items,
                             '/mnt/nfs/gaia/web_root',
                             self._tmp_test_folder)

        released_items = [{'4124': 'cho_meet_1935_0389_000_0000'}]
        self._gda.purge_unreleased_items_from_folder(released_items, self._tmp_test_folder)

        self.assertFalse(os.path.exists('%s/cho_rpax_1986_goodman_000_0000' % self._tmp_test_folder))
        self.assertTrue(os.path.exists('%s/cho_meet_1935_0389_000_0000/4124' % self._tmp_test_folder))

    def _test_sit(self):
        gda = GaleDataArchive()

        gda_folder = self._tmp_test_folder

        live_items = [{'13350': 'cho_book_1972_dexter_000_0000'}, {'3474': 'cho_bcrc_1937_cleeve_001_0000'}]
        gda.copy_all_item_versions_from_source_to_destination(live_items, '/mnt/nfs/gaia/web_root', gda_folder)

        gda.logger.info('=' * 30)
        gda.rm_gdom(live_items, gda_folder)

        gda.logger.info('=' * 30)
        fixed_items = [{'13350': 'cho_book_1972_dexter_000_0000'}]
        self.assertEqual(30757459, self._get_xml_file_size(gda_folder, 'cho_book_1972_dexter_000_0000', '13350'))
        gda.write_fixed_xml(fixed_items, gda_folder)
        self.assertEqual(30090528, self._get_xml_file_size(gda_folder, 'cho_book_1972_dexter_000_0000', '13350'))

        gda.logger.info('=' * 30)
        released_items = [{'3474': 'cho_bcrc_1937_cleeve_001_0000'}]
        gda.purge_unreleased_items_from_folder(released_items, gda_folder)
        self.assertTrue(os.path.exists('%s/cho_bcrc_1937_cleeve_001_0000/3474' % gda_folder))
        self.assertFalse(os.path.exists('%s/cho_book_1972_dexter_000_0000' % gda_folder))

    def _test_sit_place_item_str_list_into_folder(self):
        # things that been moved back into qa due to missing callisto images + other 'unknown' reasons for moving thigns back into qa!
        #item_str_list = "'cho_bcrc_1933_0001_000_0000', 'cho_book_1934_0003_000_0000'"
        item_str_list = "'cho_bcrc_1933_0001_000_0000', 'cho_book_1934_0003_000_0000', 'cho_book_1939_Kuczynski_000_0000', 'cho_book_1942_0002_002_0000', 'cho_book_1948_0000_001_0000', 'cho_book_1955_popper_000_0000', 'cho_book_1956_0002_002_0000', 'cho_book_1957_pendle_000_0000', 'cho_book_1958_bullard_000_0000', 'cho_book_1958_thomson_000_0000', 'cho_book_1964_ionescu_000_0000', 'cho_book_1965_purcell_000_0000', 'cho_book_1967_McLachlan_000_0000', 'cho_book_1974_MacFarquhar_000_0000', 'cho_book_1974_morgan_000_0000', 'cho_book_1976_0002_000_0000', 'cho_book_1976_russell_000_0000', 'cho_rfpx_1939B_0000_013_0000', 'cho_rfpx_1939C_0000_010_0000', 'cho_rfpx_1940A_0000_017_0000', 'cho_rfpx_1940A_0000_021_0000', 'cho_rfpx_1940C_0000_015_0000', 'cho_rfpx_1940C_0000_049_0000', 'cho_rfpx_1943A_0000_170_0000', 'cho_binx_1927-1928_0004_000_0000', 'cho_binx_1935-1936_0012_000_0000', 'cho_binx_1938_0015_001_0000', 'cho_binx_1938_0015_002_0000', 'cho_binx_1939_0016_001_0000', 'cho_binx_1939_0016_002_0000', 'cho_iaxx_1940-1943_0019_000_0000', 'cho_iaxx_1949_0025_000_0000', 'cho_iaxx_1955_0031_000_0000', 'cho_iaxx_1966_0042_000_0000', 'cho_byil_1922_0003_000_0000', 'cho_byil_1931_0012_000_0000', 'cho_byil_1954_0031_000_0000', 'cho_byil_1967_0042_000_0000', 'cho_diax_1962_0000_000_0000'"

        gda_folder = '/mnt/Archive/Chatham_House/gda/m1.supp'  # self._tmp_test_folder

        gda = GaleDataArchive()
        items_missing_from_gda = gda.get_live_items_from_gaia_db(item_str_list)

        gda.copy_all_item_versions_from_source_to_destination(items_missing_from_gda, '/mnt/nfs/gaia/web_root', gda_folder)
        gda.rm_gdom(items_missing_from_gda, gda_folder)
        gda.write_fixed_xml(items_missing_from_gda,
                            gda_folder,
                            django_login_url='http://10.179.176.181:8004/accounts/login/?next=/qa/',
                            ws_url='http://10.179.176.181:8004/qa/ws/v1.0/item/%s'
                            )
        gda.purge_unreleased_items_from_folder(items_missing_from_gda, gda_folder)

    def _test_get_all_items_as_fixed(self):
        # ls | egrep '^cho_[a-z]{4}_(198|199|20).*$'| xargs -I{} mv {} m2
        gda = GaleDataArchive()
        gda_folder = '/home/jsears/Desktop/prod.xml/all_fixed'
        live_items = gda.get_live_items_from_gaia_db()

        gda.login_to_gaia_website('http://10.179.176.181:8004/accounts/login/?next=/qa/')  # get CSCR

        item_count = 0
        for item in live_items:
            item_id, item_dom_name = gda.get_dom_id_dom_name(item)

            item_count += 1
            print '%s/%s: %s' % (item_count, len(live_items), item_dom_name)

            fixed_xml = gda.get_fixed_xml_from_gaia_ws(item_id, 'http://10.179.176.181:8004/qa/ws/v1.0/item/%s')
            try:
                with open('%s/%s.xml' % (gda_folder, item_dom_name), 'w') as f:
                    f.write(fixed_xml)
            except IOError as e:
                self.logger.warn(str(e))


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaleDataArchive),
    ])
