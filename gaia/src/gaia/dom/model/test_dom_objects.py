# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest

suite = doctest.DocFileSuite('test_dom_objects.py')

if __name__ == '__main__':
    doctest.testfile("test_dom_objects.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from collections import OrderedDict
>>> from gaia.dom.model.document import Document
>>> from gaia.dom.model.page import Page
>>> from gaia.dom.model.chunk import Chunk
>>> from gaia.dom.model.clip import Clip
>>> from gaia.dom.model.link import AssetLink, DocumentLink
>>> 
>>> info = OrderedDict({'title': 'The News', 'author': 'AnonyMouse'})
>>> 
>>> # test Document --------------------------------------------------------------
>>> x = Document('1', 'a_dom_name', info)
>>> str(x)
'Document(dom_id="1", dom_name="a_dom_name", info="OrderedDict([(\'author\', \'AnonyMouse\'), (\'title\', \'The News\')])")'

>>> x.info
OrderedDict([('author', 'AnonyMouse'), ('title', 'The News'), ('_dom_id', '1'), ('_dom_name', 'a_dom_name')])

>>> # test Page --------------------------------------------------------------
>>> x = Page('1', 'a_dom_name', info)
>>> str(x)
'Page(dom_id="1", dom_name="a_dom_name", info="OrderedDict([(\'author\', \'AnonyMouse\'), (\'title\', \'The News\')])")'

>>> x.info
OrderedDict([('author', 'AnonyMouse'), ('title', 'The News'), ('_dom_id', '1'), ('_dom_name', 'a_dom_name')])

>>> # test Chunk --------------------------------------------------------------
>>> x = Chunk('1', 'a_dom_name', info, page_ids=[1, 2], is_binary=True)
>>> str(x)
'Chunk(dom_id="1", dom_name="a_dom_name", clip_ids="None", is_binary="True", page_ids="[1, 2]", info="OrderedDict([(\'author\', \'AnonyMouse\'), (\'title\', \'The News\')])")'

>>> x.info
OrderedDict([('author', 'AnonyMouse'), ('title', 'The News'), ('_dom_id', '1'), ('_dom_name', 'a_dom_name'), ('_clip_ids', None), ('_page_ids', [1, 2]), ('_is_binary', True)])

>>> x = Chunk('1', 'a_dom_name', info, page_ids=[1, 2], clip_ids=[3, 4])
>>> str(x)
'Chunk(dom_id="1", dom_name="a_dom_name", clip_ids="[3, 4]", is_binary="False", page_ids="[1, 2]", info="OrderedDict([(\'author\', \'AnonyMouse\'), (\'title\', \'The News\')])")'

>>> # test Clip --------------------------------------------------------------
>>> x = Clip('1', 'a_dom_name', 'page_id_1', info)
>>> str(x)
'Clip(dom_id="1", dom_name="a_dom_name", page_id="page_id_1", info="OrderedDict([(\'author\', \'AnonyMouse\'), (\'title\', \'The News\')])")'

>>> x.info
OrderedDict([('author', 'AnonyMouse'), ('title', 'The News'), ('_dom_id', '1'), ('_dom_name', 'a_dom_name'), ('_page_id', 'page_id_1')])

>>> # test Links --------------------------------------------------------------
>>> # ... a link to an Asset ...
>>> info = OrderedDict({'/chapter/metadataInfo/relatedMedia/@duration': u'12.34', '/chapter/metadataInfo/relatedMedia/@mediaType': u'Audio', '_asset_fname': u'cho_iaxx_1963_0039_000_0000.mp3', '/chapter/metadataInfo/relatedMedia/@dataType': u'mp3'})
>>> asset_fname = 'cho_iaxx_1963_0039_000_0000.mp3'
>>> x = AssetLink('1', 'a_dom_name', info, asset_fname)
>>> str(x)
'AssetLink(dom_id="1", dom_name="a_dom_name", info="OrderedDict([(\'/chapter/metadataInfo/relatedMedia/@duration\', u\'12.34\'), (\'/chapter/metadataInfo/relatedMedia/@mediaType\', u\'Audio\'), (\'/chapter/metadataInfo/relatedMedia/@dataType\', u\'mp3\'), (\'_asset_fname\', u\'cho_iaxx_1963_0039_000_0000.mp3\')])")'

>>> x.asset_fname
'cho_iaxx_1963_0039_000_0000.mp3'

>>> # ... a link to another document --------------------------------------------------------------
>>> # Note that the target (refs) may NOT exist
>>> info = {}
>>> source = {'page': 'my_page_id', 'chunk': 'my_chunk_id'}
>>> target = {'document': 'another_document_dom_id', 'page': 'another_page_id', 'chunk': 'another_chunk_id'}
>>> x = DocumentLink('1', 'my_dom_name', info, source, target)
>>> str(x)
'DocumentLink(dom_id="1", dom_name="my_dom_name", info="{}")'
>>> x.source
{'chunk': 'my_chunk_id', 'page': 'my_page_id'}
>>> x.target
{'chunk': 'another_chunk_id', 'document': 'another_document_dom_id', 'page': 'another_page_id'}

>>> # check that optional target fields are optional.
>>> source={} # WARNING: source fields ARE typically required (but not enforced!)
>>> for target in [\
...     {'document': None, 'page': 'a_page_id', 'chunk': 'a_chunk_id'},
...     {'document': 'a_document_dom_id', 'page': None, 'chunk': 'a_chunk_id'},
...     {'document': 'a_document_dom_id', 'page': 'a_page_id', 'chunk': None},
...     {'document': None, 'page': None, 'chunk': 'a_chunk_id'},
...     {'document': None, 'page': 'a_page_id', 'chunk': None},
...     {'document': 'a_document_dom_id', 'page': 'a_page_id', 'chunk': None}]:
...     x = DocumentLink('1', 'my_dom_name', info, source, target)
...     x.target
{'chunk': 'a_chunk_id', 'document': None, 'page': 'a_page_id'}
{'chunk': 'a_chunk_id', 'document': 'a_document_dom_id', 'page': None}
{'chunk': None, 'document': 'a_document_dom_id', 'page': 'a_page_id'}
{'chunk': 'a_chunk_id', 'document': None, 'page': None}
{'chunk': None, 'document': None, 'page': 'a_page_id'}
{'chunk': None, 'document': 'a_document_dom_id', 'page': 'a_page_id'}

>>> # WARNING! All None's is not sensible, but, currently, *IS* allowed!
>>> # (PLEASE DO NOT USE THIS THIS WAY!!)
>>> target = {'document': None, 'page': None, 'chunk': None}
>>> x = DocumentLink('1', 'my_dom_name', info, source, target)
>>> x.target
{'chunk': None, 'document': None, 'page': None}


>>> # test UNICODE chars --------------------------------------------------------------
>>> info = OrderedDict({'title': u'The IN\u1234ternational News', u'aut\u1234': 'AnonyMouse'})
>>> x = Document('1', u'a_\u1234dom_name', info)
>>> str(x)
'Document(dom_id="1", dom_name="a_?dom_name", info="OrderedDict([(u\'aut\\u1234\', \'AnonyMouse\'), (\'title\', u\'The IN\\u1234ternational News\')])")'

>>> x.info
OrderedDict([(u'aut\u1234', 'AnonyMouse'), ('title', u'The IN\u1234ternational News'), ('_dom_id', '1'), ('_dom_name', u'a_\u1234dom_name')])

'''
