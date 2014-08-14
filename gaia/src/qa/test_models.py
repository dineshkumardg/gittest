'''
avoid "ImportError: Settings cannot be imported, because environment variable DJANGO_SETTINGS_MODULE is undefined." by splitting imports!
'''

import unittest
from testing.gaia_django_test import GaiaDjangoTest
from mock import MagicMock, patch
from gaia.egest.outbox import Outbox
test = GaiaDjangoTest()
test.setUp()

from datetime import datetime
from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from qa.models import Item, Document, Chunk, Page, Clip, AssetLink, DocumentLink, ItemStatus, ItemError, IngestError, MCodes,\
    Approval, Language, RejectReason
from qa.models import DocumentFinalId, ChunkFinalId, PageFinalId, ClipFinalId, AssetLinkFinalId, DocumentLinkFinalId
from qa.models import FeedFile
from qa.models import MissingFinalId
from django.contrib.auth.models import User


# NOTE: sqlite does not enforce varchar length
class QaProxiesTestCase(TestCase):
    def test_proxies(self):
        # Note: this is a deliberately minimal test: these are pure proxy objects (currently)
        # tested in dom.index
        # This test simply exercises the proxying.
        dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=dom_name)
        item.save()

        created = Item.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))

        dom_name = 'document_dom_name_1_yymmdd-yymmdd_01_02_03'
        document = Document(dom_name=dom_name, item=item)
        document.save()

        created = Document.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))

        page = Page(dom_name=dom_name, document=document)
        page.save()

        created = Page.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))

        chunk = Chunk(dom_name=dom_name, document=document)
        chunk.save()

        created = Chunk.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))
        self.assertEqual(chunk.is_binary, False)

        chunk = Chunk(dom_name=dom_name, document=document, is_binary=True)
        chunk.save()
        created = Chunk.objects.filter(dom_name=dom_name)
        self.assertEqual(chunk.is_binary, True)

        dom_name = 'The latest clip of news from Andover Times'
        clip = Clip(dom_name=dom_name, page=page)
        clip.save()

        created = Clip.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))

        dom_name = 'a link to an mp3 file'
        link = AssetLink(dom_name=dom_name, document=document, asset_fname='the_news.mp3')  # may optioanlly have chunk and page sources too
        link.save()

        created = AssetLink.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))

        dom_name = 'a link to another document'
        link = DocumentLink(dom_name=dom_name, document=document, chunk=chunk, page=page, unresolved_target_item='doc1', unresolved_target_chunk='9', unresolved_target_page='24')
        link.save()

        created = DocumentLink.objects.filter(dom_name=dom_name)
        self.assertEqual(1, len(created))


