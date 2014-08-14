#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_meeting.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_meeting.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname_meet = os.path.join(os.path.dirname(__file__), '../test_samples/cho_meet_2010_7771_001_0001.xml')
>>> asset = Asset(fname_meet)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_meet_2010_7771_001_0001

>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'speech',
 '/chapter/citation/meeting/author/@role': u'author',
 '/chapter/citation/meeting/author/@type': '_IS_ABSENT_',
 '/chapter/citation/meeting/author/aucomposed': u'MR LEO LOVELL',
 '/chapter/citation/meeting/author/first': u'Leo',
 '/chapter/citation/meeting/author/last': u'Lovell',
 '/chapter/citation/meeting/author/prefix': u'MR',
 '/chapter/citation/meeting/byline': '_IS_ABSENT_',
 '/chapter/citation/meeting/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/meeting/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/meeting/meetingGroup/meetingLocation': u'Chatham House, London, UK',
 '/chapter/citation/meeting/meetingGroup/meetingNumber': u'RIIA/8/3174',
 '/chapter/citation/meeting/meetingGroup/sponsoringOrganisation': '_IS_ABSENT_',
 '/chapter/citation/meeting/pubDate/century': u'century',
 '/chapter/citation/meeting/pubDate/composed': u'January 1963',
 '/chapter/citation/meeting/pubDate/day': u'6',
 '/chapter/citation/meeting/pubDate/dayofweek': u'Monday',
 '/chapter/citation/meeting/pubDate/irregular': u'irregular',
 '/chapter/citation/meeting/pubDate/month': u'May',
 '/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-31',
 '/chapter/citation/meeting/pubDate/pubDateStart': u'1963-01-01',
 '/chapter/citation/meeting/pubDate/year': u'1837',
 '/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 1',
 '/chapter/citation/meeting/totalPages': u'1',
 '/chapter/metadataInfo/PSMID': u'cho_meet_2010_7771_001_0001',
 '/chapter/metadataInfo/chathamHouseRule': u'Yes',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1968',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'2002-09-25',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'2002-08-24',
 '/chapter/metadataInfo/contentDate/contentDay': u'01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'2000-2010',
 '/chapter/metadataInfo/contentDate/contentIrregular': u'contentIrregular',
 '/chapter/metadataInfo/contentDate/contentMonth': u'April',
 '/chapter/metadataInfo/contentDate/contentYear': u'1968',
 '/chapter/metadataInfo/isbn': u'1234567890',
 '/chapter/metadataInfo/issn': u'12345678',
 '/chapter/metadataInfo/language': u'English',
 '/chapter/metadataInfo/productContentType': u'Meetings',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Statement',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_meet_2010_7771_001_0001',
 '_dom_name': u'cho_meet_2010_7771_001_0001'}


>>> pages = dom_adapter.pages()
>>> len(pages)
1

>>> print pages[len(pages) - 1]
Page(dom_id="1", dom_name="1", info="{'/chapter/page/article/text/textclip/footnote/word': '_IS_ABSENT_', '_asset_fname': u'cho_meet_2010_7771_001_0001.jpg', '/chapter/page/sourcePage': u'1', '@id': '1', '_id': 1}")

>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
1

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="1", dom_name="1", clip_ids="None", is_binary="False", page_ids="[1]", info="{'/chapter/page/article/articleInfo/language': u'English', '/chapter/page/article/@level': u'1', '/chapter/page/article/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page/article/articleInfo/issueTitle': '_IS_ABSENT_', '/chapter/page/article/@id': u'1', '/chapter/page/article/@type': u'article', '/chapter/page/article/articleInfo/byline': '_IS_ABSENT_', '/chapter/page/article/articleInfo/pageCount': u'1', '/chapter/page/article/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page/article/articleInfo/title': '_IS_ABSENT_'}")

>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link
AssetLink(dom_id="1", dom_name="cho_meet_2010_7771_001_0001.mp3", info="{'/chapter/metadataInfo/relatedMedia/@dataType': u'mp3', '/chapter/metadataInfo/relatedMedia/@duration': u'12.34', '/chapter/metadataInfo/relatedMedia/@mediaType': u'Audio'}")


'''
