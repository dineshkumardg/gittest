#!python -m doctest -v test_fix_form.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_global_changes_view.py')

if __name__ == '__main__':
    doctest.testfile("test_global_changes_view.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> print 'TODO make this work!!!! (fails to load templates)'
>>> TODO ! ***************************
TODO....

>>> from testing.gaia_django_test import GaiaDjangoTest
>>> test = GaiaDjangoTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config

>>> #import django.conf
>>> #print django.conf.settings.TEMPLATE_DIRS
>>> from django.test.client import Client
>>> c = Client()
>>> #response = c.post('/global_changes/', {'username': 'john', 'password': 'smith'})
>>> #response = c.post('/global_changes/', {})
>>> #response = c.post('/item/', {})
>>> #response = c.post('item/', {})
>>> response = c.get('/')
>>> response.status_code
200
>>> response = c.get('/customer/details/')
>>> response.content
'<!DOCTYPE html...'


>>> from mock import patch
>>> from qa.models import Item, ItemStatus, ItemError
>>> from qa.qa_link import QaLink

>>> # A: _get_list_of_global_changes_items ---------------------------------------
>>> item1 = Item(dom_id='cho_iaxx_1963_0039_000_0001')
>>> item1.save()
>>> item2 = Item(dom_id='cho_iaxx_1963_0039_000_0002')
>>> item2.save()
>>> item3 = Item(dom_id='cho_iaxx_1963_0039_000_0003')
>>> item3.save()
>>> item4 = Item(dom_id='cho_iaxx_1963_0039_000_0004')
>>> item4.save()

>>> query = 'doc_@contentType:* &rows=2&fl=doc_language'
>>> with patch('qa.qa_query.QaQuery.find_items') as mock_def:
...     mock_def.return_value = [item1, item2, item4]

>>> # B: _mark_items_as_rejected ---------------------------------------
>>> reason = 'blah blah blah'
>>> user = 'james'
>>> _mark_items_as_rejected(change_item_dom_ids, reason, user)
>>> rejected_items = ItemStatus.objects.filter(status=ItemStatus.REJECTED)
>>> print len(rejected_items)
3

>>> still_in_qa = ItemStatus.objects.filter(status=ItemStatus.IN_QA)
>>> print len(still_in_qa)
2

>>> test.tearDown()

'''
