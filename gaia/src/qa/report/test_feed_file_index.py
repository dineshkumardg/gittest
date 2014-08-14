import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from qa.models import FeedFile, DocumentFinalId, Item, Document, Page ,Chunk 
from django.contrib.auth.models import Group, User, Permission, ContentType

class FeedFileTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # set test data
        fname = ' 	NOINDEX-CHOA_20130530_012.xml.gz'
        when = '30 May 2013, 5:28 p.m.'
        group = 'meeting_page'
        num_docs = 20
        feed=FeedFile(fname=fname, when=when, group=group, num_docs=num_docs)
        feed.save()
        
        fname2 = 'PSM-CHOA_20130530_010.xml.gz'
        when2 = '30 May 2013, 4:28 p.m.'
        group2 = 'meeting_page'
        num_docs2 = 20
        feed2=FeedFile(fname=fname2, when=when2, group=group2, num_docs=num_docs2)
        feed2.save()
        
        item = Item(dom_id="cho_meet_2010_7771_050_0001", dom_name="cho_meet_2010_7771_050_0001") 
        item.save()
        feed3 = FeedFile(id="11", fname="PSM-CHOA_20130530_011.xml.gz", when="2013-05-30 17:28:45.751169", group="meeting_mega", num_docs="26")
        feed3.save()
        feed3.items.add(item)
        
        doc = Document(id="1",dom_id="cho_meet_2010_7771_050_0001", dom_name="cho_meet_2010_7771_050_0001" , item_id="1")    
        doc.save()
        doc_finalid = DocumentFinalId(final_id="DocumentFinalId",document=doc)
        doc_finalid.save()
        
        page = Page(document_id=doc.id, dom_name="cho_meet_2010_7771_050_0001")
        page.save()
        page.set_final_id('PAGE')
         
        chunk = Chunk(document_id=doc.id, dom_name="cho_meet_2010_7771_050_0001")
        chunk.save()
        chunk.set_final_id('CHUNK')
        
        
        # set auth group and account
        self.groups = {}
        self.perms = {}
        self.group_names = ['Administrators', 'QA', 'QAManagers', 'Browsers', 'Project Managers']
        self.permissions = [('can_manage', 'Can manage the QA process'),
                            ('can_qa',     'Can QA items'),
                            ('can_browse', 'Can browse the QA app')]

        content_type, created = ContentType.objects.get_or_create(model='', app_label='qa')
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

    def test_FeedFileView_OK(self):
        expected_num = 3
        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'page':'1',})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views
        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_FeedFileView_with_Search_ITEM(self):
        expected_num = 1
        expected_fname = 'PSM-CHOA_20130530_011.xml.gz'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'search_feed':'cho_meet_2010_7771_050_0001','search_for':'item'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.fname), expected_fname)
        self.assertEqual(len(response.context['queryset']), expected_num)
    
    def test_FeedFileView_with_Search_FEEDFILE(self):
        expected_num = 1
        expected_fname = 'PSM-CHOA_20130530_010.xml.gz'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'search_feed':'PSM-CHOA_20130530_010.xml.gz','search_for':'feed'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.fname), expected_fname)
        self.assertEqual(len(response.context['queryset']), expected_num)
    
    def test_FeedFileView_with_Search_PAGE_ASSERTIDS(self):
        expected_num = 1
        expected_fname = 'PSM-CHOA_20130530_011.xml.gz'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'search_feed':'PAGE','search_for':'asset_id'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.fname), expected_fname)
        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_FeedFileView_with_Search_Document_ASSERTIDS(self):
        expected_num = 1
        expected_fname = 'PSM-CHOA_20130530_011.xml.gz'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'search_feed':'DocumentFinalId','search_for':'asset_id'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.fname), expected_fname)
        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_FeedFileView_with_Search_CHUNK_ASSERTIDS(self):
        expected_num = 1
        expected_fname = 'PSM-CHOA_20130530_011.xml.gz'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/", {'search_feed':'CHUNK','search_for':'asset_id'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_index.html')
        
        # check variables returned from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.fname), expected_fname)
        self.assertEqual(len(response.context['queryset']), expected_num)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(FeedFileTestCase),
    ])  

test.tearDown()


if __name__ == "__main__":
    import testing
    testing.main(suite)
