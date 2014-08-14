from testing.gaia_django_test import GaiaDjangoTest
_test = GaiaDjangoTest()
_test.setUp()

import unittest
from gaia.search.adapter.chunk_search_adapter import ChunkSearchAdapter
from gaia.search.adapter.z_test_dom_item import TestDomItem

from django.test import TestCase
from gaia.dom.index.models import Item, Document, Chunk, Page


class TestChunkSearchAdapter(TestCase):
    def _create_index(self, item):
        item_index = Item(item.dom_id, item.dom_name)
        item_index.save()
        document = Document(item.dom_id, item.dom_name, item=item_index)
        document.save()

        for dom_page in item.pages():
            page = Page(dom_page.dom_id, dom_page.dom_name, document=document)
            page.save()

        for dom_chunk in item.chunks():
            chunk = Chunk(dom_chunk.dom_id, dom_chunk.dom_name, document=document)
            chunk.save()

            #IMPORTANT: TODO.....
            chunk.pages.add(page) # TODO: move this into a Chunk method? create(..., page_ids) TUSH HERE **** TODO
            #IMPORTANT: TODO.....

        return item_index

    def test(self):
        item = TestDomItem()
        item_index = self._create_index(item)

        expected = [("1234|1|1", {'doc_title': 'doc7', 'author': 'Anon1', 'title': 'chunk1', 'doc_issue': '777'}),
                ("1234|1|2", {'doc_title': 'doc7', 'author': 'Anon2', 'title': 'chunk2', 'doc_issue': '777'}),
                ("1234|1|3", {'doc_title': 'doc7', 'author': 'Anon3', 'title': 'chunk3', 'doc_issue': '777'}),
                ("1234|1|4", {'doc_title': 'doc7', 'author': 'Anon4', 'title': 'chunk4', 'doc_issue': '777'})]

        x = ChunkSearchAdapter(item, item_index)
        matches = x.get_search_objects()

        self.assertEqual(len(expected), len(matches))

        for expected_id, expected_info in expected:
            for match in matches:
                if match.search_id == expected_id:
                    self.assertDictEqual(expected_info, match.search_info)
                    continue
       
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestChunkSearchAdapter),
    ])

_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
