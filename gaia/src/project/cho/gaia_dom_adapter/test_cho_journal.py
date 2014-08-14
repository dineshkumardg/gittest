#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_journal.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_journal.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname = os.path.join(os.path.dirname(__file__), '../test_samples/cho_iaxx_1963_0039_000_0000.xml')
>>> asset = Asset(fname)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_iaxx_1963_0039_000_0000


>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'journal',
 '/chapter/citation/journal/author/@role': u'editor',
 '/chapter/citation/journal/author/@type': '_IS_ABSENT_',
 '/chapter/citation/journal/author/aucomposed': u'N. P. McDonald',
 '/chapter/citation/journal/author/first': u'N.',
 '/chapter/citation/journal/author/last': u'McDonald',
 '/chapter/citation/journal/author/middle': u'P.',
 '/chapter/citation/journal/byline': '_IS_ABSENT_',
 '/chapter/citation/journal/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/journal/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/journal/pubDate/composed': u'January 1963',
 '/chapter/citation/journal/pubDate/month': u'January',
 '/chapter/citation/journal/pubDate/pubDateEnd': u'1963-01-31',
 '/chapter/citation/journal/pubDate/pubDateStart': u'1963-01-01',
 '/chapter/citation/journal/pubDate/year': u'1963',
 '/chapter/citation/journal/titleGroup/fullTitle': u'International Affairs',
 '/chapter/citation/journal/totalPages': u'16',
 '/chapter/citation/journal/volumeGroup/volumeNumber': u'39',
 '/chapter/citation/journal/volumeGroup/volumeTitle': u'Vol.39 1963',
 '/chapter/metadataInfo/PSMID': u'cho_iaxx_1963_0039_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1968',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1968-09-25',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1968-08-24',
 '/chapter/metadataInfo/contentDate/contentDay': u'01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1960-1969',
 '/chapter/metadataInfo/contentDate/contentIrregular': u'contentIrregular',
 '/chapter/metadataInfo/contentDate/contentMonth': u'April',
 '/chapter/metadataInfo/contentDate/contentYear': u'1968',
 '/chapter/metadataInfo/isbn': u'1234567890',
 '/chapter/metadataInfo/issn': '_IS_ABSENT_',
 '/chapter/metadataInfo/language': u'EN',
 '/chapter/metadataInfo/productContentType': u'Journals',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Statement',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_iaxx_1963_0039_000_0000',
 '_dom_name': u'cho_iaxx_1963_0039_000_0000'}


>>> # Test PAGES ---------------------------------------------------
>>> pages = dom_adapter.pages()
>>> len(pages)
16

>>> page = pages[0]
>>> page.dom_id
1

>>> page.dom_name
u'I'

>>> page.info == {'_id': 1, '/chapter/page[1]/article/text/textclip/footnote/word': u'WORD', '_dom_name': u'I', '_dom_id': 1, '/chapter/page[1]/sourcePage': u'I', '_asset_fname': u'cho_iaxx_1963_0039_000_0001.jpg', '@id': '0001'}
True

>>> page = pages[8]
>>> page.dom_id
9

>>> page.dom_name
u'5'

>>> page.info == {'/chapter/page[9]/article/text/textclip/footnote/word': '_IS_ABSENT_', '_id': 9, '_dom_name': u'5', '/chapter/page[9]/sourcePage': u'5', '_dom_id': 9, '_asset_fname': u'cho_iaxx_1963_0039_000_0009.jpg', '@id': '00009'}
True



>>> # Test CHUNKS ---------------------------------------------------
>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
8

>>> def print_chunk(chunk):
...     print "CHUNK ID:", chunk.dom_id
...     print "chunk.page_ids: ", chunk.page_ids
...     #print "clip_ids: ", chunk.clip_ids    # TODO
...     print "chunk.info:"
...     info = chunk.info
...     for key in sorted(info.keys()):
...         print " ", key, ":", info[key]
>>> print_chunk(chunks[0])
CHUNK ID: 1
chunk.page_ids:  [1, 2]
chunk.info:
  /chapter/page[1]/article/@id : 1
  /chapter/page[1]/article/@level : 1
  /chapter/page[1]/article/@type : front_matter
  /chapter/page[1]/article/articleInfo/author/@type : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/byline : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/issueNumber : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/issueTitle : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/language : English
  /chapter/page[1]/article/articleInfo/pageCount : 2
  /chapter/page[1]/article/articleInfo/pageRange : 1-2
  /chapter/page[1]/article/articleInfo/title : Front Matter
  _clip_ids : None
  _dom_id : 1
  _dom_name : Front Matter
  _is_binary : False
  _page_ids : [1, 2]


