from testing.gaia_django_test import GaiaDjangoTest
_test = GaiaDjangoTest()
_test.setUp()

import unittest
from django.test import TestCase
from gaia.dom.index.models import Item, Document, Chunk, Page, Clip, DocumentLink, AssetLink

# NOTE: sqlite does not enforce varchar length
# WARNING: If adding TestCases here, MAKE SURE YOU ADD THEM TO tests.py

class _DocRelatedTest(TestCase):
    
    def setUp(self):
        self.item_dom_id = 'item_dom_id_1_yymmdd-yymmdd_01_02_03'
        self.item_dom_name = 'item_dom_NAME_something_more_descriptive'
        self.document_dom_id = 'document_dom_id_1_yymmdd-yymmdd_01_02_03'
        self.document_dom_name = 'document_dom_NAME_1_yymmdd-yymmdd_01_02_03'

        item = Item(dom_id=self.item_dom_id, dom_name=self.document_dom_name)
        item.save()
        document = Document(dom_id=self.document_dom_id, dom_name=self.item_dom_name, item=item)
        document.save()

        self.item = item
        self.document = document
        # Note: django will clean up between tests

class _PageRelatedTest(_DocRelatedTest):
    
    def setUp(self):
        _DocRelatedTest.setUp(self)
        self.page_dom_id = '1'
        self.page_dom_name = 'page1'
        page = Page(dom_id=self.page_dom_id, dom_name=self.page_dom_name, document=self.document)
        page.save()

        self.page = page

class _PageAndChunkRelatedTest(_PageRelatedTest):
    
    def setUp(self):
        _PageRelatedTest.setUp(self)
        self.chunk_dom_id = 'chunk_dom_ID'
        self.chunk_dom_name = 'chunk_dom_NAME_7_yymmdd-yymmdd_01_02_03'
        chunk = Chunk(dom_id=self.chunk_dom_id, dom_name=self.chunk_dom_name, document=self.document)
        chunk.save()

        self.chunk = chunk

class TestItem(_DocRelatedTest):
    
    def test_save(self):
        created = Item.objects.get(dom_id=self.item_dom_id)
        self.assertEqual(self.item_dom_id, created.dom_id)

    def test_save_is_live_NEW_VERSIONS(self):
        # test that creating new versions of the same item result in only one is_live version
        item2 = Item(dom_id='id_x', dom_name='a_dom_name')
        item2.save()

        item3 = Item(dom_id='id_x', dom_name='a_dom_name')
        item3.save()

        item4 = Item(dom_id='id_x', dom_name='a_dom_name')
        item4.save()

        items = Item.objects.filter(dom_id='id_x')
        self.assertEqual(3, len(items))

        live_items = Item.objects.filter(dom_id='id_x', is_live=True)
        self.assertEqual(1, len(live_items))

        non_live_items = Item.objects.filter(dom_id='id_x', is_live=False)
        self.assertEqual(2, len(non_live_items))


    def test_has_changed(self):
        item = Item.objects.get(dom_id=self.item_dom_id)
        self.assertFalse(item.has_changed)

        item.has_changed = True
        item.save()

        # requery
        self.assertTrue(Item.objects.get(dom_id=self.item_dom_id).has_changed)

    def test_duplicates(self):
        num_items = 3

        for i in range(0, num_items):
            item = Item(dom_id=self.item_dom_id, dom_name=self.item_dom_name)
            item.save()

        items = Item.objects.filter(dom_id=self.item_dom_id).order_by('date')
        self.assertEqual(num_items+1, len(items))

        # all "old" items with this dom_id should be set to "is an old version"
        is_lives = [item.is_live for item in items]
        for is_live in is_lives[:-1]:   # can't do negative indexing directly on a queryset :(
            self.assertFalse(is_live)

        # Only the latest one is "live"
        self.assertTrue(is_lives[-1])

