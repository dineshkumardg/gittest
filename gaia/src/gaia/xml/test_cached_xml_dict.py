import doctest
suite = doctest.DocFileSuite('test_cached_xml_dict.py')

if __name__ == '__main__':
    doctest.testfile("test_cached_xml_dict.py")

'''
>>> from lxml import etree
>>> from cStringIO import StringIO
>>> from pprint import pprint
>>> from gaia.xml.cached_xml_dict import CachedXmlDict
>>> # TEST without cache  =======================================================
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
>>> x = CachedXmlDict(tree)
>>> x['/book/title']
u'Hello World'
>>> x['/book/title/@lang']
u'EN'
>>> x['/book/chapter[1]/title']
u'In the Beginning'

>>> # TEST with one cache_dict  =======================================================
>>> cache_dict = {'/book/title': u'a new (cached) title'}  # warning: values MUST be unicode strings please (not checked!)
>>> x = CachedXmlDict(tree, cache_dict)
>>> x['/book/title']
u'a new (cached) title'
>>> x['/book/title/@lang']
u'EN'
>>> x['/book/chapter[1]/title']
u'In the Beginning'
>>> x['/book/chapter[1]/article']
u'Everything is Sad'

>>> # TEST access of [1] xpaths with or without the [1] qualifier =======================================================
>>> cache_dict = {'/book/title': u'a new (cached) title'} 
>>> x = CachedXmlDict(tree, cache_dict)
>>> x['/book/title']
u'a new (cached) title'
>>> x['/book[1]/title']
u'a new (cached) title'
>>> #.. non-cached xpaths..
>>> x['/book/chapter/article']
u'Everything is Sad'
>>> x['/book/chapter[1]/article']
u'Everything is Sad'
>>> x['/book[1]/chapter[1]/article']
u'Everything is Sad'

>>> # TEST complicated cases : access of [1] xpaths with or without the [1] qualifier =======================================================
>>> cache_dict = {'/book[1]/title': u'a new (cached) title'}
>>> x = CachedXmlDict(tree, cache_dict)
>>> x['/book[1]/title']
u'a new (cached) title'
>>> x['/book/title']
u'a new (cached) title'
>>> x['/book[1]/chapter[1]/article']    # uncached
u'Everything is Sad'

>>> cache_dict = {'/book[1]/title': u'a new (cached) title', '/book[1]/chapter[1]/article': u'CACHED ARTICLE'}
>>> x = CachedXmlDict(tree, cache_dict)
>>> x['/book[1]/title']
u'a new (cached) title'
>>> x['/book/title']
u'a new (cached) title'
>>> x['/book[1]/chapter[1]/article']
u'CACHED ARTICLE'
>>> x['/book/chapter[1]/article']
u'CACHED ARTICLE'
>>> x['/book[1]/chapter/article']
u'CACHED ARTICLE'
>>> x['/book/chapter/article']
u'CACHED ARTICLE'

>>> cache_dict = {'/book/title': u'a new (cached) title', '/book/chapter[1]/article': u'CACHED ARTICLE'}
>>> x = CachedXmlDict(tree, cache_dict)
>>> x['/book[1]/title']
u'a new (cached) title'
>>> x['/book/title']
u'a new (cached) title'
>>> x['/book[1]/chapter[1]/article']
u'CACHED ARTICLE'
>>> x['/book/chapter[1]/article']
u'CACHED ARTICLE'
>>> x['/book[1]/chapter/article']
u'CACHED ARTICLE'
>>> x['/book/chapter/article']
u'CACHED ARTICLE'

>>> # TEST with many cache_dicts  =======================================================
>>> # This is typical usage with changes stored in info_dicts backed by a real (unchanged) xml file
>>> doc_info = {'/book/title': u'a fixed title', '/book/title/@lang': u'FR'}
>>> # TODO: maybe we want to copy all of the cached paths with a [1] is they don;t already exist? .. hopefully we don;t need this oberhead... TODO: review.
>>> # page_info = {'/book/chapter/pages': u'77'}
>>> page_info = {'/book/chapter[1]/pages': u'77'}
>>> article_info = {'/book/chapter[1]/article': u'Everything is Groovy Baby!'}     # WARNING: this will NOT be available wihtout the [1] unlike a non-cached xpath
>>> x = CachedXmlDict(tree, doc_info, page_info, article_info)
>>> x['/book/title']
u'a fixed title'
>>> x['/book/title/@lang']
u'FR'
>>> x['/book/chapter[1]/title'] # this one is read-thru, the rest are cached value.
u'In the Beginning'
>>> x['/book/chapter[1]/pages']
u'77'
>>> x['/book/chapter[1]/article']
u'Everything is Groovy Baby!'


>>> # Test errors -----------------------------------------------------------
>>> from gaia.error import GaiaCodingError
>>> try:
...     x['/book/title'] = 'SHOULD NOT BE ABLE TO SET: should be read-only'
... except GaiaCodingError, e:
...     print e
GaiaCodingError: CachedXmlDict.setitem() called, but this class is READ ONLY! 


>>> # REGRESSION TEST -----------------------------------------------------------
>>> # There was a problem with intermediate nodes matching too many when
>>> # using a [1] in an intermediate node (see textclip below)
>>> xml = """
... <chapter>
... <page>
... <article>
... <text>
...    <textclip>
...        <p>
...            <word pos=\"438,442,764,572\">article_1_word1</word>
...        </p>
...    </textclip>
...    <textclip>
...        <p>
...            <word pos=\"376,295,428,343\">article_2_word1</word>
...            <word pos=\"510,278,532,323\">article_2_word2</word>
...            <word pos=\"540,278,599,321\">article_2_word3</word>
...        </p>
...    </textclip>
... </text>
... </article>
... </page>
... </chapter>"""
>>> tree =  etree.parse(StringIO(xml))
>>> x = CachedXmlDict(tree)
>>> xpath = '/chapter/page[1]/article[1]/text/textclip[2]/p/word'
>>> words = x[xpath]
>>> len(words), words
(3, [u'article_2_word1', u'article_2_word2', u'article_2_word3'])

>>> # This test has 2 textclips
>>> xpath = '/chapter/page[1]/article[1]/text/textclip/p/word'
>>> words = x[xpath]
>>> len(words), words
(4, [u'article_1_word1', u'article_2_word1', u'article_2_word2', u'article_2_word3'])

>>> # REGRESSION TEST: textclip macthed all nodes instead of just the [1] node.
>>> xpath = '/chapter/page[1]/article[1]/text/textclip[1]/p/word'
>>> word = x[xpath]
>>> # Note; this returns a string not a list!...
>>> len(word), word
(15, u'article_1_word1')

'''
