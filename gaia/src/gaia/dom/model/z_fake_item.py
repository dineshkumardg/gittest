# Note: a convention for these "TestObjects" is to put them in a z_ file
# (ie this is _not_ a (meme: zero) test!)
import os
from gaia.dom.model.document import Document
from gaia.dom.model.page import Page
from gaia.dom.model.chunk import Chunk
from gaia.asset.asset import Asset
from gaia.dom.model.link import DocumentLink, AssetLink
from gaia.dom.model.clip import Clip


class FakeItem:
    def __init__(self, fpath, dom_id):
        self.dom_id = dom_id
        self.dom_name = dom_id

        fnames = ['%s.xml' % self.dom_id, '%s.jpg' % self.dom_id]
        xml_asset = Asset(os.path.join(fpath, fnames[0]), 'wb')
        self.assets = []
        self.assets.append(xml_asset)

    def document(self):
        return Document(self.dom_id, self.dom_name, {'/doc/title': 'doc1', '/doc/issue': '111'})

    def pages(self):
        return [Page(1, '1', {'/page[1]/title': 'page1', '/page[1]/number': 'p1'}),
                Page(2, '2', {'/page[2]/title': 'page2', '/page[2]/number': 'p2'}),
                Page(3, '3', {'/page[3]/title': 'page3', '/page[3]/number': 'p3'}),
                Page(4, '4', {'/page[4]/title': 'page4', '/page[4]/number': 'p4'}),
               ]

    def chunks(self):
        # dom_id, dom_name, info, page_ids, clip_ids=None)
        return [Chunk(1, '1', {'/article[1]/title': 'chunk1', '/article[1]/author': 'Anon1'}, page_ids=[1]),
                Chunk(2, '2', {'/article[2]/title': 'chunk2', '/article[2]/author': 'Anon2'}, page_ids=[1, 2]),
                Chunk(3, '3', {'/article[3]/title': 'chunk3', '/article[3]/author': 'Anon3'}, page_ids=[1, 2, 3]),
                Chunk(4, '4', {'/article[4]/title': 'chunk4', '/article[4]/author': 'Anon4'}, page_ids=[1, 2, 3, 4]),
               ]

    def binary_assets(self):
        return self.assets
    
    def clips(self):
        return [Clip(1, '1', 1, {'clip_k1': 'clip_v2', 'clip_k2': 'clip_v2'}),
               ]

    def asset_links(self):
        info = {'link_k1': 'link_v2', 'link_k2': 'link_v2'}
        asset_fname = 'hello_world.mp3'
        return [AssetLink(1, '1', info, asset_fname), ]

    def document_links(self):
        info = {'link_k1': 'link_v2', 'link_k2': 'link_v2'}
        source={'chunk':None, 'page':'1'}
        target={'document': '1', 'chunk': '4', 'page': '4'}
        return [DocumentLink(1, '1', info, source, target), ]

    def is_complete(self):
        return True
