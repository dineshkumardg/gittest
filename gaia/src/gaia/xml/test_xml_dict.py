import doctest
suite = doctest.DocFileSuite('test_xml_dict.py')

if __name__ == '__main__':
    doctest.testfile("test_xml_dict.py")#, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from lxml import etree
>>> from cStringIO import StringIO
>>> from pprint import pprint
>>> from gaia.xml.xml_dict import XmlDict
>>> # A: TEST SINGLE  =======================================================
>>> xml = """
... <book>
...   <title lang="EN" id="1234">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...     <self_closed/>
...     <empty_element></empty_element>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)
>>> # BASIC Tests -----------------------------------------------------------
>>> # NOTE: ALL DATA should be returned as UNICODE STRING type
>>> x['/book/title']
u'Hello World'

>>> x['/book/title/@lang']
u'EN'

>>> x['/book/chapter/title']
u'In the Beginning'

>>> # A better (more resilient) way: see below) of addressing this node:
>>> x['/book/chapter[1]/title']
u'In the Beginning'

>>> pages = x['/book/chapter/pages']
>>> pages
u'13'

>>> x['/book/title/@id']
u'1234'

>>> # Test empty nodes -----------------------------------------------------------
>>> # test a self-closed element
>>> x['/book/chapter/self_closed'] == None
True

>>> # test an empty element
>>> x['/book/chapter/empty_element'] == None
True

>>> # Test missing nodes -----------------------------------------------------------
>>> x['/not/at/home'] == None    # Note: expect None instead of a KeyError
True


>>> # B: TEST MULTIPLE: nodes  =======================================================
>>> xml = """
... <book>
...   <title lang="EN">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...   </chapter>
...   <chapter>
...     <title>In the End</title>
...     <pages>9</pages>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)

>>> x['/book/chapter[1]/title']
u'In the Beginning'

>>> x['/book/chapter[1]/pages']
u'13'

>>> x['/book/chapter[2]/title']
u'In the End'

>>> x['/book/chapter[2]/pages']
u'9'

>>> x['/book/chapter/title'] # WARNING: Note that this does NOT match the first node: matches ALL nodes
[u'In the Beginning', u'In the End']

>>> # TEST multiple within node  =======================================================
>>> xml = """
... <book>
...   <title lang="EN" id="1234">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...     <word>hello1</word>
...     <word>hello2</word>
...     <word>hello3</word>
...     <word>hello4</word>
...     <word>hello5</word>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)

>>> # NOTE: if there are multiple nodes, the basic xpath will return a LIST..
>>> x['/book/chapter/word']
[u'hello1', u'hello2', u'hello3', u'hello4', u'hello5']

>>> # ... so you need to have more explicit addressing if you just want the first node
>>> # *** WHICH IS ALWAYS SAFE TO USE even if there's only one node
>>> # *** PLEASE NOTE WELL! ***
>>> x['/book/title[1]']
u'Hello World'

>>> x['/book/chapter/word[1]']
u'hello1'

>>> x['/book/chapter/word[3]']
u'hello3'

>>> x['/book/chapter/word[5]']
u'hello5'

>>> x['/book/chapter/word[99]'] == None
True

>>> # C: TEST __setitem__  =======================================================
>>> xml = """
... <book>
...   <title lang="EN" id="1234">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...   </chapter>
...   <chapter>
...     <title>In the End</title>
...     <pages>9</pages>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)
>>> print(etree.tostring(tree.getroot()))
<book>
  <title lang="EN" id="1234">Hello World</title>
  <chapter>
    <title>In the Beginning</title>
    <pages>13</pages>
  </chapter>
  <chapter>
    <title>In the End</title>
    <pages>9</pages>
  </chapter>
</book>

>>> # Change an existing node
>>> x['/book/title'] = 'Goodbye Universe'
>>> x['/book/title']
u'Goodbye Universe'

>>> # Change an existing attribute
>>> x['/book/title/@lang'] = 'DE'
>>> x['/book/title/@lang']
u'DE'

