import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from qa.models import IngestError
from django.contrib.auth.models import Group, User, Permission, ContentType

class IngestErrorViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        
        # set test data
        self.provider1 = 'HTC'
        self.provider2 = 'Microformat'

        for i in range(0, 3):
            IngestError.add_error(self.provider1, 'report_%d' % i)

        for i in range(0, 2):
            IngestError.add_error(self.provider2, 'report_%d' % i)

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

    def test_IngestErrorView_OK(self):        
        expected_num = 5
        expected_filter_list = [self.provider1, self.provider2]
    
        #use test client to perform login
        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/ingest_errors", {'page':'1',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/ingest_errors.html')
        
        # check variables returned from view
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_filter_list)

    def test_IngestErrorView_with_Filter_OK(self):
        expected_provider = 'HTC'
        expected_num = 3
        expected_filter_list = [self.provider1, self.provider2]

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/ingest_errors", {'filter_by':expected_provider,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/ingest_errors.html')
        
        for result in response.context['queryset']:
            self.assertEqual(result.provider_name, expected_provider)
        
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_filter_list)

    def test_IngestErrorView_with_Search_OK(self):
        expected_num = 2
        search_by = 'report_1'
        expected_report = 'report_1'
        expected_filter_list = [self.provider1, self.provider2]

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/ingest_errors", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/ingest_errors.html')
        
        for result in response.context['queryset']:
            self.assertEqual(result.report, expected_report)

        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_filter_list)

    def test_IngestErrorView_with_Search_EMPTY(self):
        expected_num = 0
        search_by = 'report_5'
        expected_filter_list = [self.provider1, self.provider2]

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/ingest_errors", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/ingest_errors.html')
        
        self.assertEqual(len(response.context['queryset']), expected_num)
        self.assertEqual(response.context['filter_types'], expected_filter_list)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(IngestErrorViewTestCase),
    ]) 

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
