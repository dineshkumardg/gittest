import doctest
suite = doctest.DocFileSuite('test_qa_query.py')

if __name__ == '__main__':
    doctest.testfile("test_qa_query.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> import urllib2
>>> from mock import MagicMock, patch
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> from test_utils.sorted_dict import sorted_dict
>>> test = GaiaDjangoTest()
>>> test.setUp()
>>> from qa.qa_link import QaLink
>>> from qa.qa_query import QaQuery
>>> from gaia.search.search_error import SearchError
>>> from qa.models import Item
>>> #
>>> config = test.config
>>> config.search_server = '127.0.0.1:8983'
>>> config.search_collection = 'cho'
>>> query = QaQuery(config.search_server, config.search_collection)
>>> #
>>> # add_item ----------------------------------------------
>>> item_index_id = '123'
>>> item_dom_id = 'cho_iaxx_1963_0039_000_0000'
>>> item = Item(id=item_index_id, dom_id=item_dom_id, dom_name='dom_name1')
>>> item.save()
>>> item.ready_for_qa()
>>> #
>>> qa_link = QaLink(item_index_id, chunk_index_id='4', first_page_index_id='5')
>>> #
>>> # mock query.find() --------------------------------------------------------
>>> num_found = 3
>>> info = {'title': 'Japan'} 
>>> qa_link.decorate_info(info)
>>> matches = [info, ]
>>> query.find = MagicMock(return_value = (matches, num_found))
>>> #
>>> # test_find_items -------------------------------------------------
>>> search_expression = u'title:Japan AND title:America'
>>> search_parameters = {'fl': 'title', 'rows': '123', 'facet': 'true'}
>>> items = query.find_items(search_expression, search_parameters)
>>> print len(items)
1

>>> for item in items:
...     print item.id, item.dom_id, item.dom_name, item.is_live, item.has_changed
123 cho_iaxx_1963_0039_000_0000 dom_name1 True False

>>> test.tearDown()

'''
