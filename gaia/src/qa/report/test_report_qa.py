import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from qa.models import Item, Document, Page
from django.contrib.auth.models import Group, User, Permission, ContentType
   
class ReportQaViewTestCase(TestCase):

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

        document_dom_name = 'document1'
        document = Document(item_id=item1.id, dom_name=document_dom_name)
        document.save()
        document_dom_name2 = 'document2'
        document2 = Document(item_id=item2.id, dom_name=document_dom_name2)
        document2.save()
        document_dom_name3 = 'document3'
        document3 = Document(item_id=item3.id, dom_name=document_dom_name3)
        document3.save()

        page_dom_name = 'page1'
        page = Page(document=document, dom_name=page_dom_name)
        page.save()
        page_dom_name2 = 'page2'
        page2 = Page(document=document2, dom_name=page_dom_name2)
        page2.save()
        page_dom_name3 = 'page3'
        page3 = Page(document=document3, dom_name=page_dom_name3)
        page3.save()

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

    def test_ReportQaView_OK(self):       
        expected_num = 3
        expected_average_pages = 1
        expected_percent_pages = 0
        expected_template = 'qa/report/reports_qa.html'

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')

        response = self.client.get("/qa/reports/qa", {'page':'1',})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template)
       
        # check variables returned from view
        self.assertEqual(len(response.context['items']), expected_num)
        self.assertEqual(response.context['average_num_pages_per_item'], '%d' % expected_average_pages)
        self.assertEqual(response.context['average_percent_page_qa_per_item'], '%.1f' % expected_percent_pages)

    def test_ReportQaView_WITHOUT_login(self):       
        response = self.client.get("/qa/reports/qa", {'page':'1',})
        # check redirect to login page, error 302
        self.assertEqual(response.status_code, 302)

    def test_ReportQaView_with_Search_OK(self):
        expected_num = 1
        expected_average_pages = 1
        expected_percent_pages = 0
        search_by = 'item2'
        expected_dom_id = 'item2'
        expected_template = 'qa/report/reports_qa.html'

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')

        response = self.client.get("/qa/reports/qa", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template)
       
        for result in response.context['items']:
            self.assertEqual(result.dom_id, expected_dom_id)

        self.assertEqual(len(response.context['items']), expected_num)
        self.assertEqual(response.context['average_num_pages_per_item'], '%d' % expected_average_pages)
        self.assertEqual(response.context['average_percent_page_qa_per_item'], '%.1f' % expected_percent_pages)

    def test_ReportQaView_with_Search_EMPTY(self):
        expected_num = 0
        search_by = 'item5'
        expected_template = 'qa/report/reports_qa.html'

        #use test client to perform login
        self.client.login(username='testuser', password='testpw')

        response = self.client.get("/qa/reports/qa", {'search_by':search_by,})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, expected_template)
       
        # empty result
        self.assertEqual(len(response.context['items']), expected_num)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ReportQaViewTestCase),
    ])  

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