class TestItem_related(_PageAndChunkRelatedTest):
    def test_chunk(self):
        chunk = self.item.chunk(self.chunk_dom_id)
        self.assertEqual(self.chunk, chunk)

    def test_chunks(self):
        chunks = self.item.chunks()
        self.assertEqual(1, len(chunks))
        self.assertEqual(self.chunk, chunks[0])

        chunk = Chunk(dom_id='2', dom_name='2', document=self.document)
        chunk.save()

        chunks = self.item.chunks()
        self.assertEqual(2, len(chunks))
        self.assertEqual(self.chunk, chunks[0])
        self.assertEqual(chunk, chunks[1])

    def test_page(self):
        page = self.item.page(self.page_dom_id)
        self.assertEqual(self.page, page)

    def test_pages(self):
        pages = self.item.pages()
        self.assertEqual(1, len(pages))
        self.assertEqual(self.page, pages[0])

        page = Page(dom_id='3', dom_name='p3', document=self.document)
        page.save()

        pages = self.item.pages()
        self.assertEqual(2, len(pages))
        self.assertEqual(self.page, pages[0])   # The first one should come first (must be ordered)
        self.assertEqual(page, pages[1])

class TestDocument(_DocRelatedTest):
    
    def test_save(self):
        created = Document.objects.get(dom_id=self.document_dom_id)
        
        self.assertEqual(self.document_dom_id, created.dom_id)
        self.assertEqual(self.item.id, self.document.item.id)
        
    def test_duplicates_ARE_ALLOWED(self):
        # WARNING: real code should always check Item.is_live.
        document = Document(dom_id=self.document_dom_id, item=self.item)
        document.save()
        document = Document(dom_id=self.document_dom_id, item=self.item)
        document.save()
        document = Document(dom_id=self.document_dom_id, item=self.item)
        document.save()

        created = Document.objects.filter(dom_id=self.document_dom_id)
        self.assertEqual(3+1, len(created))
        
class TestChunk(_DocRelatedTest):
    
    def test_save(self):
        dom_id = 'article_5'
        dom_name = 'The latest chunky article news from Andover'
        chunk = Chunk(dom_id=dom_id, dom_name=dom_name, document=self.document)
        chunk.save()

        created = Chunk.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(self.document.id, chunk.document.id)
        
    def test_duplicates_ARE_ALLOWED(self):
        dom_id = 'article_5'
        dom_name = 'The latest chunky article news from Andover'

        chunk = Chunk(dom_id=dom_id, dom_name=dom_name, document=self.document)
        chunk.save()
        chunk = Chunk(dom_id=dom_id, dom_name=dom_name, document=self.document)
        chunk.save()
        chunk = Chunk(dom_id=dom_id, dom_name=dom_name, document=self.document)
        chunk.save()

        created = Chunk.objects.filter(dom_id=dom_id)
        self.assertEqual(3, len(created))
        
class TestPage(_DocRelatedTest):
    
    def test_save(self):
        dom_id = 'page6'
        dom_name = 'The latest page of news from Andover Times'

        page = Page(dom_id=dom_id, dom_name=dom_name, document=self.document)
        page.save()

        created = Page.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(self.document.id, page.document.id)
        
    def test_duplicates_ARE_ALLOWED(self):
        dom_id = 'page6'
        dom_name = 'The latest page of news from Andover Times'

        page = Page(dom_id=dom_id, dom_name=dom_name, document=self.document)
        page.save()
        page = Page(dom_id=dom_id, dom_name=dom_name, document=self.document)
        page.save()
        page = Page(dom_id=dom_id, dom_name=dom_name, document=self.document)
        page.save()

        created = Page.objects.filter(dom_id=dom_id)
        self.assertEqual(3, len(created))
        
class TestClip(_PageRelatedTest):
    
    def test_save(self):
        dom_id = 'page6'
        dom_name = 'The latest page of news from Andover Times'
        clip = Clip(dom_id=dom_id, dom_name=dom_name, page=self.page)
        clip.save()

        created = Clip.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(self.page.id, clip.page.id)
        
    def test_duplicates_ARE_ALLOWED(self):
        dom_id = 'page6'
        dom_name = 'The latest page of news from Andover Times'

        clip = Clip(dom_id=dom_id, dom_name=dom_name, page=self.page)
        clip.save()
        clip = Clip(dom_id=dom_id, dom_name=dom_name, page=self.page)
        clip.save()
        clip = Clip(dom_id=dom_id, dom_name=dom_name, page=self.page)
        clip.save()

        created = Clip.objects.filter(dom_id=dom_id)
        self.assertEqual(3, len(created))
        
