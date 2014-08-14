#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_refugee_survey.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_refugee_survey.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname_rfpx = os.path.join(os.path.dirname(__file__), '../test_samples/cho_rsxx_1945_TEST_000_0000.xml')
>>> asset = Asset(fname_rfpx)
>>> dom_adapter_rfpx = Cho(asset)
>>> print(dom_adapter_rfpx.document().dom_id)
cho_rsxx_1945_TEST_000_0000

>>> pages = dom_adapter_rfpx.pages()
>>> len(pages)
10

>>> print pages[len(pages) - 1]
Page(dom_id="10", dom_name="II", info="{'/chapter/page[10]/article/text/textclip/footnote/word': '_IS_ABSENT_', '_asset_fname': u'cho_rsxx_1945_TEST_000_0010.jpg', '@id': '10', '/chapter/page[10]/sourcePage': u'II', '_id': 10}")

>>> chunks = dom_adapter_rfpx.chunks()
>>> print len(chunks)
14

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="14", dom_name="(a) I. British Co-Ordinating Committee for International Studies", clip_ids="None", is_binary="False", page_ids="[10]", info="{'/chapter/page[10]/article[2]/articleInfo/issueNumber': '_IS_ABSENT_', '/chapter/page[10]/article[2]/@type': u'article', '/chapter/page[10]/article[2]/articleInfo/author/@type': '_IS_ABSENT_', '/chapter/page[10]/article[2]/articleInfo/issueTitle': '_IS_ABSENT_', '/chapter/page[10]/article[2]/@level': u'2', '/chapter/page[10]/article[2]/articleInfo/title': u'(a) I. British Co-Ordinating Committee for International Studies', '/chapter/page[10]/article[2]/@id': u'11', '/chapter/page[10]/article[2]/articleInfo/startingColumn': u'A', '/chapter/page[10]/article[2]/articleInfo/pageCount': u'1', '/chapter/page[10]/article[2]/articleInfo/byline': '_IS_ABSENT_', '/chapter/page[10]/article[2]/articleInfo/language': u'English'}")

>>> print(dom_adapter_rfpx.clips())
[]

>>> for link in dom_adapter_rfpx.links():
...     print link

>>> pprint(dom_adapter_rfpx.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/book/author/@type': '_IS_ABSENT_',
 '/chapter/citation/book/author[1]/@role': u'editor',
 '/chapter/citation/book/author[1]/aucomposed': u'Mr Stephen A. Heald',
 '/chapter/citation/book/author[1]/first': u'Stephen',
 '/chapter/citation/book/author[1]/last': u'Heald',
 '/chapter/citation/book/author[1]/middle': u'A.',
 '/chapter/citation/book/author[1]/prefix': u'Mr',
 '/chapter/citation/book/author[1]/suffix': u'PHD',
 '/chapter/citation/book/author[2]/@role': u'editor',
 '/chapter/citation/book/author[2]/aucomposed': u'Mr Smith',
 '/chapter/citation/book/author[2]/last': u'Smith',
 '/chapter/citation/book/author[2]/prefix': u'Mr',
 '/chapter/citation/book/author[3]/@role': u'author',
 '/chapter/citation/book/author[3]/aucomposed': u'Mr Williams',
 '/chapter/citation/book/author[3]/last': u'Williams',
 '/chapter/citation/book/author[3]/prefix': u'Mr',
 '/chapter/citation/book/author[4]/@role': u'author',
 '/chapter/citation/book/author[4]/aucomposed': u'Mr Scott Lee Hogan PM',
 '/chapter/citation/book/author[4]/first': u'Scott',
 '/chapter/citation/book/author[4]/last': u'Hogan',
 '/chapter/citation/book/author[4]/middle': u'Lee',
 '/chapter/citation/book/author[4]/prefix': u'Mr',
 '/chapter/citation/book/author[4]/suffix': u'PM',
 '/chapter/citation/book/author[5]/@role': u'author',
 '/chapter/citation/book/author[5]/aucomposed': u'sobriquet',
 '/chapter/citation/book/author[5]/sobriquet': u'sobriquet',
 '/chapter/citation/book/byline': u'The Organisation',
 '/chapter/citation/book/editionNumber': '_IS_ABSENT_',
 '/chapter/citation/book/editionStatement': '_IS_ABSENT_',
 '/chapter/citation/book/imprint/imprintFull': u'The Royal Institute of International Affairs and the Information Service on International Affairs',
 '/chapter/citation/book/imprint/imprintPublisher': u'The Royal Institute of International Affairs and the Information Service on International Affairs',
 '/chapter/citation/book/pubDate/composed': u'01 08 1929',
 '/chapter/citation/book/pubDate/day': u'01',
 '/chapter/citation/book/pubDate/dayofweek': u'Thursday',
 '/chapter/citation/book/pubDate/month': u'08',
 '/chapter/citation/book/pubDate/pubDateEnd': u'1929-08-01',
 '/chapter/citation/book/pubDate/pubDateStart': u'1929-08-01',
 '/chapter/citation/book/pubDate/year': u'1929',
 '/chapter/citation/book/publicationPlace/publicationPlaceCity': u'London',
 '/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'London, UK',
 '/chapter/citation/book/publicationPlace/publicationPlaceCountry': u'UK',
 '/chapter/citation/book/seriesGroup/seriesNumber': u'1',
 '/chapter/citation/book/seriesGroup/seriesTitle': u'Looking Forward',
 '/chapter/citation/book/titleGroup/fullSubtitle': u'Subtitle',
 '/chapter/citation/book/titleGroup/fullTitle': u'A Directory of Societies and Organizations in Great Britain Concerned with the Study of International Affairs',
 '/chapter/citation/book/totalPages': u'10',
 '/chapter/citation/book/volumeGroup/volumeNumber': u'1',
 '/chapter/citation/book/volumeGroup/volumeTitle': u'Volume 1',
 '/chapter/metadataInfo/PSMID': u'cho_rsxx_1945_TEST_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1929',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1929-08-01',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1929-08-01',
 '/chapter/metadataInfo/contentDate/contentDay': u'01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1920-1929',
 '/chapter/metadataInfo/contentDate/contentMonth': u'08',
 '/chapter/metadataInfo/contentDate/contentYear': u'1929',
 '/chapter/metadataInfo/isbn': u'123-456-789-1011',
 '/chapter/metadataInfo/issn': u'12345678',
 '/chapter/metadataInfo/language[1]': u'French',
 '/chapter/metadataInfo/language[2]': u'English',
 '/chapter/metadataInfo/productContentType': u'Special Publications',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, England',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_rsxx_1945_TEST_000_0000',
 '_dom_name': u'cho_rsxx_1945_TEST_000_0000'}

'''
