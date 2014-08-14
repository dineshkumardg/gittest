import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()


from django.test import TestCase
from django.test.client import Client
from qa.models import Item, FeedFile, Document, DocumentFinalId
from django.contrib.auth.models import Group, User, Permission, ContentType


class FeedFileItemTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # set test data
        item1 = Item(dom_name='cho_meet_2010_7771_356_0001', dom_id='cho_meet_2010_7771_356_0001')
        item1.save()
        feed = FeedFile(id="11", fname="PSM-CHOA_20130530_011.xml.gz", when="2013-05-30 17:28:45.751169", group="meeting_mega", num_docs="26")
        feed.save()
        feed.items.add(item1)
        doc = Document(id="1", dom_id="cho_meet_2010_7771_356_0001", dom_name="cho_meet_2010_7771_356_0001", item_id="1")
        doc.save()
        doc_finalid = DocumentFinalId(final_id="DocumentFinalId", document=doc)
        doc_finalid.save()

        # set auth group and account
        self.groups = {}
        self.perms = {}
        self.group_names = ['Administrators', 'QA', 'QAManagers', 'Browsers', 'Project Managers']
        self.permissions = [('can_manage', 'Can manage the QA process'),
                            ('can_qa', 'Can QA items'),
                            ('can_browse', 'Can browse the QA app')]

        # create perm
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

    def test_FeedFile_ItemView_OK(self):
        expected_num = 1

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/feed_file_items", {'feed_file': 'PSM-CHOA_20130530_011.xml.gz'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_items.html')
        #check variables returned from view
        self.assertEqual(len(response.context['ids']), expected_num)

    def test_FeedFile_CHECK_MCODES(self):
        expected = '6SBM'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/reports/feed_file_index/feed_file_items", {'feed_file': 'PSM-CHOA_20130530_011.xml.gz'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/report/feed_file_items.html')
        #check variables returned from view
        self.assertEqual(response.context['content_set_definiton'], expected)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(FeedFileItemTestCase),
    ])

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
