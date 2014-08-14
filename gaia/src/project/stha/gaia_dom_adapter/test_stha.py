import doctest
suite = doctest.DocFileSuite('test_stha.py')

if __name__ == '__main__':
    doctest.testfile("test_stha.py", optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.stha.gaia_dom_adapter.stha import Stha
>>> import os
>>> import os.path
>>> try:
...    here = os.path.dirname(__file__)
... except NameError, e:
...    here = os.getcwd()
>>> fname = os.path.join(here, '../test_samples/STHA-1827-0204.xml')
>>> asset = Asset(fname)
>>> dom_adapter = Stha(asset)

# Test the DOCUMENT ---------------------------------------------------

>>> print(dom_adapter.document().dom_id)
STHA-1827-0204

>>> print(dom_adapter.document().dom_name)
STHA-1827-0204

>>> pprint(dom_adapter.document().info)
{'/GALENP/Newspaper/issue/copyright': u'Copyright 1827, The Sunday Times',
 '/GALENP/Newspaper/issue/da': u'February 04, 1827',
 '/GALENP/Newspaper/issue/dw': u'Sunday',
 '/GALENP/Newspaper/issue/id': u'STHA-1827-0204',
 '/GALENP/Newspaper/issue/imdim': u'5104,7175',
 '/GALENP/Newspaper/issue/ip': u'4',
 '/GALENP/Newspaper/issue/is': u'224',
 '/GALENP/Newspaper/issue/metadatainfo/newspaperID': u'STHA',
 '/GALENP/Newspaper/issue/pf': u'18270204',
 '_dom_id': u'STHA-1827-0204',
 '_dom_name': u'STHA-1827-0204'}

>>> # Hmm.. not sure about dom_id!.... TODO
>>> for page in dom_adapter.pages():
...     print page.dom_id, page.dom_name, sorted(page.info.items())
STHA-1827-0204-0001 1 [('/GALENP/Newspaper/issue/page[1]/pa', u'1'), ('_asset_fname', u'STHA-1827-0204-0001.jpg'), ('_dom_id', u'STHA-1827-0204-0001'), ('_dom_name', u'1')]
STHA-1827-0204-0002 2 [('/GALENP/Newspaper/issue/page[2]/pa', u'2'), ('_asset_fname', u'STHA-1827-0204-0002.jpg'), ('_dom_id', u'STHA-1827-0204-0002'), ('_dom_name', u'2')]
STHA-1827-0204-0003 3 [('/GALENP/Newspaper/issue/page[3]/pa', u'3'), ('_asset_fname', u'STHA-1827-0204-0003.jpg'), ('_dom_id', u'STHA-1827-0204-0003'), ('_dom_name', u'3')]
STHA-1827-0204-0004 4 [('/GALENP/Newspaper/issue/page[4]/pa', u'4'), ('_asset_fname', u'STHA-1827-0204-0004.jpg'), ('_dom_id', u'STHA-1827-0204-0004'), ('_dom_name', u'4')]

>>> # Test CHUNKS ---------------------------------------------------
>>> chunks = dom_adapter.chunks()
>>> print len(chunks)
47

>>> def print_chunk(chunk):
...     print "CHUNK ID:", chunk.dom_id
...     print "page_ids:", chunk.page_ids
...     print "clip_ids:", chunk.clip_ids
...     info = chunk.info
...     for key in sorted(info.keys()):
...         print " ", key, ":", info[key]
>>> print_chunk(chunks[0])
CHUNK ID: STHA-1827-0204-0001-001
page_ids: [u'STHA-1827-0204-0001']
clip_ids: [u'STHA-1827-0204-0001-001-001', u'STHA-1827-0204-0001-001-002', u'STHA-1827-0204-0001-001-003']
  /GALENP/Newspaper/issue/page[1]/article[1]/ct : Classified Advertising
  /GALENP/Newspaper/issue/page[1]/article[1]/id : STHA-1827-0204-0001-001
  /GALENP/Newspaper/issue/page[1]/article[1]/pc : 1
  /GALENP/Newspaper/issue/page[1]/article[1]/sc : A
  /GALENP/Newspaper/issue/page[1]/article[1]/ti : Multiple Classified Advertising Items
  _clip_ids : [u'STHA-1827-0204-0001-001-001', u'STHA-1827-0204-0001-001-002', u'STHA-1827-0204-0001-001-003']
  _dom_id : STHA-1827-0204-0001-001
  _dom_name : Multiple Classified Advertising Items
  _is_binary : False
  _page_ids : [u'STHA-1827-0204-0001']

>>> print_chunk(chunks[5])
CHUNK ID: STHA-1827-0204-0001-006
page_ids: [u'STHA-1827-0204-0001']
clip_ids: [u'STHA-1827-0204-0001-006-001', u'STHA-1827-0204-0001-006-002', u'STHA-1827-0204-0001-006-003', u'STHA-1827-0204-0001-006-004', u'STHA-1827-0204-0001-006-005', u'STHA-1827-0204-0001-006-006']
  /GALENP/Newspaper/issue/page[1]/article[6]/ct : News
  /GALENP/Newspaper/issue/page[1]/article[6]/id : STHA-1827-0204-0001-006
  /GALENP/Newspaper/issue/page[1]/article[6]/pc : 1
  /GALENP/Newspaper/issue/page[1]/article[6]/sc : E
  /GALENP/Newspaper/issue/page[1]/article[6]/ti : War in Portugal
  _clip_ids : [u'STHA-1827-0204-0001-006-001', u'STHA-1827-0204-0001-006-002', u'STHA-1827-0204-0001-006-003', u'STHA-1827-0204-0001-006-004', u'STHA-1827-0204-0001-006-005', u'STHA-1827-0204-0001-006-006']
  _dom_id : STHA-1827-0204-0001-006
  _dom_name : War in Portugal
  _is_binary : False
  _page_ids : [u'STHA-1827-0204-0001']

>>> print dom_adapter.asset_fnames()
[u'STHA-1827-0204-0001.jpg', u'STHA-1827-0204-0002.jpg', u'STHA-1827-0204-0003.jpg', u'STHA-1827-0204-0004.jpg']

>>> print(dom_adapter.clips())
[]

>>> print(dom_adapter.links())
[]

>>> print(dom_adapter.links(internal=False))
[]

>>> #dom_adapter.write(',journal.xml')
>>> # TODO
'''
