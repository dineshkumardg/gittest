import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import Group, User, Permission, ContentType

class ManageViewTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        
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
        group = Group.objects.get(name="QAManagers")
        user.groups.add(group)
        user.save()

    def test_ManageView_OK(self):        
        self.client.login(username='testuser', password='testpw')
        response = self.client.get('/qa/manage/')
        self.assertEqual(response.status_code, 200)
        
        #self.assertTemplateUsed(response, 'qa/manage/manage.html')
            
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(ManageViewTestCase),
    ]) 
if __name__ == "__main__":
    import testing
    testing.main(suite)
