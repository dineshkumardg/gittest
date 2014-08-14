import doctest
suite = doctest.DocFileSuite('test_gift_doc.py')

if __name__ == '__main__':
    doctest.testfile("test_gift_doc.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import gift_doc
>>> from lxml import etree

>>> # A: TEST NODE_METADATA  =======================================================
>>> node_metadata = gift_doc.node_metadata('node_metadata')
>>> print etree.tostring(node_metadata, pretty_print=True)
<gift-doc:node-metadata xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">node_metadata</gift-doc:node-metadata>
<BLANKLINE>

>>> # B: TEST DOCUMENT  =======================================================
>>> document = gift_doc.document('document')
>>> print etree.tostring(document, pretty_print=True)
<gift-doc:document xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">document</gift-doc:document>
<BLANKLINE>

>>> # C: TEST METADATA  =======================================================
>>> metadata = gift_doc.metadata('metadata')
>>> print etree.tostring(metadata, pretty_print=True)
<gift-doc:metadata xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">metadata</gift-doc:metadata>
<BLANKLINE>

>>> # D: TEST BODY  =======================================================
>>> body = gift_doc.body('body')
>>> print etree.tostring(body, pretty_print=True)
<gift-doc:body xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">body</gift-doc:body>
<BLANKLINE>

>>> # E: TEST DOCUMENT_METADATA  =======================================================
>>> document_metadata = gift_doc.document_metadata('document_metadata')
>>> print etree.tostring(document_metadata, pretty_print=True)
<gift-doc:document-metadata xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">document_metadata</gift-doc:document-metadata>
<BLANKLINE>

>>> # F: TEST PAGINATION_GROUP  =======================================================
>>> pagination_group = gift_doc.pagination_group('pagination_group')
>>> print etree.tostring(pagination_group, pretty_print=True)
<gift-doc:pagination-group xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">pagination_group</gift-doc:pagination-group>
<BLANKLINE>

>>> # G: TEST PAGINATION  =======================================================
>>> pagination = gift_doc.pagination('pagination')
>>> print etree.tostring(pagination, pretty_print=True)
<gift-doc:pagination xmlns:gift-doc="http://www.gale.com/goldschema/gift-doc">pagination</gift-doc:pagination>
<BLANKLINE>

'''