>>> print_chunk(chunks[1])
CHUNK ID: 2
chunk.page_ids:  [1]
chunk.info:
  /chapter/page[1]/article/illustration/@colorimage : color
  /chapter/page[1]/article/illustration/@pgref : 0001
  /chapter/page[1]/article/illustration/@type : chart
  /chapter/page[1]/article/illustration/caption : Illustration Caption Here
  _clip_ids : None
  _dom_id : 2
  _dom_name : Illustration Caption Here
  _is_binary : True
  _page_ids : [1]

>>> print_chunk(chunks[2])
CHUNK ID: 3
chunk.page_ids:  [3, 4]
chunk.info:
  /chapter/page[3]/article/@id : 2
  /chapter/page[3]/article/@level : 1
  /chapter/page[3]/article/@type : article
  /chapter/page[3]/article/articleInfo/author/@type : _IS_ABSENT_
  /chapter/page[3]/article/articleInfo/author/aucomposed : Sarah Neate
  /chapter/page[3]/article/articleInfo/author/first : Sarah
  /chapter/page[3]/article/articleInfo/author/last : Neate
  /chapter/page[3]/article/articleInfo/byline : _IS_ABSENT_
  /chapter/page[3]/article/articleInfo/issueNumber : 1
  /chapter/page[3]/article/articleInfo/issueTitle : No. 1
  /chapter/page[3]/article/articleInfo/language : English
  /chapter/page[3]/article/articleInfo/pageCount : 2
  /chapter/page[3]/article/articleInfo/pageRange : 3-5
  /chapter/page[3]/article/articleInfo/pubDate/composed : January 1963
  /chapter/page[3]/article/articleInfo/pubDate/month : January
  /chapter/page[3]/article/articleInfo/pubDate/pubDateEnd : 1963-12-31
  /chapter/page[3]/article/articleInfo/pubDate/pubDateStart : 1963-01-01
  /chapter/page[3]/article/articleInfo/pubDate/year : 1963
  /chapter/page[3]/article/articleInfo/startingColumn : a
  /chapter/page[3]/article/articleInfo/title : Article Title
  _clip_ids : None
  _dom_id : 3
  _dom_name : Article Title
  _is_binary : False
  _page_ids : [3, 4]

>>> print_chunk(chunks[6])
CHUNK ID: 7
chunk.page_ids:  [3]
chunk.info:
  /chapter/page[5]/article[2]/illustration[1]/@colorimage : color
  /chapter/page[5]/article[2]/illustration[1]/@pgref : 00003
  /chapter/page[5]/article[2]/illustration[1]/@type : chart
  /chapter/page[5]/article[2]/illustration[1]/caption : Illustration Caption Here
  _clip_ids : None
  _dom_id : 7
  _dom_name : Illustration Caption Here
  _is_binary : True
  _page_ids : [3]

>>> print_chunk(chunks[7])
CHUNK ID: 8
chunk.page_ids:  [3]
chunk.info:
  /chapter/page[5]/article[2]/illustration[2]/@colorimage : color
  /chapter/page[5]/article[2]/illustration[2]/@pgref : 0003
  /chapter/page[5]/article[2]/illustration[2]/@type : chart
  /chapter/page[5]/article[2]/illustration[2]/caption : _IS_ABSENT_
  _clip_ids : None
  _dom_id : 8
  _dom_name : chart_8
  _is_binary : True
  _page_ids : [3]

>>> print "ASSET FNAMES:"
ASSET FNAMES:

>>> print dom_adapter.asset_fnames()
[u'cho_iaxx_1963_0039_000_0001.jpg', u'cho_iaxx_1963_0039_000_0002.jpg', u'cho_iaxx_1963_0039_000_0003.jpg', u'cho_iaxx_1963_0039_000_0004.jpg', u'cho_iaxx_1963_0039_000_0005.jpg', u'cho_iaxx_1963_0039_000_0006.jpg', u'cho_iaxx_1963_0039_000_0007.jpg', u'cho_iaxx_1963_0039_000_0008.jpg', u'cho_iaxx_1963_0039_000_0009.jpg', u'cho_iaxx_1963_0039_000_0010.jpg', u'cho_iaxx_1963_0039_000_0011.jpg', u'cho_iaxx_1963_0039_000_0012.jpg', u'cho_iaxx_1963_0039_000_0013.jpg', u'cho_iaxx_1963_0039_000_0014.jpg', u'cho_iaxx_1963_0039_000_0015.jpg', u'cho_iaxx_1963_0039_000_0016.jpg', u'cho_iaxx_1963_0039_000_0000.mp3']

