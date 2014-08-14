import unittest
from testing.gaia_django_test import GaiaDjangoTest
test = GaiaDjangoTest()
test.setUp()


from django.test import TestCase
from django.test.client import Client
from qa.models import MCodes
from django.contrib.auth.models import Group, User, Permission, ContentType
from qa.mcode_view import MCodeView


class MCodeViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # set test data
        self.mcode = 'CODE'
        self.psmid = 'cho_meet_1943_first_000_0000'
        self.publication_title = 'Publication title of this item'
        self.m_code = MCodes(mcode=self.mcode, psmid=self.psmid, publication_title=self.publication_title)
        self.m_code.save()

        self.mcode = 'KODE'
        self.psmid = 'cho_bcrc_1934_second_000_0000'
        self.publication_title = 'Different title for a different item'
        self.m_code = MCodes(mcode=self.mcode, psmid=self.psmid, publication_title=self.publication_title)
        self.m_code.save()

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

    def test_MCodeView_OK(self):
        expected_num = 2

        self.client.login(username='testuser', password='testpw')
        response = self.client.get("/qa/mcodes/", {'page':'1',})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables returned from views
        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_MCodeView_with_MCode_Search_OK(self):
        expected_num = 1
        expected_mcode = 'CODE'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get('/qa/mcodes/', {'search_by':expected_mcode})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables returned from views -- search working
        for result in response.context['queryset']: 
            self.assertEqual(str(result.psmid), 'cho_meet_1943_first_000_0000')

        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_MCodeView_with_PSMID_Search_OK(self):
        expected_num = 1
        expected_psmid = 'cho_bcrc_1934_second_000_0000'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get('/qa/mcodes/', {'search_by':expected_psmid})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.psmid), 'cho_bcrc_1934_second_000_0000')

        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_MCodeView_with_Pub_Title_Search_OK(self):
        expected_num = 1
        expected_publication_title = 'Publication title of this item'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get('/qa/mcodes/', {'search_by':expected_publication_title})
        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- search working
        for result in response.context['queryset']:
            self.assertEqual(str(result.psmid), 'cho_meet_1943_first_000_0000')

        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_MCodeView_with_Partial_Search_OK(self):
        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item")
            ]
        expected_num = 2
        search_term = 'title'

        self.client.login(username='testuser', password='testpw')
        response = self.client.get('/qa/mcodes/', {'search_by':search_term})

        # check view status
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- search working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')
            self.assertIn(search_term, mcode.publication_title)

        self.assertEqual(len(response.context['queryset']), expected_num)

    def test_MCodeView_POST_ADD(self):
        expected_num = 3
        new_item_psm_id = u'cho_bcrc_1934_third_000_0000'
        new_item_mcode = u'EDOC'
        new_item_publication_title = u'A new third item'

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            MCodes(id=3, mcode=new_item_mcode, psmid=new_item_psm_id, publication_title=new_item_publication_title)
            ]

        expected_msg = MCodeView.MSG_ROW_ADDED
        expected_error = ''

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'delete_selected': [u'1'],
        u'add_item': [u'add'],
        u'add_psmid': [new_item_psm_id],
        u'add_mcode': [new_item_mcode],
        u'add_publication_title': [new_item_publication_title]})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- adding working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_ADD_EMPTY(self):
        expected_num = 2
        new_item_psm_id = u''
        new_item_mcode = u''
        new_item_publication_title = u''

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = u''
        expected_error = MCodeView.MSG_ALL_FIELDS_ARE_BLANK

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'delete_selected': [u'1'],
        u'add_item': [u'add'],
        u'add_psmid': [new_item_psm_id],
        u'add_mcode': [new_item_mcode],
        u'add_publication_title': [new_item_publication_title]})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- adding not working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_ADD_INCORRECT_PSMID(self):
        expected_num = 2
        new_item_psm_id = u'INCORRECT_PSMID'
        new_item_mcode = u'EDOC'
        new_item_publication_title = u'A new third item'

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = u''
        expected_error = MCodeView.MSG_PSMID_MUST_PASS_REGEX

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'delete_selected': [u'1'],
        u'add_item': [u'add'],
        u'add_psmid': [new_item_psm_id],
        u'add_mcode': [new_item_mcode],
        u'add_publication_title': [new_item_publication_title]})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- adding not working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_DELETE(self):
        expected_num = 1

        expected_context = [
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = MCodeView.MSG_ROWS_DELETED
        expected_error = ''

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={ u'delete_item': [u'delete selected'], u'delete_selected': [u'1']})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- deleting working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_NOT_DELETED(self):
        expected_num = 2

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = u''
        expected_error = MCodeView.MSG_ROWS_NOT_SELECTED

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={ u'delete_item': [u'delete selected']})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- deleting not working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_CHANGE(self):
        expected_num = 2

        expected_context = [
            MCodes(id=1, mcode="CODA", psmid=u"cho_meet_1943_change_000_0000", publication_title=u"Changed title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = MCodeView.MSG_CHANGES_APPLIED
        expected_error = ''

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'apply_changes': [u'apply changes'],
        u'id': [u'1',u'2'],
        u'psmid': [u'cho_meet_1943_change_000_0000', u'cho_bcrc_1934_second_000_0000'],
        u'mcode': [u'CODA', u'KODE'],
        u'publication_title': [u'Changed title of this item', u'Different title for a different item']})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- changing working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)
        self.assertEqual(response.context['error'], expected_error)

    def test_MCodeView_POST_CHANGE_EMPTY(self):
        expected_num = 2

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_msg = MCodeView.MSG_CHANGES_APPLIED

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'apply_changes': [u'apply changes'],
        u'id': [u'1',u'2'],
        u'psmid': [u'', u'cho_bcrc_1934_second_000_0000'],
        u'mcode': [u'', u'KODE'],
        u'publication_title': [u'', u'Different title for a different item']})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- changing not working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['msg'], expected_msg)

    def test_MCodeView_POST_CHANGE_INCORRECT_PSMID(self):
        expected_num = 2

        expected_context = [
            MCodes(id=1, mcode="CODE", psmid=u"cho_meet_1943_first_000_0000", publication_title=u"Publication title of this item"),
            MCodes(id=2, mcode="KODE", psmid=u"cho_bcrc_1934_second_000_0000", publication_title=u"Different title for a different item"),
            ]

        expected_error = MCodeView.MSG_PSMDS_MUST_PASS_REGEX

        self.client.login(username='testuser', password='testpw')
        response = self.client.post('/qa/mcodes/', data={
        u'apply_changes': [u'apply changes'],
        u'id': [u'1',u'2'],
        u'psmid': [u'INCORRECT_PSMID', u'INCORRECT_PSMID'],
        u'mcode': [u'CODE', u'KODE'],
        u'publication_title': [u'Publication title of this item', u'Different title for a different item']})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'qa/mcode.html')

        # check variables return from views -- changing not working
        response_context = response.context['queryset']
        for mcode in response_context:
            if mcode not in expected_context:
                self.fail('response.context != expected_context')

        self.assertEqual(len(response.context['queryset']), expected_num)

        self.assertEqual(response.context['error'], expected_error)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(MCodeViewTestCase),
    ])

test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
