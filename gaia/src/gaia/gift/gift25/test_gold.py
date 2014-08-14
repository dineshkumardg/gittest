import doctest
suite = doctest.DocFileSuite('test_gold.py')

if __name__ == '__main__':
    doctest.testfile("test_gold.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from gaia.gift.gift25 import gold
>>> from gaia.gift.gift25.hyphen_element_maker import attr
>>> from lxml import etree

>>> # A: TEST FEED  =======================================================
>>> document_instance = gold.document_instance('document_instance')
>>> metadata = gold.metadata(
...     '_feed_type',
...     '_document_schema',
...     '_schema_version',
...     '_document_id_path',
...     '_document_mcode_path',
...     '_number_of_documents',
...     '_feed_status')

>>> # B: TEST FEED_TYPE  =======================================================
>>> feed_type = gold.feed_type('feed_type')
>>> print etree.tostring(feed_type, pretty_print=True)
<gold:feed-type xmlns:gold="http://www.gale.com/gold">feed_type</gold:feed-type>
<BLANKLINE>

>>> # C: TEST DOCUMENT_SCHEMA  =======================================================
>>> document_schema = gold.document_schema('document_schema')
>>> print etree.tostring(document_schema, pretty_print=True)
<gold:document-schema xmlns:gold="http://www.gale.com/gold">document_schema</gold:document-schema>
<BLANKLINE>

>>> # D: TEST SCHEMA_VERSION  =======================================================
>>> schema_version = gold.schema_version('schema_version')
>>> print etree.tostring(schema_version, pretty_print=True)
<gold:schema-version xmlns:gold="http://www.gale.com/gold">schema_version</gold:schema-version>
<BLANKLINE>

>>> # E: TEST DOCUMENT_ID_PATH  =======================================================
>>> document_id_path = gold.document_id_path('document_id_path')
>>> print etree.tostring(document_id_path, pretty_print=True)
<gold:document-id-path xmlns:gold="http://www.gale.com/gold">document_id_path</gold:document-id-path>
<BLANKLINE>

>>> # F: TEST DOCUMENT_MCODE_PATH  =======================================================
>>> document_mcode_path = gold.document_mcode_path('document_mcode_path')
>>> print etree.tostring(document_mcode_path, pretty_print=True)
<gold:document-mcode-path xmlns:gold="http://www.gale.com/gold">document_mcode_path</gold:document-mcode-path>
<BLANKLINE>

>>> # G: TEST NUMBER_OF_DOCUMENTS  =======================================================
>>> number_of_documents = gold.number_of_documents('number_of_documents')
>>> print etree.tostring(number_of_documents, pretty_print=True)
<gold:number-of-documents xmlns:gold="http://www.gale.com/gold">number_of_documents</gold:number-of-documents>
<BLANKLINE>

>>> # H: TEST FEED_STATUS  =======================================================
>>> feed_status = gold.feed_status('feed_status')
>>> print etree.tostring(feed_status, pretty_print=True)
<gold:feed-status xmlns:gold="http://www.gale.com/gold">feed_status</gold:feed-status>
<BLANKLINE>

>>> # I: TEST DOCUMENT_INSTANCE  =======================================================
>>> document_instance = gold.document_instance('document_instance')
>>> print etree.tostring(document_instance, pretty_print=True)
<gold:document-instance xmlns:gold="http://www.gale.com/gold">document_instance</gold:document-instance>
<BLANKLINE>

'''
