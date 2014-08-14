import doctest
suite = doctest.DocFileSuite('test_dom_file_store.py')

if __name__ == '__main__':
    doctest.testfile("test_dom_file_store.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> from gaia.log.log import Log
>>> from gaia.dom.store.dom_file_store import _DomFileStore
>>> from gaia.dom.model.z_fake_item import FakeItem
>>> import json
>>> from collections import OrderedDict
>>> from test_utils.sorted_dict import sorted_dict
>>> 
>>> from testing.gaia_test import GaiaTest
>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config
>>> 
>>> class TestableDomFileStore(_DomFileStore):
...     def __init__(self, config, root_dir):
...         # normally created from a mixin
...         self._root_dir = root_dir
... 
...         self._log = Log.get_logger(self)
... 
...     # normally created from a mixin
...     def _item_dir(self, item_name, version_id, *args):
...         path_args = [self._root_dir, str(item_name), str(version_id)]
...         path_args.extend([str(arg) for arg in args])
...         item_fpath = os.path.join(*path_args)
... 
...         if not os.path.exists(item_fpath):
...             os.makedirs(item_fpath)
... 
...         return item_fpath
>>> 
>>> item = 'cho_iaxx_1963_0039_000_0000'
>>> dom_id = item
>>> dom_store_dir = test_dir
>>> item_fpath = os.path.join(test_dir, 'cho/inbox/htc/%s' % item)
>>> os.makedirs(item_fpath)
>>> 
>>> def print_sorted_pages_info(pages_info):
...     unsorted_dict = {}
...     for page_info in pages_info:
...         json_data = json.loads(page_info)
...         _dom_id =  json_data['_dom_id']
...         json_data_ordered = sorted_dict(json_data)
...         unsorted_dict[_dom_id] = json_data_ordered
...     for key in sorted(unsorted_dict.iterkeys()):
...         print unsorted_dict[key]
>>> 
>>> # A. add_item ----------------------------------------------
>>> # effectively sets up pre condition for subsequent 'assertions'
>>> 
>>> dom_file_store = TestableDomFileStore(config, dom_store_dir)
>>> fake_item = FakeItem(item_fpath, dom_id)
>>> dom_file_store.add_item(fake_item, item_index_id=1)
>>> 
>>> json_doc_info = dom_file_store.doc_info(item_dom_name=dom_id, item_index_id='1', document_dom_id=dom_id)
>>> print OrderedDict(json.loads(json_doc_info))
OrderedDict([(u'_dom_id', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/title', u'doc1'), (u'_dom_name', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/issue', u'111')])

>>> pages_info = dom_file_store.pages_info(item_dom_name=dom_id, item_index_id='1')
>>> unsorted_dict = {}
>>> print_sorted_pages_info(pages_info)
OrderedDict([(u'/page[1]/number', u'p1'), (u'/page[1]/title', u'page1'), (u'_dom_id', 1), (u'_dom_name', u'1')])
OrderedDict([(u'/page[2]/number', u'p2'), (u'/page[2]/title', u'page2'), (u'_dom_id', 2), (u'_dom_name', u'2')])
OrderedDict([(u'/page[3]/number', u'p3'), (u'/page[3]/title', u'page3'), (u'_dom_id', 3), (u'_dom_name', u'3')])
OrderedDict([(u'/page[4]/number', u'p4'), (u'/page[4]/title', u'page4'), (u'_dom_id', 4), (u'_dom_name', u'4')])

>>> json_page_info = dom_file_store.page_info(item_dom_name=dom_id, item_index_id='1', page_dom_id=4)
>>> print OrderedDict(json.loads(json_page_info))
OrderedDict([(u'/page[4]/title', u'page4'), (u'/page[4]/number', u'p4'), (u'_dom_name', u'4'), (u'_dom_id', 4)])

>>> json_chunk_info = dom_file_store.chunk_info(item_dom_name=dom_id, item_index_id='1', chunk_dom_id='1')
>>> print OrderedDict(json.loads(json_chunk_info))
OrderedDict([(u'_page_ids', [1]), (u'/article[1]/title', u'chunk1'), (u'_dom_name', u'1'), (u'_clip_ids', None), (u'_dom_id', 1), (u'/article[1]/author', u'Anon1'), (u'_is_binary', False)])

>>> json_clip_info = dom_file_store.clip_info(item_dom_name=dom_id, item_index_id='1', clip_dom_id='1')
>>> print OrderedDict(json.loads(json_clip_info))
OrderedDict([(u'_dom_id', 1), (u'_page_id', 1), (u'_dom_name', u'1'), (u'clip_k2', u'clip_v2'), (u'clip_k1', u'clip_v2')])

>>> json_link_info = dom_file_store.link_info(item_dom_name=dom_id, item_index_id='1', link_dom_id='1')
>>> print OrderedDict(json.loads(json_link_info))
OrderedDict([(u'link_k1', u'link_v2'), (u'link_k2', u'link_v2'), (u'_source', {u'chunk': None, u'page': u'1'}), (u'_dom_name', u'1'), (u'_dom_id', 1), (u'_target', {u'chunk': u'4', u'document': u'1', u'page': u'4'})])


>>> # B. change_chunks_info ----------------------------------------------
>>> chunk_info_changes = {1: {'/article[1]/title': 'title', '/article[1]/author': 'author'}}
>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1', chunk_info_changes=chunk_info_changes)
>>> json_chunk_info = dom_file_store.chunk_info(item_dom_name=dom_id, item_index_id='1', chunk_dom_id='1')
>>> print OrderedDict(json.loads(json_chunk_info))
OrderedDict([(u'_page_ids', [1]), (u'/article[1]/title', u'title'), (u'_dom_name', u'1'), (u'_clip_ids', None), (u'_dom_id', 1), (u'/article[1]/author', u'author'), (u'_is_binary', False)])

>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1', chunk_info_changes={})
>>> json_chunk_info = dom_file_store.chunk_info(item_dom_name=dom_id, item_index_id='1', chunk_dom_id='1')
>>> print OrderedDict(json.loads(json_chunk_info))
OrderedDict([(u'_page_ids', [1]), (u'/article[1]/title', u'title'), (u'_dom_name', u'1'), (u'_clip_ids', None), (u'_dom_id', 1), (u'/article[1]/author', u'author'), (u'_is_binary', False)])

>>> # C. change_doc_info ----------------------------------------------
>>> doc_info_changes = {item: {'/doc/title': 'doc2',  '/doc/issue': '1112'}}
>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1', doc_info_changes=doc_info_changes)
>>> json_doc_info = dom_file_store.doc_info(item_dom_name=dom_id, item_index_id='1', document_dom_id=dom_id)
>>> print OrderedDict(json.loads(json_doc_info))
OrderedDict([(u'_dom_name', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/title', u'doc2'), (u'_dom_id', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/issue', u'1112')])

>>> # tell DomFileStore to change 'nothing'
>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1',  doc_info_changes={})
>>> json_doc_info = dom_file_store.doc_info(item_dom_name=dom_id, item_index_id='1', document_dom_id=dom_id)
>>> print OrderedDict(json.loads(json_doc_info))
OrderedDict([(u'_dom_name', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/title', u'doc2'), (u'_dom_id', u'cho_iaxx_1963_0039_000_0000'), (u'/doc/issue', u'1112')])

>>> # D. change_pages_info ----------------------------------------------
>>> page_info_changes = {3: {'/page[3]/title': 'page33333', '/page[3]/number': 'number3333'}}
>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1', page_info_changes=page_info_changes)
>>> pages_info = dom_file_store.pages_info(item_dom_name=dom_id, item_index_id='1')
>>> print_sorted_pages_info(pages_info)
OrderedDict([(u'/page[1]/number', u'p1'), (u'/page[1]/title', u'page1'), (u'_dom_id', 1), (u'_dom_name', u'1')])
OrderedDict([(u'/page[2]/number', u'p2'), (u'/page[2]/title', u'page2'), (u'_dom_id', 2), (u'_dom_name', u'2')])
OrderedDict([(u'/page[3]/number', u'number3333'), (u'/page[3]/title', u'page33333'), (u'_dom_id', 3), (u'_dom_name', u'3')])
OrderedDict([(u'/page[4]/number', u'p4'), (u'/page[4]/title', u'page4'), (u'_dom_id', 4), (u'_dom_name', u'4')])

>>> # nothing to change should mean nothing gets changed
>>> dom_file_store.change_item_info(item_dom_name=dom_id, item_index_id='1', page_info_changes={})
>>> pages_info = dom_file_store.pages_info(item_dom_name=dom_id, item_index_id='1')
>>> print_sorted_pages_info(pages_info)
OrderedDict([(u'/page[1]/number', u'p1'), (u'/page[1]/title', u'page1'), (u'_dom_id', 1), (u'_dom_name', u'1')])
OrderedDict([(u'/page[2]/number', u'p2'), (u'/page[2]/title', u'page2'), (u'_dom_id', 2), (u'_dom_name', u'2')])
OrderedDict([(u'/page[3]/number', u'number3333'), (u'/page[3]/title', u'page33333'), (u'_dom_id', 3), (u'_dom_name', u'3')])
OrderedDict([(u'/page[4]/number', u'p4'), (u'/page[4]/title', u'page4'), (u'_dom_id', 4), (u'_dom_name', u'4')])

>>> # E. get_changes ----------------------------------------------
>>> fake_item.dom_name = item
>>> sorted(dom_file_store.get_changes(fake_item, item_index_id='1'))
[{u'_dom_name': u'cho_iaxx_1963_0039_000_0000', u'/doc/title': u'doc2', u'_dom_id': u'cho_iaxx_1963_0039_000_0000', u'/doc/issue': u'1112'}, {u'_dom_id': 1, u'_dom_name': u'1', u'/page[1]/number': u'p1', u'/page[1]/title': u'page1'}, {u'/page[2]/number': u'p2', u'/page[2]/title': u'page2', u'_dom_name': u'2', u'_dom_id': 2}, {u'/page[3]/title': u'page33333', u'/page[3]/number': u'number3333', u'_dom_name': u'3', u'_dom_id': 3}, {u'/page[4]/title': u'page4', u'/page[4]/number': u'p4', u'_dom_name': u'4', u'_dom_id': 4}, {u'_page_ids': [1], u'/article[1]/title': u'title', u'_dom_name': u'1', u'_clip_ids': None, u'_dom_id': 1, u'/article[1]/author': u'author', u'_is_binary': False}, {u'_page_ids': [1, 2], u'_dom_name': u'2', u'/article[2]/author': u'Anon2', u'_clip_ids': None, u'_dom_id': 2, u'/article[2]/title': u'chunk2', u'_is_binary': False}, {u'/article[3]/title': u'chunk3', u'_page_ids': [1, 2, 3], u'/article[3]/author': u'Anon3', u'_dom_name': u'3', u'_clip_ids': None, u'_dom_id': 3, u'_is_binary': False}, {u'_page_ids': [1, 2, 3, 4], u'_dom_name': u'4', u'_clip_ids': None, u'_dom_id': 4, u'/article[4]/author': u'Anon4', u'/article[4]/title': u'chunk4', u'_is_binary': False}]

>>> # F. chunks_info ----------------------------------------------
>>> sorted(dom_file_store.chunks_info(item_dom_name=dom_id, item_index_id='1'))
['{"/article[3]/title": "chunk3", "_clip_ids": null, "_dom_id": 3, "/article[3]/author": "Anon3", "_page_ids": [1, 2, 3], "_dom_name": "3", "_is_binary": false}', '{"_clip_ids": null, "_dom_id": 2, "_is_binary": false, "_page_ids": [1, 2], "/article[2]/author": "Anon2", "_dom_name": "2", "/article[2]/title": "chunk2"}', '{"_clip_ids": null, "_dom_id": 4, "/article[4]/author": "Anon4", "_page_ids": [1, 2, 3, 4], "_dom_name": "4", "/article[4]/title": "chunk4", "_is_binary": false}', '{"_page_ids": [1], "/article[1]/title": "title", "_dom_name": "1", "_clip_ids": null, "_dom_id": 1, "/article[1]/author": "author", "_is_binary": false}']

>>> test.tearDown()

'''