>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link
... # Note: this is a yucky dom_name with a dot, but should be ok?
DocumentLink(dom_id="1", dom_name="Survey pp.5", info="{'/chapter/page[1]/article/text/textclip[1]/relatedDocument/@type': u'article', '/chapter/page[1]/article/text/textclip[1]/relatedDocument/@docref': u'cho_iaxx_1963_0039_000_0005', '/chapter/page[1]/article/text/textclip[1]/relatedDocument/@pgref': u'5'}")
AssetLink(dom_id="2", dom_name="cho_iaxx_1963_0039_000_0000.mp3", info="{'/chapter/metadataInfo/relatedMedia/@dataType': u'mp3', '/chapter/metadataInfo/relatedMedia/@duration': u'12.34', '/chapter/metadataInfo/relatedMedia/@mediaType': u'Audio'}")

>>> # dom_adapter.write(',journal.xml')
>>> # TODO

# cho_book_1963_0000_000_0000 =============================================================================================

>>> fname_book = os.path.join(os.path.dirname(__file__), '../test_samples/cho_book_1963_0000_000_0000.xml')
>>> asset = Asset(fname_book)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_book_1963_0000_000_0000

>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/book/author/@role': u'editor',
 '/chapter/citation/book/author/@type': '_IS_ABSENT_',
 '/chapter/citation/book/author/aucomposed': u'Victor Bulmer-Thomas',
 '/chapter/citation/book/author/first': u'Victor',
 '/chapter/citation/book/author/last': u'Bulmer-Thomas',
 '/chapter/citation/book/byline': '_IS_ABSENT_',
 '/chapter/citation/book/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/book/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/book/imprint/imprintFull': u'Cambridge University Press, Issued under the auspices of the Royal Institute of International Affairs',
 '/chapter/citation/book/imprint/imprintPublisher': u'Cambridge University Press',
 '/chapter/citation/book/pubDate/composed': u'1977',
 '/chapter/citation/book/pubDate/pubDateEnd': u'1977-12-31',
 '/chapter/citation/book/pubDate/pubDateStart': u'1977-01-01',
 '/chapter/citation/book/pubDate/year': u'1977',
 '/chapter/citation/book/publicationPlace/publicationPlaceCity': u'Cambridge',
 '/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'Cambridge, Endgland',
 '/chapter/citation/book/publicationPlace/publicationPlaceCountry': u'England',
 '/chapter/citation/book/seriesGroup/seriesNumber': '_IS_ABSENT_',
 '/chapter/citation/book/seriesGroup/seriesTitle': '_IS_ABSENT_',
 '/chapter/citation/book/titleGroup/fullTitle': u'Britain and Latin America: a changing relationship',
 '/chapter/citation/book/totalPages': u'8',
 '/chapter/metadataInfo/PSMID': u'cho_book_1963_0000_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1963',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1963-12-31',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1963-01-01',
 '/chapter/metadataInfo/contentDate/contentYear': u'1963',
 '/chapter/metadataInfo/isbn': u'0192147331',
 '/chapter/metadataInfo/issn': '_IS_ABSENT_',
 '/chapter/metadataInfo/language': u'English',
 '/chapter/metadataInfo/productContentType': u'Books',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_book_1963_0000_000_0000',
 '_dom_name': u'cho_book_1963_0000_000_0000'}


>>> pages = dom_adapter.pages()
>>> len(pages)
8

>>> print pages[len(pages) - 1]
Page(dom_id="8", dom_name="_IS_ABSENT_", info="{'@id': '8', '_asset_fname': u'cho_book_1963_0000_000_0008.jpg', '/chapter/page[8]/sourcePage': '_IS_ABSENT_', '_id': 8, '/chapter/page[8]/article/text/textclip/footnote/word': '_IS_ABSENT_'}")

>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
2

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="2", dom_name="Britian and Latin America in perspective", clip_ids="None", is_binary="False", page_ids="[5, 6, 7, 8]", info="{'/chapter/page[5]/article/articleInfo/startingColumn': u'A', '/chapter/page[5]/article/@level': u'1', '/chapter/page[5]/article/@type': u'front_matter', '/chapter/page[5]/article/articleInfo/pageCount': u'4', '/chapter/page[5]/article/articleInfo/title': u'Britian and Latin America in perspective', '/chapter/page[5]/article/articleInfo/byline': '_IS_ABSENT_', '/chapter/page[5]/article/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page[5]/article/articleInfo/language': '_IS_ABSENT_', '/chapter/page[5]/article/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page[5]/article/articleInfo/issueTitle': '_IS_ABSENT_', '/chapter/page[5]/article/@id': u'2', '/chapter/page[5]/article/articleInfo/pageRange': u'1-4'}")


>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link

'''
