import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()

from django.test import TestCase
from qa.models import Item
from qa.manage.unrelease_view import UnreleaseView
from mock import MagicMock


class UnReleaseViewTestCase(TestCase):
    def test__get_m2_cho_meet(self):
        # set up test db (sqllite in ram)
        item = Item(dom_id='cho_bcrc_1933_0001_000_0000', dom_name='cho_bcrc_1933_0001_000_0000')
        item.save()
        item = Item(dom_id='cho_meet_2010_7771_001_0001', dom_name='cho_meet_2010_7771_001_0001')
        item.save()

        unrelease_view = UnreleaseView()
        self.assertEqual(1141, len(unrelease_view._get_m2_cho_meet_psmids()))

        unrelease_view._get_m2_cho_meet_psmids = MagicMock(return_value=['cho_meet_2010_7771_001_0001', 'does_not_exist'])

        items_to_release = [Item.objects.get(dom_id='cho_meet_2010_7771_001_0001')]

        unrelease_view._release(items_to_release, 'unrelease_only_meet_m2')
        self.assertEqual('un-released: 1 item(s): cho_meet_2010_7771_001_0001; cho_meet_2010_7771_001_0001', unrelease_view.msg)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(UnReleaseViewTestCase),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
