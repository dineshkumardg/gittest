import doctest
suite = doctest.DocFileSuite('test_dom_index.py')

if __name__ == '__main__':
    doctest.testfile("test_dom_index.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> django_test = GaiaDjangoTest()
>>> django_test.setUp()
>>> test_dir = django_test.test_dir

>>> import unittest
>>> import os
>>> from gaia.log.log import Log
>>> from gaia.dom.store.dom_index import _DomIndex
>>> from gaia.dom.model.z_fake_item import FakeItem
>>> from gaia.dom.index.models import Item, Page, Chunk, AssetLink, DocumentLink, Clip, Document

>>> def _print_item_index(item_index):
...     # can't print item_in_db as timestamps involved!
...     print 'id="%s" dom_id="%s" dom_name="%s" is_live="%s" has_changed="%s"' \
...         % (item_index.id, item_index.dom_id, item_index.dom_name, item_index.is_live, item_index.has_changed)

>>> def _test_item_exists(dom_id):
...     try:
...         _print_item_index(Item.objects.get(dom_id=dom_id))
...     except Item.DoesNotExist, e:
...         return e

>>> class TestableDomIndex(_DomIndex):
...     def __init__(self):
...         self._log = Log.get_logger(self)

>>> # A. add_item ----------------------------------------------
>>> item = 'cho_iaxx_1963_0039_000_0000'
>>> dom_id = item
>>> item_fpath = os.path.join(test_dir, item)
>>> os.makedirs(item_fpath)
>>> fake_item = FakeItem(item_fpath, dom_id)

>>> dom_index = TestableDomIndex()
>>> # pre-condition - the db should empty
>>> print _test_item_exists(dom_id)
Item matching query does not exist.

>>> # now, ltes put the item into the db
>>> item_index, superceded = dom_index.add_item(fake_item)
>>> print item_index.id, item_index.dom_id
1 cho_iaxx_1963_0039_000_0000

>>> print superceded
None

>>> # post-condition - the db should contain our fake_item
>>> _print_item_index(Item.objects.get(dom_id=dom_id))
id="1" dom_id="cho_iaxx_1963_0039_000_0000" dom_name="cho_iaxx_1963_0039_000_0000" is_live="True" has_changed="False"

>>> # document
>>> print Document.objects.all()
[<Document: DocumentIndex(id="#1", dom_id="cho_iaxx_1963_0039_000_0000" dom_name="cho_iaxx_1963_0039_000_0000")>]

>>> # pages
>>> print Page.objects.all()
[<Page: PageIndex(id="#1", dom_id="1" dom_name="1")>, <Page: PageIndex(id="#2", dom_id="2" dom_name="2")>, <Page: PageIndex(id="#3", dom_id="3" dom_name="3")>, <Page: PageIndex(id="#4", dom_id="4" dom_name="4")>]

>>> # chunks
>>> print Chunk.objects.all()
[<Chunk: ChunkIndex(id="#1", dom_id="1" dom_name="1" is_binary="False")>, <Chunk: ChunkIndex(id="#2", dom_id="2" dom_name="2" is_binary="False")>, <Chunk: ChunkIndex(id="#3", dom_id="3" dom_name="3" is_binary="False")>, <Chunk: ChunkIndex(id="#4", dom_id="4" dom_name="4" is_binary="False")>]

>>> # clips
>>> print Clip.objects.all()
[]

>>> # links
>>> print AssetLink.objects.all()
[<AssetLink: LinkIndex(id="#1", dom_id="1" dom_name="1")>]

>>> print DocumentLink.objects.all()
[<DocumentLink: LinkIndex(id="#2", dom_id="1" dom_name="1")>]

>>> # B. document_index ----------------------------------------------
>>> print dom_index.document_index(item_index)
DocumentIndex(id="#1", dom_id="cho_iaxx_1963_0039_000_0000" dom_name="cho_iaxx_1963_0039_000_0000")

>>> # C. mark_item_changed ----------------------------------------------
>>> item_index = Item.objects.get(dom_id=dom_id)
>>> _print_item_index(item_index)
id="1" dom_id="cho_iaxx_1963_0039_000_0000" dom_name="cho_iaxx_1963_0039_000_0000" is_live="True" has_changed="False"

>>> item_changed_index = dom_index.mark_item_changed(item_index.id)
>>> _print_item_index(item_changed_index)
id="1" dom_id="cho_iaxx_1963_0039_000_0000" dom_name="cho_iaxx_1963_0039_000_0000" is_live="True" has_changed="True"

>>> # D. delete_item ----------------------------------------------
>>> item = Item.objects.get(dom_id=dom_id)
>>> dom_index.delete_item(item)
>>> print _test_item_exists(dom_id)
Item matching query does not exist.

>>> django_test.tearDown()

'''
