import unittest
from testing.gaia_test import GaiaTest
from gtp_site import GtpSite


class TestGtpSite(GaiaTest):

    def test__init__(self):
        expected_items_dir = '/proj/items'
        expected_reports_bad_dir = '/proj/reports/bad'
        expected_reports_good_dir = '/proj/reports/good'

        gs = GtpSite('proj')
        
        self.assertEqual(expected_items_dir, gs.items_dir)
        self.assertEqual(expected_reports_bad_dir, gs.reports_bad_dir)
        self.assertEqual(expected_reports_good_dir, gs.reports_good_dir)

    def test_item_dir(self):
        expected_item_dir = '/proj/items/group/item_name'
        
        gs = GtpSite('proj')
        
        actual_item_dir = gs.item_dir('group', 'item_name')

        self.assertEqual(expected_item_dir, actual_item_dir)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGtpSite),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
