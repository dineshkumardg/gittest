import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from qa.models import Item
from django.contrib.auth.models import Group, User, Permission, ContentType

class ReleasedItemViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        
        # set test data
        item1 = Item(dom_name='item1', dom_id='item1')
        item1.save()
        item2 = Item(dom_name=u'f\u12341 item2', dom_id='item2')
        item2.save()
        item3 = Item(dom_name=u'f\u12341 item3', dom_id='item3')
        item3.save()
        item4 = Item(dom_name=u'f\u12341 item4', dom_id='item4')
        item4.save()

        item1.released()
        item2.released()
        item3.released()

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

    def test_ReleasedItemView_OK(self):        
        expected_num = 3

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/released_items", {'page':'1',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/released_items.html')
        
        # check variables returned from view
        self.assertEqual(len(response.context['items']), expected_num)

    def test_ReleasedItemView_with_Search_OK(self):
        expected_num = 1
        search_by = 'item2'
        expected_dom_id = 'item2'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/released_items", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/released_items.html')
        
        for result in response.context['items']:
            self.assertEqual(result.dom_id, expected_dom_id)

        self.assertEqual(len(response.context['items']), expected_num)

    def test_ReleasedItemView_with_Search_EMPTY(self):
        expected_num = 0
        search_by = 'item5'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/released_items", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/released_items.html')
        
        # empty result
        self.assertEqual(len(response.context['items']), expected_num)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ReleasedItemViewTestCase),
    ]) 


test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
