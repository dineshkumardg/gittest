#!python -m doctest -v test_image_manifest.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.

import doctest
suite = doctest.DocFileSuite('test_image_manifest.py')

if __name__ == '__main__':
    doctest.testfile("test_image_manifest.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> from testing.gaia_test import GaiaTest
>>> from pprint import pprint
>>> from cengage.callisto.image_manifest import ImageManifest
>>> from gaia.asset.asset import Asset
>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir

>>> class Item:
...     def __init__(self, dom_name, assets):
...         self.dom_name = dom_name
...         self.assets = assets

>>> item_id = 'cho_meet_0001_0001_0001'

>>> content_set_name = 'cho'
>>> asset_fnames = ['cho_meet_0001_0001_0001_0001.jpg',
...                 'cho_meet_0001_0001_0001_0002.jpg',
...                 'cho_meet_0001_0001_0001_0003.jpg',
...                 'cho_meet_0001_0001_0001_0004.jpg',
...                 'cho_meet_0001_0001_0001_0005.jpg',
...                 'cho_meet_0001_0001_0001_0006.jpg',
...                 'cho_meet_0001_0001_0001_0007.jpg',
...                 'cho_meet_0001_0001_0001_0008.jpg',]

>>> item_dir = os.path.join(test_dir, item_id)
>>> os.mkdir(item_dir)
>>> _assets = []
>>> for fname in asset_fnames:
...     fpath = os.path.join(item_dir, fname)
...     asset = Asset(fpath, 'wb')
...     asset.close()
...     _assets.append(asset)

>>> item = Item(item_id, _assets)
>>> manifest = ImageManifest(item, content_set_name)

# Test the manifest
>>> test.tearDown()
>>> test.setUp()    # this annoying test re-uses the same directory :( TODO: rewrite!
>>> test_dir = test.test_dir

>>> xml = manifest.create()
>>> print xml
<?xml version="1.0" encoding="UTF-8"?>
<records>
<record href="cho_meet_0001_0001_0001_0001.jpg" ECOID="cho_meet_0001_0001_0001_0001" />
<record href="cho_meet_0001_0001_0001_0002.jpg" ECOID="cho_meet_0001_0001_0001_0002" />
<record href="cho_meet_0001_0001_0001_0003.jpg" ECOID="cho_meet_0001_0001_0001_0003" />
<record href="cho_meet_0001_0001_0001_0004.jpg" ECOID="cho_meet_0001_0001_0001_0004" />
<record href="cho_meet_0001_0001_0001_0005.jpg" ECOID="cho_meet_0001_0001_0001_0005" />
<record href="cho_meet_0001_0001_0001_0006.jpg" ECOID="cho_meet_0001_0001_0001_0006" />
<record href="cho_meet_0001_0001_0001_0007.jpg" ECOID="cho_meet_0001_0001_0001_0007" />
<record href="cho_meet_0001_0001_0001_0008.jpg" ECOID="cho_meet_0001_0001_0001_0008" />
</records>

>>> print manifest.fname
cho_image_manifest_cho_meet_0001_0001_0001.xml

>>> asset_fnames = ['cho_meet_0001_0001_0001_0001.xml',
...                 'cho_meet_0001_0001_0001_0001.mp3',
...                 'cho_meet_0001_0001_0001_0001.jpg',
...                 'cho_meet_0001_0001_0001_0002.jpg',
...                 'cho_meet_0001_0001_0001_0003.jpg',
...                 'cho_meet_0001_0001_0001_0004.jpg',
...                 'cho_meet_0001_0001_0001_0005.jpg',]

>>> item_dir = os.path.join(test_dir, item_id)
>>> os.mkdir(item_dir)
>>> _assets = []
>>> for fname in asset_fnames:
...     fpath = os.path.join(item_dir, fname)
...     asset = Asset(fpath, 'wb')
...     asset.close()
...     _assets.append(asset)

>>> item = Item(item_id, _assets)
>>> manifest = ImageManifest(item, content_set_name)
>>> xml = manifest.create()
>>> print xml
<?xml version="1.0" encoding="UTF-8"?>
<records>
<record href="cho_meet_0001_0001_0001_0001.jpg" ECOID="cho_meet_0001_0001_0001_0001" />
<record href="cho_meet_0001_0001_0001_0001.mp3" ECOID="cho_meet_0001_0001_0001_0001" />
<record href="cho_meet_0001_0001_0001_0002.jpg" ECOID="cho_meet_0001_0001_0001_0002" />
<record href="cho_meet_0001_0001_0001_0003.jpg" ECOID="cho_meet_0001_0001_0001_0003" />
<record href="cho_meet_0001_0001_0001_0004.jpg" ECOID="cho_meet_0001_0001_0001_0004" />
<record href="cho_meet_0001_0001_0001_0005.jpg" ECOID="cho_meet_0001_0001_0001_0005" />
</records>

>>> test.tearDown()

'''
