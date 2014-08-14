# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_qa_link.py')

if __name__ == '__main__':
    import testing
    testing.main(suite)

'''
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> django_test = GaiaDjangoTest()
>>> django_test.setUp()
>>> from qa.qa_link import QaLink
>>> QaLink.field_name
'_gaia_qa_link'

>>> info = {}
>>> item_index_id, chunk_index_id, first_page_index_id = 1, 2, 3
>>> #qa_link = QaLink(item_index_id, chunk_index_id, first_page_index_id)
>>> #qa_link.url(info)
>>> QaLink.link_info(info)
Traceback (most recent call last):
  File "c:\Python27\lib\doctest.py", line 1254, in __run
    compileflags, 1) in test.globs
  File "<doctest test_qa_link.py[6]>", line 1, in <module>
    qa_link.url(info)
  File "c:\GIT_REPOS\gaia\src\qa\qa_link.py", line 38, in url
    raise GaiaCodingError('missing "_qa_link" key from info dict!', info=info)
GaiaCodingError: GaiaCodingError: missing "_gaia_qa_link" key from info dict! (info="{}")

>>> qa_link = QaLink(item_index_id, chunk_index_id, first_page_index_id)
>>> qa_link.decorate_info(info)
>>> QaLink.link_info(info)
('/qa/page/3', '1', '2', '3')

>>> django_test.tearDown()

'''
