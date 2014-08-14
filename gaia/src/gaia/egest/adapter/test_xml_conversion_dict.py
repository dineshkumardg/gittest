import doctest
suite = doctest.DocFileSuite('test_xml_conversion_dict.py')

if __name__ == '__main__':
    doctest.testfile("test_xml_conversion_dict.py")

'''
>>> from lxml import etree
>>> from cStringIO import StringIO
>>> from pprint import pprint
>>> from gaia.egest.adapter.xml_conversion_dict import XmlConversionDict
>>> xml = """
... <book>
...   <title lang="EN" id="1234">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...     <self_closed/>
...     <empty_element></empty_element>
...     <article>Everything is Sad</article>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> # TEST returning None instead of _IS_ABSENT_ =======================================================
>>> changed_xml = {'/book/title': u'_IS_ABSENT_'} 
>>> x = XmlConversionDict(tree, changed_xml)
>>> print x['/book/title']                  # test an _IS_ABSENT_ field
None
>>> print x['/book/chapter/empty_element']  # test an empty field
None
>>> print x['/book/chapter/DOES_NOT_EXIST']  # test a missing field
None
>>> x['/book/title/@lang']
u'EN'
>>> x['/book/chapter[1]/title']
u'In the Beginning'
>>> x['/book/chapter[1]/article']
u'Everything is Sad'

'''