class TestAssetLink(_PageAndChunkRelatedTest):
    def test_save(self):
        dom_id = 'link6'
        dom_name = 'a link to an audio file'
        asset_fname = 'todays_meeting.mp3'
        link = AssetLink(dom_id=dom_id, dom_name=dom_name, document=self.document, asset_fname=asset_fname)
        link.save()

        created = AssetLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(None, created.chunk)
        self.assertEqual(None, created.page)
        self.assertEqual(asset_fname, created.asset_fname)
        
class TestDocumentLink(_PageAndChunkRelatedTest):
    
    def test_save(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document)
        link.save()

        created = DocumentLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(None, created.chunk)
        self.assertEqual(None, created.page)
        # Note that the target fields are NOT direct links within the index (they have to resolved to the latest _version_ of an item at runtime)
        self.assertEqual(u'', created.unresolved_target_item)
        self.assertEqual(u'', created.unresolved_target_chunk)
        self.assertEqual(u'', created.unresolved_target_page)
        # WARNING: target methods: these resolve the target index links each time to the latest live version of the target
        self.assertEqual(None, created.target_item)
        self.assertEqual(None, created.target_chunk)
        self.assertEqual(None, created.target_page)
        
    def test_save_WITH_SOURCE_chunk_no_page(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document, chunk=self.chunk)
        link.save()

        created = DocumentLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(self.chunk.id, created.chunk.id)
        self.assertEqual(None, created.page)
        # Note that the target fields are NOT direct links within the index (they have to resolved to the latest _version_ of an item at runtime)
        self.assertEqual(u'', created.unresolved_target_item)
        self.assertEqual(u'', created.unresolved_target_chunk)
        self.assertEqual(u'', created.unresolved_target_page)
        # WARNING: target methods: these resolve the target index links each time to the latest live version of the target
        self.assertEqual(None, created.target_item)
        self.assertEqual(None, created.target_chunk)
        self.assertEqual(None, created.target_page)

    def test_save_WITH_SOURCE_page_no_chunk(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document, page=self.page)
        link.save()

        created = DocumentLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(dom_id, created.dom_id)
        self.assertEqual(dom_name, created.dom_name)
        self.assertEqual(None, created.chunk)
        self.assertEqual(self.page.id, created.page.id)
        # Note that the target fields are NOT direct links within the index (they have to resolved to the latest _version_ of an item at runtime)
        self.assertEqual(u'', created.unresolved_target_item)
        self.assertEqual(u'', created.unresolved_target_chunk)
        self.assertEqual(u'', created.unresolved_target_page)
        # WARNING: target methods: these resolve the target index links each time to the latest live version of the target
        self.assertEqual(None, created.target_item)
        self.assertEqual(None, created.target_chunk)
        self.assertEqual(None, created.target_page)

    def test_save_WITH_TARGET_not_available(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'
        
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document, page=self.page, unresolved_target_item='NOT_YET_HERE')
        link.save()

        created = DocumentLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(u'NOT_YET_HERE', created.unresolved_target_item)
        self.assertEqual(u'', created.unresolved_target_chunk)
        self.assertEqual(u'', created.unresolved_target_page)

        # WARNING: target methods: these resolve the target index links each time to the latest live version of the target
        self.assertEqual(None, created.target_item) # NOTE: The target item does not yet exist, so is unresolvable.
        self.assertEqual(None, created.target_chunk)
        self.assertEqual(None, created.target_page)

    def test_save_WITH_TARGET_is_available(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'
        
        # try with just an item reference
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document, page=self.page, unresolved_target_item=self.item.dom_id)
        link.save()

        created = DocumentLink.objects.get(dom_id=dom_id)
        
        self.assertEqual(self.item.dom_id, created.unresolved_target_item)
        self.assertEqual(u'', created.unresolved_target_chunk)
        self.assertEqual(u'', created.unresolved_target_page)

        # WARNING: target methods: these resolve the target index links each time to the latest live version of the target
        self.assertEqual(self.item, created.target_item)
        self.assertEqual(None, created.target_chunk)
        self.assertEqual(None, created.target_page)

        # Now try with chunk and page
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document, page=self.page, unresolved_target_item=self.item.dom_id, unresolved_target_chunk=self.chunk.dom_id, unresolved_target_page=self.page.dom_id)
        link.save()

        created = DocumentLink.objects.get(id=link.id)

        self.assertEqual(self.item, created.target_item)
        self.assertEqual(self.chunk, created.target_chunk)
        self.assertEqual(self.page, created.target_page)

    def test_changing_target(self):
        # create a new version of the item, and make sure this one gets selected
        # as the "current live target", rather than the older one

        # This link points to the fourth article on the fourth page of item "id_x" 
        unresolved_target_item = 'id_x'
        unresolved_target_chunk = '4'
        unresolved_target_page = '4'

        item2 = Item(dom_id='id_x', dom_name='a_dom_name')
        item2.save()
        document2 = Document(dom_id='2', dom_name='2', item=item2)
        document2.save()
        chunk2 = Chunk(dom_id='2', dom_name='2', document=document2)
        chunk2.save()
        page2 = Page(dom_id='2', dom_name='2', document=document2)
        page2.save()

        link = DocumentLink(dom_id='99', dom_name='link99', document=document2, page=page2)
        link.unresolved_target_item  = unresolved_target_item
        link.unresolved_target_chunk = unresolved_target_chunk
        link.unresolved_target_page  = unresolved_target_page
        link.save()

        self.assertEqual(item2, link.target_item)
        self.assertEqual(None, link.target_chunk)   # '4' doesn't exist in this item
        self.assertEqual(None, link.target_page)    # '4' doesn't exist in this item

        item3 = Item(dom_id='id_x', dom_name='a_dom_name')
        item3.save()
        self.assertNotEqual(item2, link.target_item)
        self.assertEqual(item3, link.target_item)
        self.assertEqual(None, link.target_chunk)   # '4' doesn't exist in this item
        self.assertEqual(None, link.target_page)    # '4' doesn't exist in this item

        item4 = Item(dom_id='id_x', dom_name='a_dom_name')
        item4.save()
        document4 = Document(dom_id='4', dom_name='4', item=item4)
        document4.save()
        chunk4 = Chunk(dom_id='4', dom_name='4', document=document4)
        chunk4.save()
        page4 = Page(dom_id='4', dom_name='4', document=document4)
        page4.save()

        self.assertNotEqual(item3, link.target_item)
        self.assertEqual(item4, link.target_item)
        self.assertEqual(chunk4, link.target_chunk) # finally, these targets are resolvable
        self.assertEqual(page4, link.target_page)

    def test_duplicates_ARE_ALLOWED(self):
        dom_id = 'link6'
        dom_name = 'a link to news in Chelsea'

        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document)
        link.save()
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document)
        link.save()
        link = DocumentLink(dom_id=dom_id, dom_name=dom_name, document=self.document)
        link.save()

        created = DocumentLink.objects.filter(dom_id=dom_id)
        self.assertEqual(3, len(created))


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestItem),
    unittest.TestLoader().loadTestsFromTestCase(TestItem_related),
    unittest.TestLoader().loadTestsFromTestCase(TestDocument),
    unittest.TestLoader().loadTestsFromTestCase(TestChunk),
    unittest.TestLoader().loadTestsFromTestCase(TestPage),
    unittest.TestLoader().loadTestsFromTestCase(TestClip),
    unittest.TestLoader().loadTestsFromTestCase(TestAssetLink),
    unittest.TestLoader().loadTestsFromTestCase(TestDocumentLink),
    ])

_test.tearDown()

if __name__ == '__main__':
    import testing
    testing.main(suite)
