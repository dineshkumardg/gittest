#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_conference_series.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_conference_series.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname = os.path.join(os.path.dirname(__file__), '../test_samples/cho_iprx_1933_0001_001_0000.xml')
>>> asset = Asset(fname)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_iprx_1933_0001_001_0000


>>> print(dom_adapter.document().dom_id)
cho_iprx_1933_0001_001_0000

>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/conference/author/@type': '_IS_ABSENT_',
 '/chapter/citation/conference/author[1]/@role': u'author',
 '/chapter/citation/conference/author[1]/aucomposed': u'Mr Smith',
 '/chapter/citation/conference/author[1]/prefix': u'Mr',
 '/chapter/citation/conference/author[1]/suffix': u'Smith',
 '/chapter/citation/conference/author[2]/@role': u'editor',
 '/chapter/citation/conference/author[2]/aucomposed': u'Mr James J Sears SE',
 '/chapter/citation/conference/author[2]/first': u'James',
 '/chapter/citation/conference/author[2]/last': u'Sears',
 '/chapter/citation/conference/author[2]/middle': u'J',
 '/chapter/citation/conference/author[2]/prefix': u'Mr',
 '/chapter/citation/conference/author[2]/suffix': u'SE',
 '/chapter/citation/conference/byline': '_IS_ABSENT_',
 '/chapter/citation/conference/conferenceGroup/conferenceLocation': u'Canada',
 '/chapter/citation/conference/conferenceGroup/conferenceName': u'Institute of Pacific Relations, 5th Conference',
 '/chapter/citation/conference/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/conference/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/conference/pubDate/composed': u'Wednesday 1st August 1933',
 '/chapter/citation/conference/pubDate/day': u'01',
 '/chapter/citation/conference/pubDate/dayofweek': u'Wednesday',
 '/chapter/citation/conference/pubDate/month': u'08',
 '/chapter/citation/conference/pubDate/pubDateEnd': u'1933-08-01',
 '/chapter/citation/conference/pubDate/pubDateStart': u'1933-08-01',
 '/chapter/citation/conference/pubDate/year': u'1933',
 '/chapter/citation/conference/titleGroup/fullSubtitle': u'Pacific Relations',
 '/chapter/citation/conference/titleGroup/fullTitle': u'Institute of Pacific Relations',
 '/chapter/citation/conference/totalPages': u'8',
 '/chapter/citation/conference/volumeGroup/volumeNumber': u'1',
 '/chapter/citation/conference/volumeGroup/volumeTitle': u'Central Secretariat Papers',
 '/chapter/metadataInfo/PSMID': u'cho_iprx_1933_0001_001_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'August 1933',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1933-08-01',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1933-08-01',
 '/chapter/metadataInfo/contentDate/contentDay': u'01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1930-1939',
 '/chapter/metadataInfo/contentDate/contentMonth': u'08',
 '/chapter/metadataInfo/contentDate/contentYear': u'1933',
 '/chapter/metadataInfo/isbn': u'1234567891012',
 '/chapter/metadataInfo/issn': u'12345678',
 '/chapter/metadataInfo/language[1]': u'English',
 '/chapter/metadataInfo/language[2]': u'French',
 '/chapter/metadataInfo/productContentType': u'Conference Series',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_iprx_1933_0001_001_0000',
 '_dom_name': u'cho_iprx_1933_0001_001_0000'}


>>> # Test PAGES ---------------------------------------------------
>>> pages = dom_adapter.pages()
>>> len(pages)
8

>>> page = pages[0]
>>> page.dom_id
1

>>> page.dom_name
u'[1]'

>>> page.info
{'_id': 1, '/chapter/page[1]/article/text/textclip/footnote/word': '_IS_ABSENT_', '_dom_name': u'[1]', '_dom_id': 1, '/chapter/page[1]/sourcePage': u'[1]', '_asset_fname': u'cho_iprx_1933_0001_001_0001.jpg', '@id': '1'}