class ItemTestCase(TestCase):
    def test_document(self):
        # get document for item
        item_id = 123
        item = Item(id=item_id)
        item.save()

        dom_name = 'document_1'
        document = Document(dom_name=dom_name, item=item)
        document.save()

        doc = item.document()
        self.assertEqual(document.id, doc.id)

    def test_document_links(self):
        # get document links for item
        item = Item(id=123)
        item.save()

        document = Document(dom_name='document_1', item=item)
        document.save()

        link1 = DocumentLink(document_id=document.id, dom_name='link1')
        link1.save()
        link2 = DocumentLink(document_id=document.id, dom_name='link2')
        link2.save()
        link3 = DocumentLink(document_id=document.id, dom_name='link3')
        link3.save()

        links = item.document_links()
        self.assertEqual(3, len(links))
        self.assertIn(link1, links)
        self.assertIn(link2, links)
        self.assertIn(link3, links)

    def test_document_link(self):
        # get a document link for item
        item = Item(id=123)
        item.save()

        document = Document(dom_name='document_1', item=item)
        document.save()

        dom_id1 = '1'
        dom_id2 = '2'
        dom_id3 = '3'

        link1 = DocumentLink(document_id=document.id, dom_name='link1', dom_id=dom_id1)
        link1.save()
        link2 = DocumentLink(document_id=document.id, dom_name='link2', dom_id=dom_id2)
        link2.save()
        link3 = DocumentLink(document_id=document.id, dom_name='link3', dom_id=dom_id3)
        link3.save()

        self.assertEqual(link1, item.document_link(dom_id1))
        self.assertEqual(link2, item.document_link(dom_id2))
        self.assertEqual(link3, item.document_link(dom_id3))

    def test_chunks(self):
        # get document chunks for item
        item = Item(id=123)
        item.save()

        document = Document(dom_name='document_1', item=item)
        document.save()

        chunk1 = Chunk(document_id=document.id, dom_name='chunk1')
        chunk1.save()
        chunk2 = Chunk(document_id=document.id, dom_name='chunk2')
        chunk2.save()
        chunk3 = Chunk(document_id=document.id, dom_name='chunk3')
        chunk3.save()

        chunks = item.chunks()
        self.assertEqual(3, len(chunks))
        self.assertIn(chunk1, chunks)
        self.assertIn(chunk2, chunks)
        self.assertIn(chunk3, chunks)

    def test_chunk(self):
        # get a document chunk for item
        item = Item(id=123)
        item.save()

        document = Document(dom_name='document_1', item=item)
        document.save()

        dom_id1 = '1'
        dom_id2 = '2'
        dom_id3 = '3'

        chunk1 = Chunk(document_id=document.id, dom_name='chunk1', dom_id=dom_id1)
        chunk1.save()
        chunk2 = Chunk(document_id=document.id, dom_name='chunk2', dom_id=dom_id2)
        chunk2.save()
        chunk3 = Chunk(document_id=document.id, dom_name='chunk3', dom_id=dom_id3)
        chunk3.save()

        self.assertEqual(chunk1, item.chunk(dom_id1))
        self.assertEqual(chunk2, item.chunk(dom_id2))
        self.assertEqual(chunk3, item.chunk('3'))

    def test_set_released(self):
        item_id = 123
        item = Item(id=item_id)
        item.save()  # Note that the item must exist before using this method.

        Item.set_released(item_id) 

        created = ItemStatus.objects.filter(item__id=item_id)
        self.assertEqual(1, len(created))
        self.assertEqual(ItemStatus.RELEASED, created[0].status)

    def test_set_released_FAILS_IF_NOT_EXISTS(self):
        item_id = 999
        self.assertRaises(ObjectDoesNotExist, Item.set_released, item_id)

    def test_set_error(self):
        # set_error gets populated into ItemError, there's no referential integrity on this table - so it looks like we could use any item_id value! '''
        error_type = 'my_type'
        error_msg = 'my_msg'
        item_id = 123
        item = Item(id=item_id)
        item.save()  # Note that the item must exist before using this method.

        Item.set_error(item_id, error_type, error_msg)

        created = ItemError.objects.filter(item=item_id)
        item_error = created[0]
        self.assertEqual(1, len(created))
        self.assertEqual(error_type, item_error.err_type)
        self.assertEqual(error_msg, item_error.err_msg)

    def test_set_error_FAILS_IF_NOT_EXISTS(self):
        items = Item.objects.all()
        self.assertEqual(0, len(items))

        item_id = 123
        #item = Item(id=item_id)
        #item.save() # Note that the item must exist before using this method.
        self.assertRaises(ObjectDoesNotExist, Item.set_error, item_id, 'err_type', 'err_msg')

    def test_reject(self):
        # Expectations/setup
        msg = u'f\u12341 this has bad data: sort it out or else.'
        dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=dom_name)
        item.save()

        # Test
        item.reject(msg)

        # Assertions
        created = ItemStatus.objects.filter(item=item.id)
        item_status = created[0]
        self.assertEqual(1, len(created))
        self.assertEqual(ItemStatus.REJECTED, item_status.status)

        created = ItemError.objects.filter(item=item.id)
        item_error = created[0]
        self.assertEqual(1, len(created))
        self.assertEqual('QA', item_error.err_type)
        self.assertEqual(msg, item_error.err_msg)

    def test_rejections(self):
        item1 = Item(dom_name='dom_name_100')
        item1.save()
        item1.reject('reject reason 100')

        item2 = Item(dom_name='dom_name_200')
        item2.save()

        item3 = Item(dom_name='dom_name_300')
        item3.save()
        item3.reject('reject reason 300')

        item4 = Item(dom_name='dom_name_400')
        item4.save()

        rejected_items = Item.rejections()
        self.assertEquals(2, rejected_items.count())

    def test_error(self):
        # Expectations/setup
        err_type = 'QA: Invalid author'
        err_msg = u'f\u12341 this has bad data: sort it out or else.'
        dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=dom_name)
        item.save()

        # Test
        item.error(err_type, err_msg)

        # with unicode
        err_msg = u'f\u12341 this has bad data: sort it out or else.'
        item.error(err_type, err_msg)

        # Assertions
        created = ItemStatus.objects.filter(item=item.id)
        self.assertEqual(1, len(created))
        item_status = created[0]
        self.assertEqual(ItemStatus.ERROR, item_status.status)

        created = ItemError.objects.filter(item=item.id)
        item_error = created[0]
        self.assertEqual(2, len(created))
        self.assertEqual(err_type, item_error.err_type)
        self.assertEqual(err_msg, item_error.err_msg)

    def test_ready_for_release(self):
        # Expectations/setup
        item1 = Item(dom_name='item1')
        item1.save()
        item2 = Item(dom_name=u'f\u12341 item2')
        item2.save()

        # Test
        item2.ready_for_release()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.READY_FOR_RELEASE)
        self.assertEqual(1, len(ready))

        # Test
        item1.ready_for_release()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.READY_FOR_RELEASE)
        self.assertEqual(2, len(ready))

    def test_ready_for_release_only_xml(self):
        # Expectations/setup
        item1 = Item(dom_name='item1')
        item1.save()
        item2 = Item(dom_name=u'f\u12341 item2')
        item2.save()

        # Test
        item2.ready_for_release_only_xml()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.READY_FOR_RELEASE_ONLY_XML)
        self.assertEqual(1, len(ready))

        # Test
        item1.ready_for_release_only_xml()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.READY_FOR_RELEASE_ONLY_XML)
        self.assertEqual(2, len(ready))

    def test_ready_for_qa(self):
        # Expectations/setup
        item1 = Item(dom_name='item1')
        item1.save()
        item2 = Item(dom_name=u'f\u12341 item2')
        item2.save()

        # Test
        item2.ready_for_qa()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.IN_QA)
        self.assertEqual(1, len(ready))

        # Test
        item1.ready_for_qa()

        # Assertions
        ready = ItemStatus.objects.filter(status=ItemStatus.IN_QA)
        self.assertEqual(2, len(ready))

    def test_in_qa(self):
        # Expectations/setup
        item1 = Item(dom_id='1', dom_name='item1', is_live=True)
        item1.save()
        item2 = Item(dom_id='2', dom_name='item2', is_live=True)
        item2.save()

        items = Item.in_qa()
        self.assertEqual(0, len(items))

        item1.ready_for_qa()
        items = Item.in_qa()
        self.assertEqual(1, len(items))

        item2.ready_for_qa()
        items = Item.in_qa()
        self.assertEqual(2, len(items))

        item2.ready_for_release()
        items = Item.in_qa()
        self.assertEqual(1, len(items))

    def test_without_any_approval(self):
        # no approval exists for this item

        psmid = 'psmid1'
        item = Item(dom_id=psmid, dom_name=psmid, is_live=True)
        item.save()

        self.assertFalse(item.with_approval())

    def test_without_approval(self):
        expected_approval = False

        psmid = 'psmid2'
        item = Item(dom_id=psmid, dom_name=psmid, is_live=True)
        item.save()

        approval = Approval(item_id=item.id, approved=expected_approval, notes='', who_id=1)
        approval.save()

        self.assertFalse(item.with_approval())

    def test_with_approval(self):
        expected_approval = True

        psmid = 'psmid3'
        item = Item(dom_id=psmid, dom_name=psmid, is_live=True)
        item.save()

        approval = Approval(item_id=item.id, approved=expected_approval, notes='', who_id=1)
        approval.save()

        self.assertTrue(item.with_approval())

    def test_release_next(self):
        # this also tests item.in_exporting()
        expected_names = set()
        expected_names_2nd = set()
        expected_names_3rd = set()

        for i in range(0, 3):
            item_dom_name = "cho_meet_" + 'NOTready_item' + str(i)
            item = Item(dom_name=item_dom_name)
            item.save()
            item._set_status(ItemStatus.IN_QA)

        items = Item.in_exporting()
        self.assertEqual(0, len(items))

        for i in range(0, 7):
            item_dom_name = "cho_meet_" + 'ready_item' + str(i)
            item = Item(dom_name=item_dom_name, dom_id=item_dom_name)
            item.save()
            item._set_status(ItemStatus.READY_FOR_RELEASE)
            expected_names.add(item.dom_name)

        for i in range(0, 7):
            item_dom_name = "cho_bcrc_" + 'ready_item' + str(i)
            item = Item(dom_name=item_dom_name, dom_id=item_dom_name)
            item.save()
            item._set_status(ItemStatus.READY_FOR_RELEASE)
            expected_names_2nd.add(item.dom_name)

        for i in range(0, 7):
            item_dom_name = "cho_book_" + 'ready_item' + str(i)
            item = Item(dom_name=item_dom_name, dom_id=item_dom_name)
            item.save()
            item._set_status(ItemStatus.READY_FOR_RELEASE)
            expected_names_3rd.add(item.dom_name)

        items = Item.in_exporting()
        self.assertEqual(0, len(items))

        items = Item.in_ready_for_release()
        self.assertEqual(21, len(items))

        # first release -> all meetings
        item_ids, item_names, only_xml, create_feed = Item.release_next()
        self.assertEqual(expected_names, set(item_names))
        self.assertEqual(create_feed, True)

        # WARNING: NAMES GO IN NON-UNICODE AND COME OUT AS UNICODE (TODO: INVESTIGATE)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

        items = Item.in_exporting()
        self.assertEqual(7, len(items))

        # 2nd release -> all conference series
        item_ids, item_names, only_xml, create_feed = Item.release_next()
        self.assertEqual(expected_names_2nd, set(item_names))
        self.assertEqual(create_feed, True)

        # WARNING: NAMES GO IN NON-UNICODE AND COME OUT AS UNICODE (TODO: INVESTIGATE)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

        items = Item.in_exporting()
        self.assertEqual(14, len(items))

        # 3nd release -> all books
        item_ids, item_names, only_xml, create_feed = Item.release_next()
        self.assertEqual(expected_names_3rd, set(item_names))
        self.assertEqual(create_feed, True)

        # WARNING: NAMES GO IN NON-UNICODE AND COME OUT AS UNICODE (TODO: INVESTIGATE)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

    def test_release_next_WITH_LIMIT(self):

        for i in range(0, 3):
            item_dom_name = "cho_meet_" + 'NOTready_item'
            item = Item(dom_name=item_dom_name)
            item.save()
            item._set_status(ItemStatus.IN_QA)

        expected_names = []
        expected_names_2nd = []

        for i in range(0, 7):
            item_dom_name = "cho_meet_" + 'ready_item' + str(i)
            item = Item(dom_name=item_dom_name, dom_id=item_dom_name)
            item.save()
            item._set_status(ItemStatus.READY_FOR_RELEASE)
            expected_names.append(item.dom_name)

        for i in range(0, 7):
            item_dom_name = "cho_bcrc_" + 'ready_item' + str(i)
            item = Item(dom_name=item_dom_name, dom_id=item_dom_name)
            item.save()
            item._set_status(ItemStatus.READY_FOR_RELEASE)
            expected_names_2nd.append(item.dom_name)

        # 1st release -> 4 meet
        item_ids, item_names, only_xml, create_feed = Item.release_next(limit=4)
        self.assertEqual(set(expected_names[:4]), set(item_names))
        self.assertEqual(create_feed, False)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

        # 2st release -> the rest 3 meet, create feed file
        item_ids, item_names, only_xml, create_feed = Item.release_next(limit=4)
        self.assertEqual(set(expected_names[4:]), set(item_names))
        self.assertEqual(create_feed, True)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

        # 3rd release -> 4 bcrc
        item_ids, item_names, only_xml, create_feed = Item.release_next(limit=4)
        self.assertEqual(set(expected_names_2nd[:4]), set(item_names))
        self.assertEqual(create_feed, False)
        for item_id in item_ids:    
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

        # 4rd release -> the rest 3 bcrc, create feed file
        item_ids, item_names, only_xml, create_feed = Item.release_next(limit=4)
        self.assertEqual(set(expected_names_2nd[4:]), set(item_names))
        self.assertEqual(create_feed, True)
        for item_id in item_ids:
            item_status = ItemStatus.objects.get(item__id=item_id)
            self.assertEqual(ItemStatus.EXPORTING, item_status.status)

    def test__set_status(self):
        item_dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=item_dom_name)
        item.save()

        item._set_status(ItemStatus.IN_QA)   # Hmm... maybe should be Item.IN_QA?
        item_status = ItemStatus.objects.get(item=item.id)
        self.assertEqual(ItemStatus.IN_QA, item_status.status)

        item._set_status(ItemStatus.READY_FOR_RELEASE)
        item_status = ItemStatus.objects.get(item=item.id)
        self.assertEqual(ItemStatus.READY_FOR_RELEASE, item_status.status)

    def test_is_fully_linked(self):  # sorry, but this is a doctest-style/narrative unittest (=a lot less code)!
        item = Item(id=123)
        item.save()

        document = Document(dom_name='document123', item=item)
        document.save()

        # test an item with NO lINKS
        self.assertTrue(item.is_fully_linked())

        link = DocumentLink(document_id=document.id, dom_name='link1')
        link.save()

        # test an item with 1 link, but NO TARGET
        self.assertTrue(item.is_fully_linked())

        # test an item with 1 link, and a target item that is missing
        link.unresolved_target_item = 'target_item_1'
        link.save()

        self.assertFalse(item.is_fully_linked())

        target_item = Item(id=321, dom_id='target_item_1')  # Note that the target is the dom_id (not the dom_name)
        target_item.save()
        target_document = Document(dom_name='dtarget_document_1', item=target_item)
        target_document.save()

        self.assertTrue(item.is_fully_linked())   # now we're linked with a target!

        link.unresolved_target_chunk = 'target_chunk_1'
        link.save()
        self.assertFalse(item.is_fully_linked())   # no matching chunk target (yet)

        chunk = Chunk(dom_id='target_chunk_1', document=target_document)
        chunk.save()

        self.assertTrue(item.is_fully_linked())   # both chunk and item natch

        link.unresolved_target_page = 'target_page_1'
        link.save()
        self.assertFalse(item.is_fully_linked())   # no matching page target (yet)

        page = Page(dom_id='target_page_1', document=target_document)
        page.save()

        self.assertTrue(item.is_fully_linked())   # item, chunk and page all match

        link.unresolved_target_chunk = 'MISSING'
        link.save()
        self.assertFalse(item.is_fully_linked())   # no matching chunk target (yet), buti item and page match

        link.unresolved_target_chunk = 'target_chunk_1'
        link.save()
        self.assertTrue(item.is_fully_linked())   # matches again.

        # And finally add a link to another target
        link2 = DocumentLink(document_id=document.id, dom_name='link1')
        link2.unresolved_target_item = 'target_item_2'
        link2.save()

        self.assertFalse(item.is_fully_linked())   # first link is OK, but second is not.

        target_item_2 = Item(id=222, dom_id='target_item_2')
        target_item_2.save()
        target_document_2 = Document(dom_id='target_document_2', item=target_item_2)
        target_document_2.save()

        self.assertTrue(item.is_fully_linked())   # both links ok now.


