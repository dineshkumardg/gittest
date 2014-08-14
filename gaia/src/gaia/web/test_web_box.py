# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest

suite = doctest.DocFileSuite('test_web_box.py')

if __name__ == '__main__':
    import testing
    testing.main(suite)



''' 
>>> import os
>>> import shutil
>>> import logging
>>> import json
>>> from pprint import pprint
>>> from django.conf import settings
>>> from gaia.config.config import get_config
>>> from gaia.log.log import Log
>>> from gaia.asset.asset import Asset
>>> import project.cho.gaia_dom_adapter.factory

>>> from testing.gaia_django_test import GaiaDjangoTest
>>> test = GaiaDjangoTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config

# ==================================================
# Set up ===========================================
# ==================================================

>>> doc_id = 'cho_iaxx_1963_0039_000_0000'
>>> test_files_dir = os.path.join(os.path.dirname(__file__), 'test_files')
>>> xml_fpath = os.path.join(test_files_dir, '%s.xml' % doc_id)

>>> web_root = os.path.join(test_dir, 'web_root')
>>> _log_dir = os.path.join(test_dir, 'log_dir')

>>> try:
...     os.makedirs(web_root)
...     os.makedirs(_log_dir)
... except Exception, e:
...     print 'Problem creating directory: %s' % str(e)

>>> asset = Asset(xml_fpath, 'rb')
>>> assets = [asset,]

>>> class Config:
...    WEB_ROOT = web_root
...    web_image_ftype = 'png'
...    log_dir = _log_dir
...    log_level = logging.DEBUG
...    dom_adapter_factory = project.cho.gaia_dom_adapter.factory.Factory
...    search_server = '127.0.0.1' # dummy for testing
...    search_adapter_class_name = 'gaia.search.adapter.chunk_search_adapter.ChunkSearchAdapter'

>>> config = Config()

# Logging
>>> log_fpath = os.path.join(config.log_dir, 'test_web_box')
>>> log_fpath = Log.configure_logging('test_web_box', config, multi_process=False, rollover=False)

# ==================================================
# Test the WebBox ==================================
# ==================================================

>>> from gaia.web.web_box import WebBox
>>> # stub out the search-functionality as this requires a search server to be running..
>>> # stub out the asset id functionality as this requires a real AssetId server in the US!
>>> class FakeAssetIdService:
...     next_id = 1
...     def get(self):
...         self.next_id += 1
...         return self.next_id
>>> #
>>> class TestableWebBox(WebBox):
...     def __init__(self, config):
...         WebBox.__init__(self, config)
...         self.fid_service = FakeAssetIdService()
...     
...     def _add_search_item(self, item, item_index_id):
...         print 'Called: _add_search_item(', item, item_index_id, ')'
...     def _delete_search_item(self, item_index_id):
...         print 'Called: _delete_search_item(', item_index_id, ')'


>>> web_box = TestableWebBox(config)
>>> from gaia.dom.model.item import Item
>>> item = Item(doc_id, doc_id, assets, config)
>>> web_box.add_item(item)
Called: _add_search_item( Item (dom_id="cho_iaxx_1963_0039_000_0000", dom_name="cho_iaxx_1963_0039_000_0000") 1 )

>>> item_index_id = 1

# ==================================================
# Doc info =========================================
# ==================================================
>>> pprint(json.loads((web_box.doc_info(doc_id, item_index_id, doc_id))))
{u'/chapter/@contentType': u'Journal',
 u'/chapter/citation/journal/author/@role': u'editor',
 u'/chapter/citation/journal/author/@type': u'_IS_ABSENT_',
 u'/chapter/citation/journal/author/aucomposed': u'N. P. McDonald',
 u'/chapter/citation/journal/author/first': u'N.',
 u'/chapter/citation/journal/author/last': u'McDonald',
 u'/chapter/citation/journal/author/middle': u'P.',
 u'/chapter/citation/journal/byline': u'_IS_ABSENT_',
 u'/chapter/citation/journal/editionNumber': u'_IS_ABSENT_',
 u'/chapter/citation/journal/editionStatement': u'_IS_ABSENT_',
 u'/chapter/citation/journal/pubDate/composed': u'January 1963',
 u'/chapter/citation/journal/pubDate/month': u'January',
 u'/chapter/citation/journal/pubDate/pubDateEnd': u'1963-01-31',
 u'/chapter/citation/journal/pubDate/pubDateStart': u'1963-01-01',
 u'/chapter/citation/journal/pubDate/year': u'1963',
 u'/chapter/citation/journal/titleGroup/fullTitle': u'International Affairs',
 u'/chapter/citation/journal/totalPages': u'16',
 u'/chapter/citation/journal/volumeGroup/volumeNumber': u'39',
 u'/chapter/citation/journal/volumeGroup/volumeTitle': u'Vol.39 1963',
 u'/chapter/metadataInfo/PSMID': u'cho_iaxx_1963_0039_000_0000',
 u'/chapter/metadataInfo/chathamHouseRule': u'No',
 u'/chapter/metadataInfo/contentDate/contentComposed': u'1968',
 u'/chapter/metadataInfo/contentDate/contentDateEnd': u'2002-09-25',
 u'/chapter/metadataInfo/contentDate/contentDateStart': u'2002-08-24',
 u'/chapter/metadataInfo/contentDate/contentDay': u'01',
 u'/chapter/metadataInfo/contentDate/contentDecade': u'1960-1969',
 u'/chapter/metadataInfo/contentDate/contentIrregular': u'contentIrregular',
 u'/chapter/metadataInfo/contentDate/contentMonth': u'April',
 u'/chapter/metadataInfo/contentDate/contentYear': u'1968',
 u'/chapter/metadataInfo/isbn': u'1234567890',
 u'/chapter/metadataInfo/issn': u'_IS_ABSENT_',
 u'/chapter/metadataInfo/language': u'EN',
 u'/chapter/metadataInfo/productContentType': u'Journals',
 u'/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Statement',
 u'/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 u'/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 u'_dom_id': u'cho_iaxx_1963_0039_000_0000',
 u'_dom_name': u'cho_iaxx_1963_0039_000_0000'}

# ==================================================
# Page info ========================================
# ==================================================
>>> pprint(json.loads((web_box.page_info(doc_id, item_index_id, 1))))
{u'/chapter/page[1]/article/text/textclip/footnote/word': u'WORD',
 u'/chapter/page[1]/sourcePage': u'I',
 u'@id': u'0001',
 u'_asset_fname': u'cho_iaxx_1963_0039_000_0001.jpg',
 u'_dom_id': 1,
 u'_dom_name': u'I',
 u'_id': 1,
 u'_img_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0001.png',
 u'_thumb_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0001_thumbnail.png'}

>>> pprint(json.loads((web_box.page_info(doc_id, item_index_id, 2))))
{u'/chapter/page[2]/article/text/textclip/footnote/word': u'_IS_ABSENT_',
 u'/chapter/page[2]/sourcePage': u'II',
 u'@id': u'00002',
 u'_asset_fname': u'cho_iaxx_1963_0039_000_0002.jpg',
 u'_dom_id': 2,
 u'_dom_name': u'II',
 u'_id': 2,
 u'_img_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0002.png',
 u'_thumb_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0002_thumbnail.png'}

>>> pprint(json.loads((web_box.page_info(doc_id, item_index_id, 3))))
{u'/chapter/page[3]/article/text/textclip/footnote/word': u'_IS_ABSENT_',
 u'/chapter/page[3]/sourcePage': u'III',
 u'@id': u'00003',
 u'_asset_fname': u'cho_iaxx_1963_0039_000_0003.jpg',
 u'_dom_id': 3,
 u'_dom_name': u'III',
 u'_id': 3,
 u'_img_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0003.png',
 u'_thumb_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0003_thumbnail.png'}

>>> pprint(json.loads((web_box.page_info(doc_id, item_index_id, 4))))
{u'/chapter/page[4]/article/text/textclip/footnote/word': u'_IS_ABSENT_',
 u'/chapter/page[4]/sourcePage': u'IV',
 u'@id': u'00004',
 u'_asset_fname': u'cho_iaxx_1963_0039_000_0004.jpg',
 u'_dom_id': 4,
 u'_dom_name': u'IV',
 u'_id': 4,
 u'_img_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0004.png',
 u'_thumb_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0004_thumbnail.png'}

# ==================================================
# There are 16 pages in this XML
# ...
# ==================================================
 
>>> pprint(json.loads((web_box.page_info(doc_id, item_index_id, 16))))
{u'/chapter/page[16]/article/text/textclip/footnote/word': u'_IS_ABSENT_',
 u'/chapter/page[16]/sourcePage': u'12',
 u'@id': u'00016',
 u'_asset_fname': u'cho_iaxx_1963_0039_000_0016.jpg',
 u'_dom_id': 16,
 u'_dom_name': u'12',
 u'_id': 16,
 u'_img_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0016.png',
 u'_thumb_url': u'cho_iaxx_1963_0039_000_0000/1/cho_iaxx_1963_0039_000_0016_thumbnail.png'}

# ==================================================
# Chunk info =======================================
# ==================================================
>>> pprint(json.loads((web_box.chunk_info(doc_id, item_index_id, 1))))
{u'/chapter/page[1]/article/@id': u'1',
 u'/chapter/page[1]/article/@level': u'1',
 u'/chapter/page[1]/article/@type': u'front_matter',
 u'/chapter/page[1]/article/articleInfo/author/@type': u'_IS_ABSENT_',
 u'/chapter/page[1]/article/articleInfo/byline': u'_IS_ABSENT_',
 u'/chapter/page[1]/article/articleInfo/issueNumber': u'_IS_ABSENT_',
 u'/chapter/page[1]/article/articleInfo/issueTitle': u'_IS_ABSENT_',
 u'/chapter/page[1]/article/articleInfo/language': u'English',
 u'/chapter/page[1]/article/articleInfo/pageCount': u'2',
 u'/chapter/page[1]/article/articleInfo/pageRange': u'1-2',
 u'/chapter/page[1]/article/articleInfo/title': u'Front Matter',
 u'_clip_ids': None,
 u'_dom_id': 1,
 u'_dom_name': u'Front Matter',
 u'_is_binary': False,
 u'_page_ids': [1, 2]}

# There are 7 articles in this XML
# ...
# ...

>>> pprint(json.loads((web_box.chunk_info(doc_id, item_index_id, 7))))
{u'/chapter/page[5]/article[2]/illustration/@colorimage': u'color',
 u'/chapter/page[5]/article[2]/illustration/@pgref': u'00003',
 u'/chapter/page[5]/article[2]/illustration/@type': u'chart',
 u'/chapter/page[5]/article[2]/illustration/caption': u'Illustration Caption Here',
 u'_clip_ids': None,
 u'_dom_id': 7,
 u'_dom_name': u'Illustration Caption Here',
 u'_is_binary': True,
 u'_page_ids': [3]}

# ======================================================
# Try adding the same item again - Expecting another version
# and the old one shuld be deleted from the Search Index
# ======================================================

>>> # Note: this is a SUPERCEDE, so 2 is added, and 1 is deleted.
>>> web_box.add_item(item)
Called: _add_search_item( Item (dom_id="cho_iaxx_1963_0039_000_0000", dom_name="cho_iaxx_1963_0039_000_0000") 2 )
Called: _delete_search_item( 1 )

>>> item_index_id = 2

# ==================================================
# Doc info =========================================
# ==================================================
>>> pprint(json.loads((web_box.doc_info(doc_id, item_index_id, doc_id))))
{u'/chapter/@contentType': u'Journal',
 u'/chapter/citation/journal/author/@role': u'editor',
 u'/chapter/citation/journal/author/@type': u'_IS_ABSENT_',
 u'/chapter/citation/journal/author/aucomposed': u'N. P. McDonald',
 u'/chapter/citation/journal/author/first': u'N.',
 u'/chapter/citation/journal/author/last': u'McDonald',
 u'/chapter/citation/journal/author/middle': u'P.',
 u'/chapter/citation/journal/byline': u'_IS_ABSENT_',
 u'/chapter/citation/journal/editionNumber': u'_IS_ABSENT_',
 u'/chapter/citation/journal/editionStatement': u'_IS_ABSENT_',
 u'/chapter/citation/journal/pubDate/composed': u'January 1963',
 u'/chapter/citation/journal/pubDate/month': u'January',
 u'/chapter/citation/journal/pubDate/pubDateEnd': u'1963-01-31',
 u'/chapter/citation/journal/pubDate/pubDateStart': u'1963-01-01',
 u'/chapter/citation/journal/pubDate/year': u'1963',
 u'/chapter/citation/journal/titleGroup/fullTitle': u'International Affairs',
 u'/chapter/citation/journal/totalPages': u'16',
 u'/chapter/citation/journal/volumeGroup/volumeNumber': u'39',
 u'/chapter/citation/journal/volumeGroup/volumeTitle': u'Vol.39 1963',
 u'/chapter/metadataInfo/PSMID': u'cho_iaxx_1963_0039_000_0000',
 u'/chapter/metadataInfo/chathamHouseRule': u'No',
 u'/chapter/metadataInfo/contentDate/contentComposed': u'1968',
 u'/chapter/metadataInfo/contentDate/contentDateEnd': u'2002-09-25',
 u'/chapter/metadataInfo/contentDate/contentDateStart': u'2002-08-24',
 u'/chapter/metadataInfo/contentDate/contentDay': u'01',
 u'/chapter/metadataInfo/contentDate/contentDecade': u'1960-1969',
 u'/chapter/metadataInfo/contentDate/contentIrregular': u'contentIrregular',
 u'/chapter/metadataInfo/contentDate/contentMonth': u'April',
 u'/chapter/metadataInfo/contentDate/contentYear': u'1968',
 u'/chapter/metadataInfo/isbn': u'1234567890',
 u'/chapter/metadataInfo/issn': u'_IS_ABSENT_',
 u'/chapter/metadataInfo/language': u'EN',
 u'/chapter/metadataInfo/productContentType': u'Journals',
 u'/chapter/metadataInfo/sourceLibrary/copyrightStatement': u'Copyright Statement',
 u'/chapter/metadataInfo/sourceLibrary/libraryLocation': u'London, UK',
 u'/chapter/metadataInfo/sourceLibrary/libraryName': u'Chatham House',
 u'_dom_id': u'cho_iaxx_1963_0039_000_0000',
 u'_dom_name': u'cho_iaxx_1963_0039_000_0000'}

# ==================================================
# get_changes ======================================
# ==================================================
>>> # changes is returned as a full list of
>>> # all info objects, in one big list,
>>> # ie [doc_info; page_infos...; chunk_infos...]
>>> changes = web_box.get_changes(item)
>>> for change in changes:
...     print change['_dom_id'], change['_dom_name']
1 I
1 Front Matter
2 II
2 Illustration Caption Here
3 III
3 Article Title
4 IV
4 Illustration Caption Here
5 1
5 Issue No. 1
6 2
6 The Polish Plan
7 3
7 Illustration Caption Here
8 4
9 5
10 6
11 7
12 8
13 9
14 10
15 11
16 12
cho_iaxx_1963_0039_000_0000 cho_iaxx_1963_0039_000_0000


>>> for change in changes:
...     print "------------------------------------------------------------------------------"
...     for key in sorted(change.keys()):
...          print key, '=', change[key]
------------------------------------------------------------------------------
/chapter/page[1]/article/text/textclip/footnote/word = WORD
/chapter/page[1]/sourcePage = I
@id = 0001
_asset_fname = cho_iaxx_1963_0039_000_0001.jpg
_dom_id = 1
_dom_name = I
_id = 1
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0001.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0001_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[1]/article/@id = 1
/chapter/page[1]/article/@level = 1
/chapter/page[1]/article/@type = front_matter
/chapter/page[1]/article/articleInfo/author/@type = _IS_ABSENT_
/chapter/page[1]/article/articleInfo/byline = _IS_ABSENT_
/chapter/page[1]/article/articleInfo/issueNumber = _IS_ABSENT_
/chapter/page[1]/article/articleInfo/issueTitle = _IS_ABSENT_
/chapter/page[1]/article/articleInfo/language = English
/chapter/page[1]/article/articleInfo/pageCount = 2
/chapter/page[1]/article/articleInfo/pageRange = 1-2
/chapter/page[1]/article/articleInfo/title = Front Matter
_clip_ids = None
_dom_id = 1
_dom_name = Front Matter
_is_binary = False
_page_ids = [1, 2]
------------------------------------------------------------------------------
/chapter/page[2]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[2]/sourcePage = II
@id = 00002
_asset_fname = cho_iaxx_1963_0039_000_0002.jpg
_dom_id = 2
_dom_name = II
_id = 2
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0002.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0002_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[1]/article/illustration/@colorimage = color
/chapter/page[1]/article/illustration/@pgref = 0001
/chapter/page[1]/article/illustration/@type = chart
/chapter/page[1]/article/illustration/caption = Illustration Caption Here
_clip_ids = None
_dom_id = 2
_dom_name = Illustration Caption Here
_is_binary = True
_page_ids = [1]
------------------------------------------------------------------------------
/chapter/page[3]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[3]/sourcePage = III
@id = 00003
_asset_fname = cho_iaxx_1963_0039_000_0003.jpg
_dom_id = 3
_dom_name = III
_id = 3
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0003.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0003_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[3]/article/@id = 2
/chapter/page[3]/article/@level = 1
/chapter/page[3]/article/@type = article
/chapter/page[3]/article/articleInfo/author/@type = _IS_ABSENT_
/chapter/page[3]/article/articleInfo/author/aucomposed = Sarah Neate
/chapter/page[3]/article/articleInfo/author/first = Sarah
/chapter/page[3]/article/articleInfo/author/last = Neate
/chapter/page[3]/article/articleInfo/byline = _IS_ABSENT_
/chapter/page[3]/article/articleInfo/issueNumber = 1
/chapter/page[3]/article/articleInfo/issueTitle = No. 1
/chapter/page[3]/article/articleInfo/language = English
/chapter/page[3]/article/articleInfo/pageCount = 2
/chapter/page[3]/article/articleInfo/pageRange = 3-5
/chapter/page[3]/article/articleInfo/pubDate/composed = January 1963
/chapter/page[3]/article/articleInfo/pubDate/month = January
/chapter/page[3]/article/articleInfo/pubDate/pubDateEnd = 1963-12-31
/chapter/page[3]/article/articleInfo/pubDate/pubDateStart = 1963-01-01
/chapter/page[3]/article/articleInfo/pubDate/year = 1963
/chapter/page[3]/article/articleInfo/startingColumn = a
/chapter/page[3]/article/articleInfo/title = Article Title
_clip_ids = None
_dom_id = 3
_dom_name = Article Title
_is_binary = False
_page_ids = [2, 3, 4]
------------------------------------------------------------------------------
/chapter/page[4]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[4]/sourcePage = IV
@id = 00004
_asset_fname = cho_iaxx_1963_0039_000_0004.jpg
_dom_id = 4
_dom_name = IV
_id = 4
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0004.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0004_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[3]/article/illustration/@colorimage = color
/chapter/page[3]/article/illustration/@pgref = 00003
/chapter/page[3]/article/illustration/@type = chart
/chapter/page[3]/article/illustration/caption = Illustration Caption Here
_clip_ids = None
_dom_id = 4
_dom_name = Illustration Caption Here
_is_binary = True
_page_ids = [3]
------------------------------------------------------------------------------
/chapter/page[5]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[5]/sourcePage = 1
@id = 00005
_asset_fname = cho_iaxx_1963_0039_000_0005.jpg
_dom_id = 5
_dom_name = 1
_id = 5
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0005.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0005_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[5]/article[1]/@id = 3
/chapter/page[5]/article[1]/@level = 1
/chapter/page[5]/article[1]/@type = article
/chapter/page[5]/article[1]/articleInfo/author/@type = _IS_ABSENT_
/chapter/page[5]/article[1]/articleInfo/byline = _IS_ABSENT_
/chapter/page[5]/article[1]/articleInfo/issueNumber = 1
/chapter/page[5]/article[1]/articleInfo/issueTitle = No. 1
/chapter/page[5]/article[1]/articleInfo/language = English
/chapter/page[5]/article[1]/articleInfo/pageCount = 1
/chapter/page[5]/article[1]/articleInfo/pageRange = 5
/chapter/page[5]/article[1]/articleInfo/pubDate/composed = January 1963
/chapter/page[5]/article[1]/articleInfo/pubDate/month = January
/chapter/page[5]/article[1]/articleInfo/pubDate/pubDateEnd = 1963-04-30
/chapter/page[5]/article[1]/articleInfo/pubDate/pubDateStart = 1963-01-01
/chapter/page[5]/article[1]/articleInfo/pubDate/year = 1963
/chapter/page[5]/article[1]/articleInfo/title = Issue No. 1
_clip_ids = None
_dom_id = 5
_dom_name = Issue No. 1
_is_binary = False
_page_ids = [5]
------------------------------------------------------------------------------
/chapter/page[6]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[6]/sourcePage = 2
@id = 00006
_asset_fname = cho_iaxx_1963_0039_000_0006.jpg
_dom_id = 6
_dom_name = 2
_id = 6
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0006.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0006_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[5]/article[2]/@id = 4
/chapter/page[5]/article[2]/@level = 2
/chapter/page[5]/article[2]/@type = article
/chapter/page[5]/article[2]/articleInfo/author/@type = _IS_ABSENT_
/chapter/page[5]/article[2]/articleInfo/byline = _IS_ABSENT_
/chapter/page[5]/article[2]/articleInfo/issueNumber = 1
/chapter/page[5]/article[2]/articleInfo/issueTitle = No. 1
/chapter/page[5]/article[2]/articleInfo/language = English
/chapter/page[5]/article[2]/articleInfo/pageCount = 12
/chapter/page[5]/article[2]/articleInfo/pageRange = 1-12
/chapter/page[5]/article[2]/articleInfo/pubDate/composed = January 1963
/chapter/page[5]/article[2]/articleInfo/pubDate/month = January
/chapter/page[5]/article[2]/articleInfo/pubDate/pubDateEnd = 1963-04-30
/chapter/page[5]/article[2]/articleInfo/pubDate/pubDateStart = 1963-01-01
/chapter/page[5]/article[2]/articleInfo/pubDate/year = 1963
/chapter/page[5]/article[2]/articleInfo/startingColumn = a
/chapter/page[5]/article[2]/articleInfo/title = The Polish Plan
_clip_ids = None
_dom_id = 6
_dom_name = The Polish Plan
_is_binary = False
_page_ids = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
------------------------------------------------------------------------------
/chapter/page[7]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[7]/sourcePage = 3
@id = 00007
_asset_fname = cho_iaxx_1963_0039_000_0007.jpg
_dom_id = 7
_dom_name = 3
_id = 7
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0007.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0007_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[5]/article[2]/illustration/@colorimage = color
/chapter/page[5]/article[2]/illustration/@pgref = 00003
/chapter/page[5]/article[2]/illustration/@type = chart
/chapter/page[5]/article[2]/illustration/caption = Illustration Caption Here
_clip_ids = None
_dom_id = 7
_dom_name = Illustration Caption Here
_is_binary = True
_page_ids = [3]
------------------------------------------------------------------------------
/chapter/page[8]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[8]/sourcePage = 4
@id = 00008
_asset_fname = cho_iaxx_1963_0039_000_0008.jpg
_dom_id = 8
_dom_name = 4
_id = 8
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0008.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0008_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[9]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[9]/sourcePage = 5
@id = 00009
_asset_fname = cho_iaxx_1963_0039_000_0009.jpg
_dom_id = 9
_dom_name = 5
_id = 9
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0009.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0009_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[10]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[10]/sourcePage = 6
@id = 00010
_asset_fname = cho_iaxx_1963_0039_000_0010.jpg
_dom_id = 10
_dom_name = 6
_id = 10
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0010.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0010_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[11]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[11]/sourcePage = 7
@id = 00011
_asset_fname = cho_iaxx_1963_0039_000_0011.jpg
_dom_id = 11
_dom_name = 7
_id = 11
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0011.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0011_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[12]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[12]/sourcePage = 8
@id = 00012
_asset_fname = cho_iaxx_1963_0039_000_0012.jpg
_dom_id = 12
_dom_name = 8
_id = 12
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0012.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0012_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[13]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[13]/sourcePage = 9
@id = 00013
_asset_fname = cho_iaxx_1963_0039_000_0013.jpg
_dom_id = 13
_dom_name = 9
_id = 13
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0013.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0013_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[14]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[14]/sourcePage = 10
@id = 00014
_asset_fname = cho_iaxx_1963_0039_000_0014.jpg
_dom_id = 14
_dom_name = 10
_id = 14
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0014.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0014_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[15]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[15]/sourcePage = 11
@id = 00015
_asset_fname = cho_iaxx_1963_0039_000_0015.jpg
_dom_id = 15
_dom_name = 11
_id = 15
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0015.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0015_thumbnail.png
------------------------------------------------------------------------------
/chapter/page[16]/article/text/textclip/footnote/word = _IS_ABSENT_
/chapter/page[16]/sourcePage = 12
@id = 00016
_asset_fname = cho_iaxx_1963_0039_000_0016.jpg
_dom_id = 16
_dom_name = 12
_id = 16
_img_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0016.png
_thumb_url = cho_iaxx_1963_0039_000_0000/2/cho_iaxx_1963_0039_000_0016_thumbnail.png
------------------------------------------------------------------------------
/chapter/@contentType = Journal
/chapter/citation/journal/author/@role = editor
/chapter/citation/journal/author/@type = _IS_ABSENT_
/chapter/citation/journal/author/aucomposed = N. P. McDonald
/chapter/citation/journal/author/first = N.
/chapter/citation/journal/author/last = McDonald
/chapter/citation/journal/author/middle = P.
/chapter/citation/journal/byline = _IS_ABSENT_
/chapter/citation/journal/editionNumber = _IS_ABSENT_
/chapter/citation/journal/editionStatement = _IS_ABSENT_
/chapter/citation/journal/pubDate/composed = January 1963
/chapter/citation/journal/pubDate/month = January
/chapter/citation/journal/pubDate/pubDateEnd = 1963-01-31
/chapter/citation/journal/pubDate/pubDateStart = 1963-01-01
/chapter/citation/journal/pubDate/year = 1963
/chapter/citation/journal/titleGroup/fullTitle = International Affairs
/chapter/citation/journal/totalPages = 16
/chapter/citation/journal/volumeGroup/volumeNumber = 39
/chapter/citation/journal/volumeGroup/volumeTitle = Vol.39 1963
/chapter/metadataInfo/PSMID = cho_iaxx_1963_0039_000_0000
/chapter/metadataInfo/chathamHouseRule = No
/chapter/metadataInfo/contentDate/contentComposed = 1968
/chapter/metadataInfo/contentDate/contentDateEnd = 2002-09-25
/chapter/metadataInfo/contentDate/contentDateStart = 2002-08-24
/chapter/metadataInfo/contentDate/contentDay = 01
/chapter/metadataInfo/contentDate/contentDecade = 1960-1969
/chapter/metadataInfo/contentDate/contentIrregular = contentIrregular
/chapter/metadataInfo/contentDate/contentMonth = April
/chapter/metadataInfo/contentDate/contentYear = 1968
/chapter/metadataInfo/isbn = 1234567890
/chapter/metadataInfo/issn = _IS_ABSENT_
/chapter/metadataInfo/language = EN
/chapter/metadataInfo/productContentType = Journals
/chapter/metadataInfo/sourceLibrary/copyrightStatement = Copyright Statement
/chapter/metadataInfo/sourceLibrary/libraryLocation = London, UK
/chapter/metadataInfo/sourceLibrary/libraryName = Chatham House
_dom_id = cho_iaxx_1963_0039_000_0000
_dom_name = cho_iaxx_1963_0039_000_0000


# ==================================================
# _get_live_index ==================================
# ==================================================
>>> live_item = web_box._get_live_index(item)
>>> print '%s; %s; %s; %s; %s' % (live_item.id, live_item.dom_id, live_item.dom_name, live_item.is_live, live_item.has_changed)
2; cho_iaxx_1963_0039_000_0000; cho_iaxx_1963_0039_000_0000; True; False

# ==================================================
# Teardown
# ==================================================

>>> test.tearDown()

'''