>>> page = pages[7]
>>> page.dom_id
8

>>> page.dom_name
u'[1]'

>>> page.info
{'_id': 8, '_dom_name': u'[1]', '/chapter/page[8]/sourcePage': u'[1]', '_dom_id': 8, '_asset_fname': u'cho_iprx_1933_0001_001_0008.jpg', '@id': '8', '/chapter/page[8]/article/text/textclip/footnote/word': '_IS_ABSENT_'}



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
  /chapter/page[1]/article/articleInfo/author/aucomposed : Admiral Chatfield
  /chapter/page[1]/article/articleInfo/author/last : Chatfield
  /chapter/page[1]/article/articleInfo/author/prefix : Admiral
  /chapter/page[1]/article/articleInfo/byline : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/issueNumber : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/issueTitle : _IS_ABSENT_
  /chapter/page[1]/article/articleInfo/language[1] : English
  /chapter/page[1]/article/articleInfo/language[2] : French
  /chapter/page[1]/article/articleInfo/pageCount : 2
  /chapter/page[1]/article/articleInfo/startingColumn : A
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
  /chapter/page[1]/article/illustration[1]/@colorimage : color
  /chapter/page[1]/article/illustration[1]/@pgref : 1
  /chapter/page[1]/article/illustration[1]/@type : line_drawing
  /chapter/page[1]/article/illustration[1]/caption : HELP!
  _clip_ids : None
  _dom_id : 2
  _dom_name : HELP!
  _is_binary : True
  _page_ids : [1]

>>> print_chunk(chunks[2])
CHUNK ID: 3
chunk.page_ids:  [1]
chunk.info:
  /chapter/page[1]/article/illustration[2]/@colorimage : color
  /chapter/page[1]/article/illustration[2]/@pgref : 1
  /chapter/page[1]/article/illustration[2]/@type : line_drawing
  /chapter/page[1]/article/illustration[2]/caption : _IS_ABSENT_
  _clip_ids : None
  _dom_id : 3
  _dom_name : line_drawing_3
  _is_binary : True
  _page_ids : [1]

>>> print_chunk(chunks[5])
CHUNK ID: 6
chunk.page_ids:  [6, 7]
chunk.info:
  /chapter/page[6]/article/@id : 3
  /chapter/page[6]/article/@level : 2
  /chapter/page[6]/article/@type : article
  /chapter/page[6]/article/articleInfo/author/@type : _IS_ABSENT_
  /chapter/page[6]/article/articleInfo/byline : The Organisation
  /chapter/page[6]/article/articleInfo/issueNumber : _IS_ABSENT_
  /chapter/page[6]/article/articleInfo/issueTitle : _IS_ABSENT_
  /chapter/page[6]/article/articleInfo/language : English
  /chapter/page[6]/article/articleInfo/pageCount : 2
  /chapter/page[6]/article/articleInfo/pubDate/composed : August 14-28, 1933
  /chapter/page[6]/article/articleInfo/pubDate/irregular : August 14-28, 1933
  /chapter/page[6]/article/articleInfo/pubDate/pubDateEnd : 1933-08-28
  /chapter/page[6]/article/articleInfo/pubDate/pubDateStart : 1933-08-14
  /chapter/page[6]/article/articleInfo/startingColumn : A
  /chapter/page[6]/article/articleInfo/title : A First Speech.
  _clip_ids : None
  _dom_id : 6
  _dom_name : A First Speech.
  _is_binary : False
  _page_ids : [6, 7]

>>> print dom_adapter.asset_fnames()
[u'cho_iprx_1933_0001_001_0001.jpg', u'cho_iprx_1933_0001_001_0002.jpg', u'cho_iprx_1933_0001_001_0003.jpg', u'cho_iprx_1933_0001_001_0004.jpg', u'cho_iprx_1933_0001_001_0005.jpg', u'cho_iprx_1933_0001_001_0006.jpg', u'cho_iprx_1933_0001_001_0007.jpg', u'cho_iprx_1933_0001_001_0008.jpg']

