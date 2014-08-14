import doctest
suite = doctest.DocFileSuite('test_dom_store.py')

if __name__ == '__main__':
    doctest.testfile("test_dom_store.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> django_test = GaiaDjangoTest()
>>> django_test.setUp()
>>> test_dir = django_test.test_dir

>>> import unittest
>>> import os
>>> import json
>>> from pprint import pprint
>>> from test_utils.sorted_dict import sorted_dict
>>> from gaia.log.log import Log
>>> from gaia.dom.store.dom_store import DomStore
>>> from gaia.dom.model.z_fake_item import FakeItem
>>> from gaia.dom.index.models import Item, Page, Chunk, AssetLink, DocumentLink, Clip, Document

>>> # setup ----------------------------------------------
>>> item_dom_name = 'cho_iaxx_1963_0039_000_0000'
>>> dom_id = item_dom_name
>>> item_fpath = os.path.join(test_dir, item_dom_name)
>>> os.makedirs(item_fpath)
>>> item = FakeItem(item_fpath, dom_id)

>>> store_dir = os.path.join(test_dir, 'store')
>>> dom_store = DomStore(store_dir)
>>> # add item ----------------------------------------------
>>> len(Item.objects.all())
0
>>> dom_store.add_item(item)
>>> len(Item.objects.all())
1
>>> # test that adding to the store creates the indexes in the DomIndex
>>> # after adding to the dom store, the item should now be available for direct access from the Dom Index (db):
>>> item_index = Item.objects.all()[0]
>>> item_index.dom_id
u'cho_iaxx_1963_0039_000_0000'

>>> # test that adding to the store saves the info objects in the DomFileStore
>>> document_index = Document.objects.get(item=item_index)
>>> dom_store.doc_info(item_dom_name, item_index.id, document_index.dom_id)
'{"_dom_name": "cho_iaxx_1963_0039_000_0000", "/doc/title": "doc1", "_dom_id": "cho_iaxx_1963_0039_000_0000", "/doc/issue": "111"}'

>>> # check the internal structure of the DomFileStore
>>> unsorted_fnames = []
>>> for root, dirs, fnames in os.walk(store_dir):
...    #print root[len(store_dir):], dirs, files
...    if fnames:
...       for fname in fnames:
...          unsorted_fnames.append(os.path.join(root[len(store_dir):], fname))
>>> sorted_fnames = sorted(unsorted_fnames)
>>> for fname in sorted_fnames:
...    print fname
/cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0000.xml
/cho_iaxx_1963_0039_000_0000/1/chunk/1/info.txt
/cho_iaxx_1963_0039_000_0000/1/chunk/2/info.txt
/cho_iaxx_1963_0039_000_0000/1/chunk/3/info.txt
/cho_iaxx_1963_0039_000_0000/1/chunk/4/info.txt
/cho_iaxx_1963_0039_000_0000/1/clip/1/info.txt
/cho_iaxx_1963_0039_000_0000/1/document/cho_iaxx_1963_0039_000_0000/info.txt
/cho_iaxx_1963_0039_000_0000/1/link/1/info.txt
/cho_iaxx_1963_0039_000_0000/1/page/1/info.txt
/cho_iaxx_1963_0039_000_0000/1/page/2/info.txt
/cho_iaxx_1963_0039_000_0000/1/page/3/info.txt
/cho_iaxx_1963_0039_000_0000/1/page/4/info.txt


>>> # test changes -------------------------------------------
>>> changes = dom_store.get_changes(item)
>>> print len(changes)
9

>>> pprint(changes)
[{u'/page[1]/number': u'p1',
  u'/page[1]/title': u'page1',
  u'_dom_id': 1,
  u'_dom_name': u'1'},
 {u'/article[1]/author': u'Anon1',
  u'/article[1]/title': u'chunk1',
  u'_clip_ids': None,
  u'_dom_id': 1,
  u'_dom_name': u'1',
  u'_is_binary': False,
  u'_page_ids': [1]},
 {u'/page[2]/number': u'p2',
  u'/page[2]/title': u'page2',
  u'_dom_id': 2,
  u'_dom_name': u'2'},
 {u'/article[2]/author': u'Anon2',
  u'/article[2]/title': u'chunk2',
  u'_clip_ids': None,
  u'_dom_id': 2,
  u'_dom_name': u'2',
  u'_is_binary': False,
  u'_page_ids': [1, 2]},
 {u'/page[3]/number': u'p3',
  u'/page[3]/title': u'page3',
  u'_dom_id': 3,
  u'_dom_name': u'3'},
 {u'/article[3]/author': u'Anon3',
  u'/article[3]/title': u'chunk3',
  u'_clip_ids': None,
  u'_dom_id': 3,
  u'_dom_name': u'3',
  u'_is_binary': False,
  u'_page_ids': [1, 2, 3]},
 {u'/page[4]/number': u'p4',
  u'/page[4]/title': u'page4',
  u'_dom_id': 4,
  u'_dom_name': u'4'},
 {u'/article[4]/author': u'Anon4',
  u'/article[4]/title': u'chunk4',
  u'_clip_ids': None,
  u'_dom_id': 4,
  u'_dom_name': u'4',
  u'_is_binary': False,
  u'_page_ids': [1, 2, 3, 4]},
 {u'/doc/issue': u'111',
  u'/doc/title': u'doc1',
  u'_dom_id': u'cho_iaxx_1963_0039_000_0000',
  u'_dom_name': u'cho_iaxx_1963_0039_000_0000'}]

>>> change_key = u'/doc/title'
>>> for change in changes:
...    if change.has_key(change_key):
...       print '/doc/title =', change[change_key]
/doc/title = doc1

>>> doc_info_changes={'cho_iaxx_1963_0039_000_0000': {'/doc/title': 'NEW_TITLE'}}
>>> page_info_changes={}
>>> chunk_info_changes={}

>>> dom_store.change_item_info(item_index, doc_info_changes, page_info_changes, chunk_info_changes)

>>> changes = dom_store.get_changes(item)
>>> print len(changes)
9
>>> for change in changes:
...    if change.has_key(change_key):
...       print '/doc/title =', change[change_key]
/doc/title = NEW_TITLE

>>> sorted_dict(json.loads(dom_store.doc_info(item_dom_name, item_index.id, document_index.dom_id)))
OrderedDict([(u'/doc/issue', u'111'), (u'/doc/title', u'NEW_TITLE'), (u'_dom_id', u'cho_iaxx_1963_0039_000_0000'), (u'_dom_name', u'cho_iaxx_1963_0039_000_0000')])


>>> # and finally, test it vanishes when deleted
>>> dom_store.delete_item(item_index)
>>> len(Item.objects.all())
0

>>> # test versioning -------------------------------------------
>>> dom_store.add_item(item)
>>> dom_store.add_item(item)
>>> dom_store.add_item(item)
>>> # there should now be 3 versions of the same item
>>> for item_index in Item.objects.all():
...     print item_index.id, item_index.dom_id, item_index.is_live
1 cho_iaxx_1963_0039_000_0000 False
2 cho_iaxx_1963_0039_000_0000 False
3 cho_iaxx_1963_0039_000_0000 True


# TODO: test these too...?
# def link_info(self, item_dom_name, item_index_id, link_dom_id):
# def page_info(self, item_dom_name, item_index_id, page_dom_id):
# def pages_info(self, item_dom_name, item_index_id):
# def chunk_info(self, item_dom_name, item_index_id, chunk_dom_id):
# def chunks_info(self, item_dom_name, item_index_id):

>>> django_test.tearDown()

'''
