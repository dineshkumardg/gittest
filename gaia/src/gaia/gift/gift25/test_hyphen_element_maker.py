import doctest
suite = doctest.DocFileSuite('test_hyphen_element_maker.py')

if __name__ == '__main__':
    doctest.testfile("test_hyphen_element_maker.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25.hyphen_element_maker import HyphenElementMaker
>>> from lxml import etree

>>> # A: TEST WITHOUT HYPTHEN  =======================================================
>>> E = HyphenElementMaker()
>>> without_hyphen = E.element('value')
>>> print etree.tostring(without_hyphen, pretty_print=True)
<element>value</element>
<BLANKLINE>

>>> # B: TEST WITH HYPHEN  =======================================================
>>> with_hyphen = E.element_with_hyphen('value')
>>> print etree.tostring(with_hyphen, pretty_print=True)
<element-with-hyphen>value</element-with-hyphen>
<BLANKLINE>

'''