>>> print(dom_adapter.clips())
[]

>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link


# bcrc ================================================================================================

>>> fname_bcrc = os.path.join(os.path.dirname(__file__), '../test_samples/cho_bcrc_1933_0001_000_0000.xml')
>>> asset = Asset(fname_bcrc)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_bcrc_1933_0001_000_0000

>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/conference/author/@role': '_IS_ABSENT_',
 '/chapter/citation/conference/author/@type': '_IS_ABSENT_',
 '/chapter/citation/conference/byline': '_IS_ABSENT_',
 '/chapter/citation/conference/conferenceGroup/conferenceLocation': u'Toronto, Canada',
 '/chapter/citation/conference/conferenceGroup/conferenceName': u'British Commonwealth Relations. 1st Conference, Toronto, 1933. Vol. 1. Verbatim reports',
 '/chapter/citation/conference/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/conference/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/conference/pubDate/composed': u'1933',
 '/chapter/citation/conference/pubDate/pubDateEnd': u'1933-12-31',
 '/chapter/citation/conference/pubDate/pubDateStart': u'1933-01-01',
 '/chapter/citation/conference/pubDate/year': u'1933',
 '/chapter/citation/conference/titleGroup/fullTitle': u'British Commonwealth Realtions Conference, Toronto',
 '/chapter/citation/conference/totalPages': u'3',
 '/chapter/citation/conference/volumeGroup/volumeNumber': u'1',
 '/chapter/metadataInfo/PSMID': u'cho_bcrc_1933_0001_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1933',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1933-12-31',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1933-01-01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1930-1939',
 '/chapter/metadataInfo/contentDate/contentYear': u'1933',
 '/chapter/metadataInfo/isbn': '_IS_ABSENT_',
 '/chapter/metadataInfo/issn': '_IS_ABSENT_',
 '/chapter/metadataInfo/language': u'English',
 '/chapter/metadataInfo/productContentType': u'Conference Series',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Statement',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_bcrc_1933_0001_000_0000',
 '_dom_name': u'cho_bcrc_1933_0001_000_0000'}

>>> pages = dom_adapter.pages()
>>> len(pages)
3

>>> print pages[len(pages) - 1]
Page(dom_id="3", dom_name="2B", info="{'/chapter/page[3]/article/text/textclip/footnote/word': '_IS_ABSENT_', '/chapter/page[3]/sourcePage': u'2B', '_asset_fname': u'cho_bcrc_1933_0001_000_0003.jpg', '@id': '3', '_id': 3}")

>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
2

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="2", dom_name="Opening Session", clip_ids="None", is_binary="False", page_ids="[3]", info="{'/chapter/page[3]/article/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page[3]/article/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page[3]/article/@type': u'article', '/chapter/page[3]/article/articleInfo/issueTitle': '_IS_ABSENT_', '/chapter/page[3]/article/@id': u'2', '/chapter/page[3]/article/articleInfo/language': u'English', '/chapter/page[3]/article/articleInfo/author/suffix': u'G.C.M.G., K.C', '/chapter/page[3]/article/articleInfo/pageCount': u'2', '/chapter/page[3]/article/articleInfo/pageRange': u'2B', '/chapter/page[3]/article/articleInfo/author/first': u'Robert', '/chapter/page[3]/article/articleInfo/author/aucomposed': u'Sir Robert Borden, G.C.M.G.,K.C', '/chapter/page[3]/article/articleInfo/byline': '_IS_ABSENT_', '/chapter/page[3]/article/articleInfo/author/last': u'Borden', '/chapter/page[3]/article/@level': u'1', '/chapter/page[3]/article/articleInfo/author/prefix': u'Sir', '/chapter/page[3]/article/articleInfo/title': u'Opening Session'}")

>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link


'''
