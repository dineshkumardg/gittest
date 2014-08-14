import doctest

suite = doctest.DocFileSuite('test_cho_content_type.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_content_type.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)


'''
>>> from project.cho.cho_content_type import ChoContentType

>>> chapter_citation_book_value = None
>>> product_content_type = 'Books'
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
book

>>> product_content_type = 'Special Publications'
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
journal

>>> product_content_type = 'Special Publications'
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
journal

>>> product_content_type = "some product content type we don't know about"
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
None

>>> chapter_citation_book_value = 'book'
>>> product_content_type = 'Special Publications'
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
book

>>> chapter_citation_book_value = None
>>> product_content_type = 'Special Publications'
>>> print ChoContentType.content_type(chapter_citation_book_value, product_content_type)
journal

'''
