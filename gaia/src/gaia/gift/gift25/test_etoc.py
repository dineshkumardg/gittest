import doctest
suite = doctest.DocFileSuite('test_etoc.py')

if __name__ == '__main__':
    doctest.testfile("test_etoc.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import etoc
>>> from lxml import etree

>>> # A: TEST DOCUMENT  =======================================================
>>> document = etoc.document('document')
>>> print etree.tostring(document, pretty_print=True)
<etoc:document xmlns:etoc="http://www.gale.com/goldschema/etoc">document</etoc:document>
<BLANKLINE>

>>> # B: TEST ETOC_UNIQUE_ID  =======================================================
>>> etoc_unique_id = etoc.etoc_unique_id('etoc_unique_id')
>>> print etree.tostring(etoc_unique_id, pretty_print=True)
<etoc:etoc-unique-id xmlns:etoc="http://www.gale.com/goldschema/etoc">etoc_unique_id</etoc:etoc-unique-id>
<BLANKLINE>

'''
