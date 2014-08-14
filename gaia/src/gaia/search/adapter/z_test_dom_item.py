# Note: a convention for these "TestObjects" is to put them in a z_ file
# (ie this is _not_ a (meme: zero) test!)
from gaia.dom.model.document import Document
from gaia.dom.model.page import Page
from gaia.dom.model.chunk import Chunk

class TestDomItem:
    dom_id = 1234
    dom_name = 'item_1234'

    def document(self):
        return Document(7, '7', {'/doc/title': 'doc7', '/doc/issue': '777'})

    def pages(self):
        return [Page(1, '1', {'/page[1]/title': 'page1', '/page[1]/number': 'p1'}),
                Page(2, '2', {'/page[2]/title': 'page2', '/page[2]/number': 'p2'}),
                Page(3, '3', {'/page[3]/title': 'page3', '/page[3]/number': 'p3'}),
               ]

    def chunks(self):
        #             dom_id, dom_name, info, page_ids, clip_ids=None)
        return [Chunk(1, '1', {'/article[1]/title': 'chunk1', '/article[1]/author': 'Anon1'}, page_ids=[1]),
                Chunk(2, '2', {'/article[2]/title': 'chunk2', '/article[2]/author': 'Anon2'}, page_ids=[1, 2]),
                Chunk(3, '3', {'/article[3]/title': 'chunk3', '/article[3]/author': 'Anon3'}, page_ids=[1, 2, 3]),
                Chunk(4, '4', {'/article[4]/title': 'chunk4', '/article[4]/author': 'Anon4'}, page_ids=[1, 2, 3, 4]),
               ]

    def clips(self): return [] 
    def links(self): return []

    def is_complete(self):
        return True
