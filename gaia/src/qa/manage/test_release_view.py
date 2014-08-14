import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()

from django.test import TestCase
from django.test.client import Client
from qa.models import Item, Document
from django.contrib.auth.models import Group, User, Permission, ContentType
from qa.manage.release_view import ReleaseView
from mock import MagicMock


class ReleaseViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        
        # set test data
        item1 = Item(dom_name='item1', dom_id='item1')
        item1.save()
        document1 = Document(dom_id='doc1', item=item1)
        document1.save()
        item2 = Item(dom_name=u'f\u12341 item2', dom_id='item2')
        item2.save()
        document2 = Document(dom_id='doc2', item=item2)
        document2.save()
        item3 = Item(dom_name=u'f\u12341 item3', dom_id='item3')
        item3.save()
        document3 = Document(dom_id='doc3', item=item3)
        document3.save()
        item4 = Item(dom_name=u'f\u12341 item4', dom_id='item4')
        item4.save()
        document4 = Document(dom_id='doc4', item=item4)
        document4.save()

        item1.ready_for_qa()
        item2.ready_for_qa()
        item3.ready_for_qa()

        # set auth group and account
        self.groups = {}
        self.perms = {}
        self.group_names = ['Administrators', 'QA', 'QAManagers', 'Browsers', 'Project Managers']
        self.permissions = [('can_manage', 'Can manage the QA process'),
                            ('can_qa',     'Can QA items'),
                            ('can_browse', 'Can browse the QA app')]

        # create perm
        content_type, created = ContentType.objects.get_or_create(model = '', app_label = 'qa')
        for codename, name in self.permissions:
            perm, created = Permission.objects.get_or_create(codename=codename, name=name, content_type=content_type)
            self.perms[codename] = perm
        # create group
        for group_name in self.group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            self.groups[group_name] = group
        # add perm to group
        for group_name in 'QA', 'QAManagers':
            self.groups[group_name].permissions.add(self.perms['can_qa'])
            self.groups[group_name].permissions.add(self.perms['can_manage'])

        # create users for unittest
        user = User.objects.create_user(username='testuser', email='fake@cengage.com', password='testpw')
        group = Group.objects.get(name="QA")
        user.groups.add(group)
        user.save()

    def test_ReleaseItemView_WITHOUT_login(self):        
        response = self.client.get("/qa/manage/release/")
        self.assertEqual(response.status_code, 302)

    def test__get_m2_cho_meet(self):
        # set up test db (sqllite in ram)
        item = Item(dom_id='cho_bcrc_1933_0001_000_0000', dom_name='cho_bcrc_1933_0001_000_0000')
        item.save()
        item = Item(dom_id='cho_meet_2010_7771_001_0001', dom_name='cho_meet_2010_7771_001_0001')
        item.save()

        release_view = ReleaseView()
        self.assertEqual(1141, len(release_view._get_m2_cho_meet_psmids()))

        release_view._get_m2_cho_meet_psmids = MagicMock(return_value=['cho_meet_2010_7771_001_0001', 'does_not_exist'])

        m2_cho_meet = release_view._get_m2_cho_meet()
        self.assertIsNotNone(m2_cho_meet)
        self.assertEquals('cho_meet_2010_7771_001_0001', m2_cho_meet[0].dom_id)
        self.assertNotEqual('cho_bcrc_1933_0001_000_0000', m2_cho_meet[0].dom_id)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ReleaseViewTestCase),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