class ItemStatusTestCase(TestCase):
    def test(self):
        item_dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=item_dom_name)
        item.save()

        item_status = ItemStatus(item=item, status=ItemStatus.IN_QA)
        item_status.save()

        created = ItemStatus.objects.filter(item=item.id)
        self.assertEqual(1, len(created))

        item_status = created[0]
        self.assertEqual(ItemStatus.IN_QA, item_status.status)

        # try changing the status..
        item_status, created = ItemStatus.objects.get_or_create(item=item)
        item_status.save()

        created = ItemStatus.objects.filter(item=item.id)
        self.assertEqual(1, len(created))

        item_status = created[0]
        item_status.status = ItemStatus.READY_FOR_RELEASE
        item_status.save()

        created = ItemStatus.objects.filter(item=item.id)
        self.assertEqual(1, len(created))
        item_status = created[0]
        self.assertEqual(ItemStatus.READY_FOR_RELEASE, item_status.status)

    def test__str(self):
        # test patch datetime
        item_dom_name = 'item_dom_name_1_yymmdd-yymmdd_01_02_03'
        item = Item(dom_name=item_dom_name)
        item.save()

        item_status = ItemStatus(item=item, status=ItemStatus.IN_QA)
        item_status.save()

        created = ItemStatus.objects.filter(item=item.id)
        test_date = created[0].when.date()

        now = datetime.now()
        self.assertEqual(now.date(), test_date)  # at least, the date is on same day?

        datetime.strptime(str(created[0].when), "%Y-%m-%d %H:%M:%S.%f")  # time date should match this format


