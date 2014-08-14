import doctest
suite = doctest.DocFileSuite('test_query.py')

if __name__ == '__main__':
    doctest.testfile("test_query.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import urllib2
>>> from mock import MagicMock, patch
>>> from testing.gaia_test import GaiaTest
>>> from test_utils.sorted_dict import sorted_dict
>>> from gaia.search.query import Query
>>> from gaia.search.search_error import SearchError

>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config

>>> config.search_server = '127.0.0.1:8983'
>>> config.search_collection = 'cho'
>>> query = Query(config.search_server, config.search_collection)

>>> # A. find --------------------------------------------------------
>>> #  _get represents: /mnt/UKDEV/SYSTEM_TEST_DATA/test_items/cho/common/page_numbers_wrong-cho_iaxx_1963_0039_000_0000/provider1/cho/items/all/cho_iaxx_1963_0039_000_0000
>>> query._get = MagicMock(return_value = (3, 0, [
...               {'_gaia_qa_link': '1|ChunkIndex(id="#3", dom_id="3" dom_name="Article Title" is_binary="False")|1',
...                '@level': '1',
...                'id': 'cho_iaxx_1963_0039_000_0000|1|3', '@type': 'article'}, 
...               {'_gaia_qa_link': '1|ChunkIndex(id="#5", dom_id="5" dom_name="Issue No. 1" is_binary="False")|1',
...                '@level': '1',
...                'id': 'cho_iaxx_1963_0039_000_0000|1|5',
...                '@type': 'article'}, 
...               {'_gaia_qa_link': '1|ChunkIndex(id="#6", dom_id="6" dom_name="The Polish Plan" is_binary="False")|1',
...                '@level': '2', 'id': 'cho_iaxx_1963_0039_000_0000|1|6',
...                '@type': 'article'}
...               ]))

>>> # on the UI its' @type:article or doc_productContentType=* &fl=@type&fl=@level
>>> _query = u'@type:article or doc_productContentType=* &fl=@type&fl=@level&fl=id,_gaia_qa_link'
>>> print query.find(_query)
([{'_gaia_qa_link': '1|ChunkIndex(id="#3", dom_id="3" dom_name="Article Title" is_binary="False")|1', '@level': '1', 'id': 'cho_iaxx_1963_0039_000_0000|1|3', '@type': 'article'}, {'_gaia_qa_link': '1|ChunkIndex(id="#5", dom_id="5" dom_name="Issue No. 1" is_binary="False")|1', '@level': '1', 'id': 'cho_iaxx_1963_0039_000_0000|1|5', '@type': 'article'}, {'_gaia_qa_link': '1|ChunkIndex(id="#6", dom_id="6" dom_name="The Polish Plan" is_binary="False")|1', '@level': '2', 'id': 'cho_iaxx_1963_0039_000_0000|1|6', '@type': 'article'}], 3)

>>> # B. count --------------------------------------------------------
>>> print query.count(_query)
3

>>> # C. find except's --------------------------------------------------------
>>> query = Query('123.456.789.123', config.search_collection)
>>> try:
...     query.find(_query)
... except SearchError, e:
...     print e.msg
Cannot Analyse due to a SEARCH SERVER PROBLEM

>>> # D: facet tests ===========================================================
>>> query = Query('server', 'collection')
>>> query._get = MagicMock(return_value =\
...   (777, 0, [], {'facet_queries':{},'facet_fields':{'pageCount':['4',13,'1',6,'2',5,'3',5,'5',3,'6',2,'7',1]},'facet_dates':{},'facet_ranges':{}}))
>>>  
>>> search_query = 'id:*'
>>> facet_field = 'pageCount'
>>> num_found, field_counts = query.facet(search_query, facet_field)
>>> print num_found, sorted_dict(field_counts)
777 OrderedDict([('1', 6), ('2', 5), ('3', 5), ('4', 13), ('5', 3), ('6', 2), ('7', 1)])

>>> test.tearDown()

'''