>>> x['/book/chapter[2]/title'] = 'No End In Sight'
>>> # Add new attributes
>>> x['/book/chapter[2]/title/@ending'] = 'never'
>>> x['/book/chapter[2]/title/@year'] = '2999'
>>> x['/book/chapter[2]/title']
u'No End In Sight'

>>> print(etree.tostring(tree.getroot()))
<book>
  <title lang="DE" id="1234">Goodbye Universe</title>
  <chapter>
    <title>In the Beginning</title>
    <pages>13</pages>
  </chapter>
  <chapter>
    <title ending="never" year="2999">No End In Sight</title>
    <pages>9</pages>
  </chapter>
</book>

>>> from gaia.error import GaiaCodingError
>>> try:
...     x['/not/at whitespace/home']
... except GaiaCodingError, e:
...     print e
GaiaCodingError: XmlDict.getitem() failed: Problem with xpath (xpath="/not/at whitespace/home", error="Invalid expression")

>>> # D: TEST USE MULTIPLE OCCURANCES =======================================================
>>> xml = """
... <book>
...   <title lang="EN" id="1234">Hello World</title>
...   <chapter>
...     <title>In the Beginning</title>
...     <pages>13</pages>
...     <pages>14
...       <word>a</word>
...       <word>b</word>
...     </pages>
...     <pages>15</pages>
...     <self_closed/>
...     <empty_element></empty_element>
...   </chapter>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)
>>> x['/book/chapter/pages']
[u'13', u'14\n      ', u'15']

>>> len(x['/book/chapter/pages'])
3

>>> x['/book/chapter/pages[2]/word']
[u'a', u'b']

>>> x['/book/chapter/pages[2]/word[1]']
u'a'


>>> # entity reference tests  -----------------------------------------------------------
>>> # RE: http://en.wikipedia.org/wiki/List_of_XML_and_HTML_character_entity_references#Predefined_entities_in_XML
>>> # entity reference in should get entity reference out!
>>> #
>>> # WARNING: to properly process entity refs. you ***MUST***
>>> # create the xml etree in the correct way (in particular, resolve_entities=False):
>>> # Unfortunately, resolve_enitites=False ONLY works for dtd-defined entities, not the standard ones, so thi sdoes NOT fix thi stest! :(
>>> #parser = etree.XMLParser(resolve_entities=False)     #, no_network=True)
>>> #tree   = etree.parse(StringIO(xml), parser)
>>> #etree.tostring(tree.getroot())
>>> #
>>> # NOTE: quotatations only get transformed in attributes?: &quot;
>>> # ..and &apos; never gets transformed (because attrs are output with double, not single quotes?
>>> #
>>> xml ="<a double_quoted=\"hello &quot; &apos; world\" single_quoted=\'hello &quot; &apos; world\'>&lt;x&gt;x&amp;x&apos;x&quot;</a>"
>>> tree =  etree.parse(StringIO(xml))
>>> element = tree.xpath('/a')
>>> xml_dict = XmlDict(tree)
>>> print xml_dict['/a']
<x>x&x'x"

>>> print etree.tostring(tree)
<a double_quoted="hello &quot; ' world" single_quoted="hello &quot; ' world">&lt;x&gt;x&amp;x'x"</a>


>>> # test for the word 'None' in the xml  =======================================================
>>> xml = """
... <book>
...   <title>None</title>
...   <name></name>
...   <majestic_title/>
... </book>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)
>>> x['/book/title']
u'None'

>>> x['/book/name']

>>> x['/book/majestic_title']

>>> # test for a single illustration (empty element)  =======================================================
>>> xml = """<chapter>
...     <page>
...         <article>
...             <illustration pgref="166" type="chart" colorimage="color"/>
...         </article>
...     </page>
...     <page>
...         <article>
...             <illustration pgref="221" type="chart" colorimage="color"/>
...             <illustration pgref="223" type="chart" colorimage="color"/>
...         </article>
...     </page>
... </chapter>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = XmlDict(tree)
>>> x['/chapter/page[1]/article[1]/illustration']  # TODO what to do when an element value is empty but its attributes are not!


>>> x['/chapter/page[2]/article[1]/illustration']
[None, None]

'''
