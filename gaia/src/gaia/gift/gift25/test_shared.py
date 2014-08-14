import doctest
suite = doctest.DocFileSuite('test_shared.py')

if __name__ == '__main__':
    doctest.testfile("test_shared.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import shared
>>> from lxml import etree

>>> # A: TEST MEDIA  =======================================================
>>> media = shared.media('media')
>>> print etree.tostring(media, pretty_print=True)
<shared:media xmlns:shared="http://www.gale.com/goldschema/shared">media</shared:media>
<BLANKLINE>

'''
