import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from qa.models import Item
from django.contrib.auth.models import Group, User, Permission, ContentType

class ItemErrorViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # set test data
        self.err_type = 'QA'
        self.err_msg = 'item error this has bad data: sort it out or else.'
        self.dom_name = 'item_dom_name_1'
        self.item = Item(dom_name=self.dom_name, dom_id=self.dom_name)
        self.item.save()
        self.item.error(self.err_type, self.err_msg)
        
        self.err_type2 = 'Egest'
        self.err_msg2 = 'this has bad data: sort it out or else. item_dom_name_2'
        self.dom_name2 = 'item_dom_name_2'
        self.item2 = Item(dom_name=self.dom_name2, dom_id=self.dom_name2)
        self.item2.save()
        self.item2.error(self.err_type2, self.err_msg2)

        # set auth group and account
        self.groups = {}
        self.perms = {}
        self.group_names = ['Administrators', 'QA', 'QAManagers', 'Browsers', 'Project Managers']
        self.permissions = [('can_manage', 'Can manage the QA process'),
                            ('can_qa',     'Can QA items '),
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

    def test_ItemErrorView_OK(self):
        expected_num = 2
        expected_type_list = [self.err_type2, self.err_type]

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/item_errors", {'page':'1',})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/item_errors.html')
        
        # check variables returned from views
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_type_list)

    def test_ItemErrorView_with_Filter_OK(self):
        expected_num = 1
        expected_type = 'Egest'
        expected_type_list = [self.err_type2, self.err_type]

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/item_errors", {'filter_by': expected_type,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/item_errors.html')

        # check variables returned from views -- filter working
        for result in response.context['queryset']:
            self.assertEqual(result.err_type, expected_type)
        
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_type_list)

    def test_ItemErrorView_with_Search_OK(self):
        expected_num = 1
        expected_id = 'item error'
        expected_type_list = [str(self.err_type2), str(self.err_type)]

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/item_errors", {'search_by':expected_id,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/item_errors.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.item.dom_id),'item_dom_name_1')
        
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_type_list)

    def test_ItemErrorView_with_partial_Search_OK(self):
        expected_num = 1
        expected_id = 'item_dom_name_2'
        search_by = 'name_2'
        expected_type_list = [self.err_type2, self.err_type]

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/item_errors", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/item_errors.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(result.item.dom_id, expected_id)
        
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_type_list)

    def test_ItemErrorView_with_Search_result_EMPTY(self):
        expected_num = 0
        search_by = 'item_dom_name_3'
        expected_type_list = [self.err_type2, self.err_type]

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/item_errors", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/item_errors.html')
        
        # check variables returned from views -- search working
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_type_list)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ItemErrorViewTestCase),
    ])

 
test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
