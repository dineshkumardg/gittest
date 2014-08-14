#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_report.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_report.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML


>>> fname_rpax= os.path.join(os.path.dirname(__file__), '../test_samples/cho_rpax_1943_notes_000_0000.xml')
>>> asset = Asset(fname_rpax)
>>> dom_adapter = Cho(asset)
>>> print(dom_adapter.document().dom_id)
cho_rpax_1943_notes_000_0000

>>> pprint(dom_adapter.document().info)
{'/chapter/@contentType': u'book',
 '/chapter/citation/book/author/@type': '_IS_ABSENT_',
 '/chapter/citation/book/author[1]/@role': u'author',
 '/chapter/citation/book/author[1]/aucomposed': u'Mr Frank M. Smith, PHD',
 '/chapter/citation/book/author[1]/first': u'Frank',
 '/chapter/citation/book/author[1]/last': u'Smith',
 '/chapter/citation/book/author[1]/middle': u'M.',
 '/chapter/citation/book/author[1]/prefix': u'Mr',
 '/chapter/citation/book/author[1]/suffix': u'PHD',
 '/chapter/citation/book/author[2]/@role': u'author',
 '/chapter/citation/book/author[2]/aucomposed': u'Mr Jones',
 '/chapter/citation/book/author[2]/last': u'Jones',
 '/chapter/citation/book/author[2]/prefix': u'Mr',
 '/chapter/citation/book/author[3]/@role': u'author',
 '/chapter/citation/book/author[3]/aucomposed': u'Researcher',
 '/chapter/citation/book/author[3]/sobriquet': u'Researcher',
 '/chapter/citation/book/author[4]/@role': u'editor',
 '/chapter/citation/book/author[4]/aucomposed': u'Mrs Sandra M. Smith PHD',
 '/chapter/citation/book/author[4]/first': u'Sandra',
 '/chapter/citation/book/author[4]/last': u'Smith',
 '/chapter/citation/book/author[4]/middle': u'M.',
 '/chapter/citation/book/author[4]/prefix': u'Mrs',
 '/chapter/citation/book/byline': u'The Organisation',
 '/chapter/citation/book/editionNumber': u'2',
 '/chapter/citation/book/editionStatement': u'Reprint',
 '/chapter/citation/book/imprint/imprintFull': u'The Broadwater Press',
 '/chapter/citation/book/imprint/imprintManufacturer': u'Printing Press',
 '/chapter/citation/book/imprint/imprintPublisher': u'The Broadwater Press',
 '/chapter/citation/book/pubDate/composed': u'November 1943',
 '/chapter/citation/book/pubDate/month': u'11',
 '/chapter/citation/book/pubDate/pubDateEnd': u'1943-11-30',
 '/chapter/citation/book/pubDate/pubDateStart': u'1943-11-01',
 '/chapter/citation/book/pubDate/year': u'1943',
 '/chapter/citation/book/publicationPlace/publicationPlaceCity': u'Welwyn',
 '/chapter/citation/book/publicationPlace/publicationPlaceComposed': u'Welwyn, Hertfordshire',
 '/chapter/citation/book/publicationPlace/publicationPlaceState': u'Hertfordshire',
 '/chapter/citation/book/seriesGroup/seriesNumber': u'1',
 '/chapter/citation/book/seriesGroup/seriesTitle': u'Information Notes',
 '/chapter/citation/book/titleGroup/fullSubtitle': u'An approch',
 '/chapter/citation/book/titleGroup/fullTitle': u'The Middle East',
 '/chapter/citation/book/totalPages': u'2',
 '/chapter/metadataInfo/PSMID': u'cho_rpax_1943_notes_000_0000',
 '/chapter/metadataInfo/chathamHouseRule': u'No',
 '/chapter/metadataInfo/contentDate/contentComposed': u'1943',
 '/chapter/metadataInfo/contentDate/contentDateEnd': u'1943-11-30',
 '/chapter/metadataInfo/contentDate/contentDateStart': u'1943-11-01',
 '/chapter/metadataInfo/contentDate/contentDecade': u'1940-1949',
 '/chapter/metadataInfo/contentDate/contentMonth': u'11',
 '/chapter/metadataInfo/contentDate/contentYear': u'1943',
 '/chapter/metadataInfo/isbn': u'978-567-891-0111',
 '/chapter/metadataInfo/issn': u'12345678',
 '/chapter/metadataInfo/language[1]': u'English',
 '/chapter/metadataInfo/language[2]': u'French',
 '/chapter/metadataInfo/productContentType': u'Pamphlets and Reports',
 '/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'COPYRIGHT under the aupicies of Royal Institute of International Affairs',
 '/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 '/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 '_dom_id': u'cho_rpax_1943_notes_000_0000',
 '_dom_name': u'cho_rpax_1943_notes_000_0000'}


>>> pages = dom_adapter.pages()
>>> len(pages)
2

>>> print pages[len(pages) - 1]
Page(dom_id="2", dom_name="2", info="{'/chapter/page[2]/sourcePage': u'2', '/chapter/page[2]/article/text/textclip/footnote/word': '_IS_ABSENT_', '_asset_fname': u'cho_rpax_1943_notes_000_0002.jpg', '@id': '2', '_id': 2}")

>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
3

>>> print chunks[len(chunks) - 1]
Chunk(dom_id="3", dom_name="photograph_3", clip_ids="None", is_binary="True", page_ids="[1]", info="{'/chapter/page[1]/article/illustration[2]/caption': '_IS_ABSENT_', '/chapter/page[1]/article/illustration[2]/@pgref': u'1', '/chapter/page[1]/article/illustration[2]/@colorimage': u'color', '/chapter/page[1]/article/illustration[2]/@type': u'photograph'}")

>>> print(dom_adapter.clips())
[]

>>> for link in dom_adapter.links():
...     print link

'''
