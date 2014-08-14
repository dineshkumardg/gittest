import doctest
suite = doctest.DocFileSuite('test_document_instances.py')

if __name__ == '__main__':
    doctest.testfile("test_document_instances.py", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> from lxml import etree
>>> from project.cho.egest_adapter.doc.document_instances import DocumentInstances
>>> from test_utils.test_helper import TestHelper

>>> # Set up config for logging 
>>> test_dir, log_fpath, log_fname, config = TestHelper().setUp()

>>> document_instances = DocumentInstances(config, 'source_xml_dict', 'builders', 'extra_args')
>>> home = os.environ['HOME']
>>> with open(os.path.join(home, 'GIT_REPOS/gaia/src/project/cho/egest_adapter/doc/test_data/cho_bcrc_1933_0001_000_0000_PARENT.xml'), 'r') as gift_xml: 
...     xml = gift_xml.read()

>>> # Test a valid xml, expectation nothing (i.e no error)
>>> document_instances._validate(xml)

>>> # Test a malformed xml fails validation
>>> invalid_xml = xml.replace('/','')
>>> document_instances._validate(invalid_xml)
Traceback (most recent call last):
  ...
InvalidXmlError: InvalidXmlError: gift document-instance(s) -- badly formed (error="Excessive depth in document: 256 use XML_PARSE_HUGE option, line 193, column 13")

>>> # Test an xml that is not valid against the xsd
>>> gift_validation_xml = xml.replace('19330101', 'baluabcdefg') 
>>> document_instances._validate(gift_validation_xml)
Traceback (most recent call last):
  ...
GiftValidationError: GiftValidationError: gift document-instance(s) do not validate against XSD (missing="Element '{http://www.gale.com/goldschema/metadata}standard-date': 'baluabcdefg' is not a valid value of the atomic type 'xs:integer'., line 28")

>>> TestHelper().tearDown(test_dir)

'''