class IngestErrorTestCase(TestCase):
    def test_error(self):
        # Expectations/setup
        provider1 = 'HTC'
        provider2 = 'Microformat'

        # Test
        for i in range(0, 3):
            IngestError.add_error(provider1, 'report_%d' % i)

        for i in range(0, 7):
            IngestError.add_error(provider2, 'report_%d' % i)

        p1_errs = IngestError.provider_errors(provider1)
        p2_errs = IngestError.provider_errors(provider2)

        # Assertions
        self.assertEqual(3 + 7, len(IngestError.objects.all()))

        self.assertEqual(3, len(p1_errs))
        created = IngestError.objects.filter(provider_name=provider1)
        self.assertEqual(3, len(created))

        self.assertEqual(7, len(p2_errs))
        created = IngestError.objects.filter(provider_name=provider2)
        self.assertEqual(7, len(created))


class DocumentFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        created = DocumentFinalId.objects.filter(document=document.id)
        self.assertEqual(0, len(created))

        self.assertRaises(MissingFinalId, document.get_final_id)  # check special "DoesNotExist" class

        final_id1 = 'f1'
        document.set_final_id(final_id1)

        created = DocumentFinalId.objects.filter(document=document.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(document_dom_name, fid.document.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        document.set_final_id(final_id2)

        final_id2 = u'f\u12341'
        document.set_final_id(final_id2)

        created = DocumentFinalId.objects.filter(document=document.id)
        self.assertEqual(1, len(created))   # shold still only be one entry for this document

        fid = created[0]
        self.assertEqual(document_dom_name, fid.document.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this document

        # try getting the final_id with the accessor method
        self.assertEqual(final_id2, document.get_final_id())


class PageFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        page_dom_name = 'page1'
        page = Page(document_id=document.id, dom_name=page_dom_name)
        page.save()

        created = PageFinalId.objects.filter(page=page.id)
        self.assertEqual(0, len(created))
        self.assertRaises(MissingFinalId, page.get_final_id)  # check special "DoesNotExist" class

        final_id1 = 'f1'
        page.set_final_id(final_id1)

        created = PageFinalId.objects.filter(page=page.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(page_dom_name, fid.page.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        page.set_final_id(final_id2)

        final_id2 = u'f\u12341f2'
        page.set_final_id(final_id2)

        created = PageFinalId.objects.filter(page=page.id)
        self.assertEqual(1, len(created))   # shold still only be one entry for this page

        fid = created[0]
        self.assertEqual(page_dom_name, fid.page.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this page

        # try getting the final_id with the accessor method
        self.assertEqual(final_id2, page.get_final_id())


class ChunkFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        page_dom_name = 'page1'
        page = Page(document=document, dom_name=page_dom_name)
        page.save()

        chunk_dom_name = 'chunk1'
        chunk = Chunk(document=document, dom_name=chunk_dom_name)
        chunk.save()

        created = ChunkFinalId.objects.filter(chunk=chunk.id)
        self.assertEqual(0, len(created))
        self.assertRaises(MissingFinalId, chunk.get_final_id)  # check special "DoesNotExist" class

        final_id1 = 'f1'
        chunk.set_final_id(final_id1)

        created = ChunkFinalId.objects.filter(chunk=chunk.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(chunk_dom_name, fid.chunk.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        chunk.set_final_id(final_id2)

        created = ChunkFinalId.objects.filter(chunk=chunk.id)
        self.assertEqual(1, len(created))   # shold still only be one entry for this chunk

        fid = created[0]
        self.assertEqual(chunk_dom_name, fid.chunk.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this chunk

        # try getting the final_id with the accessor method
        self.assertEqual(final_id2, chunk.get_final_id())

    def test_UNICODE(self):
        item_dom_name = u'it\u1234em1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = u'doc\u1234ument1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        page_dom_name = u'pa\u1234ge1'
        page = Page(document=document, dom_name=page_dom_name)
        page.save()

        chunk_dom_name = u'chu\u1234nk1'
        chunk = Chunk(document=document, dom_name=chunk_dom_name)
        chunk.save()

        final_id1 = u'f\u12341'
        chunk.set_final_id(final_id1)

        final_id =  chunk.get_final_id()  # TODO


class ClipFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        page_dom_name = 'page1'
        page = Page(document=document, dom_name=page_dom_name)
        page.save()

        clip_dom_name = 'clip1'
        clip = Clip(page=page, dom_name=clip_dom_name)
        clip.save()

        created = ClipFinalId.objects.filter(clip=clip.id)
        self.assertEqual(0, len(created))

        final_id1 = 'f1'
        clip.set_final_id(final_id1)

        created = ClipFinalId.objects.filter(clip=clip.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(clip_dom_name, fid.clip.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        clip.set_final_id(final_id2)

        final_id2 = u'f\u12341'
        clip.set_final_id(final_id2)

        created = ClipFinalId.objects.filter(clip=clip.id)
        self.assertEqual(1, len(created))  # should still only be one entry for this clip

        fid = created[0]
        self.assertEqual(clip_dom_name, fid.clip.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this clip


class AssetLinkFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        link_dom_name = 'link1'
        link = AssetLink(document_id=document.id, dom_name=link_dom_name)
        link.save()

        created = AssetLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(0, len(created))

        final_id1 = 'f1'
        link.set_final_id(final_id1)

        final_id1 = u'f\u12341f1'
        link.set_final_id(final_id1)

        created = AssetLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(link_dom_name, fid.link.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        link.set_final_id(final_id2)

        created = AssetLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(1, len(created))   # should still only be one entry for this link

        fid = created[0]
        self.assertEqual(link_dom_name, fid.link.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this link


class DocumentLinkFinalIdTestCase(TestCase):
    def test(self):
        item_dom_name = 'item1'
        item = Item(dom_name=item_dom_name)
        item.save()

        document_dom_name = 'document1'
        document = Document(item_id=item.id, dom_name=document_dom_name)
        document.save()

        link_dom_name = 'link1'
        link = DocumentLink(document_id=document.id, dom_name=link_dom_name)
        link.save()

        created = DocumentLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(0, len(created))

        final_id1 = 'f1'
        link.set_final_id(final_id1)

        final_id1 = u'f\u12341f1'
        link.set_final_id(final_id1)

        created = DocumentLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(1, len(created))

        fid = created[0]
        self.assertEqual(link_dom_name, fid.link.dom_name)
        self.assertEqual(final_id1, fid.final_id)

        # try changing the final_id
        final_id2 = 'f2'
        link.set_final_id(final_id2)

        created = DocumentLinkFinalId.objects.filter(link=link.id)
        self.assertEqual(1, len(created))  # shold still only be one entry for this link

        fid = created[0]
        self.assertEqual(link_dom_name, fid.link.dom_name)
        self.assertEqual(final_id2, fid.final_id)  # changed final_id for this link


class FeedFileTestCase(TestCase):
    def test_one(self):
        items = []
        num_items = 5
        item_ids = range(1, num_items + 1)

        for i in range(0, num_items):
            dom_name = 'item_%d' % i
            item = Item(dom_name=dom_name)
            item.save()
            items.append(item)

        ff = FeedFile(fname='f1.gz', group='my_func_type')
        ff.save()
        ff.items.add(*items)
        # Note: no need to save

        # Assertions
        self.assertEqual(num_items, len(ff.items.all()))
        self.assertEqual(1, ff.id)
        self.assertEqual('my_func_type', ff.group)
        ff_item_ids = [item.id for item in ff.items.all()]
        self.assertEqual(item_ids, ff_item_ids)

    def test_multiple(self):
        items = []
        num_items = 5
        item_ids = range(1, num_items + 1)

        for i in item_ids:
            dom_name = 'item_%d' % i
            item = Item(dom_name=dom_name)
            item.save()
            items.append(item)

        ff1 = FeedFile(fname='f1.gz', group='my_func_type')
        ff1.save()
        ff1.items.add(*items)

        ff2 = FeedFile(fname='f2.gz', group='another_func_type')
        ff2.save()
        ff2.items.add(*items[:3])

        # Assertions
        self.assertEqual(num_items, len(ff1.items.all()))
        self.assertEqual(1, ff1.id)
        self.assertEqual('my_func_type', ff1.group)

        ff_item_ids = [item.id for item in ff1.items.all()]
        self.assertEqual(item_ids, ff_item_ids)

        self.assertEqual(3, len(ff2.items.all()))
        self.assertEqual(2, ff2.id)
        self.assertEqual('another_func_type', ff2.group)

        ff_item_ids = [item.id for item in ff2.items.all()]
        self.assertEqual(item_ids[:3], ff_item_ids)

    def test_create_one(self):
        # Note: use the create method in preference to the raw methods above
        items = []
        num_items = 5
        num_docs = 27
        item_ids = range(1, num_items + 1)

        for i in range(0, num_items):
            dom_name = 'item_%d' % i
            item = Item(dom_name=dom_name)
            item.save()
            items.append(item)

        ff = FeedFile.create(fname='f1.gz', group='my_func_type', num_docs=num_docs, items=items)  # Note: no need to save separately

        # Assertions
        self.assertEqual(num_items, len(ff.items.all()))
        self.assertEqual(1, ff.id)
        self.assertEqual('my_func_type', ff.group)
        self.assertEqual(num_docs, ff.num_docs)
        ff_item_ids = [item.id for item in ff.items.all()]
        self.assertEqual(item_ids, ff_item_ids)


class MCodeTestCase(TestCase):
    def test_mcode_found(self):
        expected_mcode = u'6HHA'
        mcodes = MCodes(mcode=expected_mcode, psmid=u'cho_book_1920_paris_000_0000', publication_title=u'The Treaty of Peace Between the Allied and Associated Powers and Germany Signed at Versailles, June 28, 1919')
        mcodes.save()

        actual_mcodes = MCodes.objects.filter(psmid=u'cho_book_1920_paris_000_0000')
        self.assertEqual(1, len(actual_mcodes))
        self.assertEqual(expected_mcode, actual_mcodes[0].mcode)

    def test_mcode_not_found(self):
        expected_mcode = u''
        mcodes = MCodes(mcode=expected_mcode, psmid=u'cho_book_1956_0002_002_0000', publication_title=u'Calendar and Texts of Documents on International Affairs, vol. 2: Jan 1955-June 1956 Part 2')
        mcodes.save()

        actual_mcodes = MCodes.objects.filter(psmid=u'cho_book_1956_0002_002_0000')
        self.assertEqual(expected_mcode, actual_mcodes[0].mcode)

    def test_psmid_not_in_database(self):
        actual_mcodes = MCodes.objects.filter(psmid=u'not_in_db')
        self.assertEqual(0, len(actual_mcodes))


class ApprovalTestCase(TestCase):
    def test_approval(self):
        # an item can have approval information related to it

        expected_item_id = 1
        expected_notes = '...some notes...'
        expected_who_id = 1

        psmid = 'cho_bcrc_1933_0001_000_0000'
        item = Item(dom_id=psmid, dom_name=psmid)
        item.save()

        username = 'john'
        user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
        user.save()

        saved_item = Item.objects.get(dom_name__exact=psmid)
        saved_user = User.objects.get(username__exact=username)

        approval = Approval(item_id=saved_item.id, approved=True, notes=expected_notes, who_id=saved_user.id)
        approval.save()

        saved_approval = Approval.objects.get(item_id__exact=saved_item.id)

        self.assertEqual(expected_item_id, saved_approval.item_id)
        self.assertEqual(expected_notes, saved_approval.notes)
        self.assertEqual(expected_who_id, saved_approval.who_id)


class LanguageTestCase(TestCase):
    def test_language_psmid(self):
        expected_lang = 'English'
        language = Language(psmid='1', article_id='1', lang=expected_lang)
        language.save()

        actual_language = Language.objects.get(psmid='1')

        self.assertEqual(actual_language.lang, expected_lang)

    def test_languages_psmid(self):
        expected_langs = ['English', 'French']

        psmid = 'xxx'
        language = Language(psmid=psmid, article_id='1', lang=expected_langs[0])
        language.save()
        language = Language(psmid=psmid, article_id='2', lang=expected_langs[1])
        language.save()

        actual_langs = Language.langs(psmid)  # they come back as unicode

        self.assertListEqual(actual_langs, expected_langs)  # but assert unicode v. non unicode ignored

    def test_language_article_id(self):
        expected_lang = 'Russian'
        language = Language(psmid='1', article_id='1', lang='Bulgarian')
        language.save()
        language = Language(psmid='1', article_id='2', lang=expected_lang)
        language.save()

        actual_language = Language.objects.get(psmid='1', article_id='2')

        self.assertEqual(actual_language.lang, expected_lang)

    def test_psmid_not_in_gaia(self):
        language = Language(psmid='does_not_exist', article_id='1', lang='English')
        language._get_outbox = MagicMock(return_value=Outbox(test.test_dir))  # mock a def inside the Language class

        self.assertEquals(language.article_title(), Language.PSMID_NOT_FOUND_IN_GAIA)

    def test_article_id_not_in_gaia(self):
        # we require an xml asset to "exist"

        with patch('qa.models.DomItem') as mock:  # mock an object inside the Language.article_title def
            mock.xml_asset.return_value = '/james'
            language = Language(psmid='does_not_exist', article_id='1', lang='English')
            language._get_outbox = MagicMock(return_value=Outbox(test.test_dir))

            self.assertEquals(Language.ARTICLE_NOT_FOUND_IN_GAIA, language.article_title())


class RejectReasonTestCase(TestCase):
    def test_reject_reason(self):

        expected_item_id = 1
        expected_reason = '...some notes...'
        expected_who_id = 1

        psmid = 'cho_bcrc_1933_0001_000_0000'
        item = Item(dom_id=psmid, dom_name=psmid)
        item.save()

        username = 'john'
        user = User.objects.create_user(username, 'lennon@thebeatles.com', 'johnpassword')
        user.save()

        saved_item = Item.objects.get(dom_name__exact=psmid)
        saved_user = User.objects.get(username__exact=username)

        reject_reason = RejectReason(item_id=saved_item.id, reason=expected_reason, who_id=saved_user.id)
        reject_reason.save()

        saved_reject_reason = RejectReason.objects.get(item_id__exact=saved_item.id)

        self.assertEqual(expected_item_id, saved_reject_reason.item_id)
        self.assertEqual(expected_reason, saved_reject_reason.reason)
        self.assertEqual(expected_who_id, saved_reject_reason.who_id)

    def test_no_reject_reason_saved(self):
        try:
            RejectReason.objects.get(item_id__exact=123)
        except RejectReason.DoesNotExist:
            pass
        except Exception:
            self.fail()

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(QaProxiesTestCase),
    unittest.TestLoader().loadTestsFromTestCase(ItemTestCase),
    unittest.TestLoader().loadTestsFromTestCase(ItemStatusTestCase),
    unittest.TestLoader().loadTestsFromTestCase(IngestErrorTestCase),
    unittest.TestLoader().loadTestsFromTestCase(FeedFileTestCase),
    unittest.TestLoader().loadTestsFromTestCase(DocumentFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(PageFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(PageFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(ChunkFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(ClipFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(AssetLinkFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(DocumentLinkFinalIdTestCase),
    unittest.TestLoader().loadTestsFromTestCase(MCodeTestCase),
    unittest.TestLoader().loadTestsFromTestCase(ApprovalTestCase),
    unittest.TestLoader().loadTestsFromTestCase(LanguageTestCase),
    unittest.TestLoader().loadTestsFromTestCase(RejectReasonTestCase),
    ])

test.tearDown()

if __name__ == '__main__':
    import testing
    testing.main(suite)
