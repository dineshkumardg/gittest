#!python -m doctest -v test_fix_form.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_fix_form.py')

if __name__ == '__main__':
    doctest.testfile("test_fix_form.py")

'''
>>> import json
>>> from pprint import pprint
>>> from qa.fix.fix_form import FixForm
>>> from gaia.dom.model.document import Document
>>> from gaia.dom.model.page import Page
>>> from gaia.dom.model.chunk import Chunk

>>> form = FixForm()
>>> form.add_doc_info(json.dumps(Document(7, '7', {'/doc/title': 'doc7', '/doc/issue': '777'}).info))
>>> form.add_page_info(json.dumps(Page(1, '1', {'/page[1]/title': 'page1', '/page[1]/number': 'p1'}).info))
>>> form.add_chunk_info(json.dumps(Chunk(1, '1', {'/article[1]/title': 'chunk1', '/article[1]/author': 'Anon1'}, page_ids=[1]).info))
>>> form.add_chunk_info(json.dumps(Chunk(2, '2', {'/article[2]/title': 'chunk2', '/article[2]/author': 'Anon2'}, page_ids=[1, 2]).info))
>>> print form.form('/go/here')
<form action="/go/here" method="post">
<table border="0">
<tr><td align="right"><span title="/doc/issue">issue:</span></td>
<td><span title="777">
<input name="new|D|7|/doc/issue" value="777" type="text" size="35">
<input name="old|D|7|/doc/issue" value="777" type="hidden">
</span></td></tr>
<tr><td align="right"><span title="/doc/title">title:</span></td>
<td><span title="doc7">
<input name="new|D|7|/doc/title" value="doc7" type="text" size="35">
<input name="old|D|7|/doc/title" value="doc7" type="hidden">
</span></td></tr>
</table>
<table border="0">
<tr><td align="right"><span title="/page[1]/number">number:</span></td>
<td><span title="p1">
<input name="new|P|1|/page[1]/number" value="p1" type="text" size="35">
<input name="old|P|1|/page[1]/number" value="p1" type="hidden">
</span></td></tr>
<tr><td align="right"><span title="/page[1]/title">title:</span></td>
<td><span title="page1">
<input name="new|P|1|/page[1]/title" value="page1" type="text" size="35">
<input name="old|P|1|/page[1]/title" value="page1" type="hidden">
</span></td></tr>
</table>
<table border="0">
<tr><td align="right"><span title="/article[1]/author">author:</span></td>
<td><span title="Anon1">
<input name="new|C|1|/article[1]/author" value="Anon1" type="text" size="35">
<input name="old|C|1|/article[1]/author" value="Anon1" type="hidden">
</span></td></tr>
<tr><td align="right"><span title="/article[1]/title">title:</span></td>
<td><span title="chunk1">
<input name="new|C|1|/article[1]/title" value="chunk1" type="text" size="35">
<input name="old|C|1|/article[1]/title" value="chunk1" type="hidden">
</span></td></tr>
</table>
<table border="0">
<tr><td align="right"><span title="/article[2]/author">author:</span></td>
<td><span title="Anon2">
<input name="new|C|2|/article[2]/author" value="Anon2" type="text" size="35">
<input name="old|C|2|/article[2]/author" value="Anon2" type="hidden">
</span></td></tr>
<tr><td align="right"><span title="/article[2]/title">title:</span></td>
<td><span title="chunk2">
<input name="new|C|2|/article[2]/title" value="chunk2" type="text" size="35">
<input name="old|C|2|/article[2]/title" value="chunk2" type="hidden">
</span></td></tr>
</table>
<table width="100%">
<tr><td align="center"><input style="padding:7px; margin:3px; background-color: black; color: white; font-size:small" type="submit"  value="  fix  " /></td></tr></table></form>
<BLANKLINE>


>>> # A: Test some doc_info, no page_info, some chunk_info ---------------------
>>> form_data = {\
... u'old|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'smelly', 
... u'new|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'sweet', 
... u'old|P|6|/chapter/page[6]/article/articleInfo/pageRange': u'1-30',
... u'new|P|6|/chapter/page[6]/article/articleInfo/pageRange': u'1-30',
... u'old|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 2',
... u'new|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 2 HAS BEEN FIXED',
... u'old|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-99',
... u'new|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-31',
... }
>>> doc_infos, page_infos, chunk_infos = FixForm.parse(form_data)
>>> pprint(doc_infos)
{u'cho_meet_2010_7771_002_0001': {u'/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-31',
                                  u'/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 2 HAS BEEN FIXED'}}

>>> page_infos
{}

>>> chunk_infos
{u'1': {u'/chapter/page[1]/article/text/textclip/footnote/word': u'sweet'}}

>>> # B: Test no doc_info, some page_info, some chunk_info ---------------------
>>> form_data = {\
... u'old|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'smelly', 
... u'new|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'sweet', 
... u'old|C|2|/chapter/page[2]/article/text/textclip/footnote/word': u'rancid', 
... u'new|C|2|/chapter/page[2]/article/text/textclip/footnote/word': u'cheesy', 
... u'old|P|6|/chapter/page[6]/article/articleInfo/pageRange': u'1-30',
... u'new|P|6|/chapter/page[6]/article/articleInfo/pageRange': u'6-66',
... u'old|P|7|/chapter/page[7]/article/articleInfo/pageRange': u'1-11',
... u'new|P|7|/chapter/page[7]/article/articleInfo/pageRange': u'7-77',
... u'old|P|8|/chapter/page[8]/article/articleInfo/pageRange': u'1-11',
... u'new|P|8|/chapter/page[8]/article/articleInfo/pageRange': u'8-88',
... u'old|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 2',
... u'new|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/titleGroup/fullTitle': u'fullTitle for 2',
... u'old|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-31',
... u'new|D|cho_meet_2010_7771_002_0001|/chapter/citation/meeting/pubDate/pubDateEnd': u'1963-01-31',
... }
>>> doc_infos, page_infos, chunk_infos = FixForm.parse(form_data)
>>> pprint(doc_infos)
{}

>>> pprint(page_infos)
{u'6': {u'/chapter/page[6]/article/articleInfo/pageRange': u'6-66'},
 u'7': {u'/chapter/page[7]/article/articleInfo/pageRange': u'7-77'},
 u'8': {u'/chapter/page[8]/article/articleInfo/pageRange': u'8-88'}}

>>> pprint(chunk_infos)
{u'1': {u'/chapter/page[1]/article/text/textclip/footnote/word': u'sweet'},
 u'2': {u'/chapter/page[2]/article/text/textclip/footnote/word': u'cheesy'}}

>>> # C: Test Unicode/Entity Refs ----------------------------
>>> form_data = {\
... u'old|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in unicode abc', 
... u'new|C|1|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in unicode \ufed5bc', 
... u'old|C|2|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in numeric char ref \ufed5bc', 
... u'new|C|2|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in numeric char ref &#65237;bc', 
... u'old|C|3|/chapter/page[2]/article/text/textclip/footnote/word': u"an entity code \' (quote mark)", 
... u'new|C|3|/chapter/page[2]/article/text/textclip/footnote/word': u'an entity code &quot; (quote mark)',
... u'old|C|4|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in unicode \ufed5bc NOT being changed', 
... u'new|C|4|/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in unicode \ufed5bc NOT being changed', 
... }
>>> doc_infos, page_infos, chunk_infos = FixForm.parse(form_data)
>>> # Note that unicode characters are translated to Xml Numeric Character Entity Refs (in the first chunk).
>>> pprint(chunk_infos)
{u'1': {u'/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in unicode &#65237;bc'},
 u'2': {u'/chapter/page[1]/article/text/textclip/footnote/word': u'An Arabic Character in numeric char ref &#65237;bc'},
 u'3': {u'/chapter/page[2]/article/text/textclip/footnote/word': u'an entity code &quot; (quote mark)'}}

'''
