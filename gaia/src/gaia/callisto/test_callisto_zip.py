# Note: use "<BLANKLINE>" to expect an empty line in the output.

import doctest
suite = doctest.DocFileSuite('test_callisto_zip.py')

if __name__ == '__main__':
    doctest.testfile("test_callisto_zip.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> import sys
>>> from pprint import pprint
>>> from testing.gaia_test import GaiaTest
>>> from gaia.utils.try_cmd import try_cmd
>>> from gaia.utils.work_area import WorkArea
>>> from gaia.asset.asset import Asset
>>> from gaia.dom.model.item import Item
>>> from gaia.callisto.callisto_zip import CallistoZip
>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir

>>> # Set up
>>> item_name = 'cho_meet_0001_0001_0001'
>>> asset_fpaths = [ os.path.join(test_dir, 'cho_0001_0001_0001_0001.xml'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0001.mp3'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0001.jpg'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0002.jpg'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0003.jpg'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0004.jpg'),
...                  os.path.join(test_dir, 'cho_0001_0001_0001_0005.jpg'), ]
>>> assets = []
>>> for fpath in asset_fpaths:
...     asset = Asset(fpath, 'wb')
...     asset.close()
...     assets.append(asset)
>>> num_image_assets = 5 # 5 jpg files
>>> num_av_assets = 1 # 1 mp3 file

>>> if sys.platform.startswith("win"):
...     _zip_fpath = r'c:\Program Files\7-zip\7z.exe'
... else:
...     _zip_fpath = '/usr/bin/7z'

>>> class Config:
...     content_set_name = 'cho'
...     av_content_set_name = 'AV_CONTENT_SET'
...     zip_fpath = _zip_fpath
...     working_dir = test_dir

>>> config = Config()

>>> # Test
>>> item = Item(dom_id='dom_id', dom_name=item_name, assets=assets, config=config)

>>> work_area = WorkArea(config)
>>> work_dir = work_area.path
>>> callisto_zip = CallistoZip(config)
>>> callisto_zip.create(item, work_dir)

>>> # Make sure ther are 2 zips in the work_dir: one for audio, the other for images
>>> fnames = sorted(os.listdir(work_dir))  # with v. basic sorting!
>>> len(fnames)
2
>>> for zip_fname in fnames:
...     zip_fname.endswith('.7z')
...     zip_fname.startswith(item_name)
...     zip_fname.endswith('_av.7z')
True
True
False
True
True
True

>>> # Make sure that both zips have the right contents
>>> def fpaths_in_zip(zip_fpath):
...     unpack_dir = os.path.join(test_dir, 'unpack_'+os.path.basename(zip_fpath))
...     cmd = [_zip_fpath, 'x', zip_fpath, '-o%s' % unpack_dir]
...     out = try_cmd(*cmd)
... 
...     fpaths = []
...     for root, dirs, fnames in os.walk(unpack_dir):
...         for fname in fnames:
...             fpath = os.path.join(root, fname)
...             fpaths.append(os.path.relpath(fpath, unpack_dir))
...     return fpaths

>>> out_zip_fpaths = work_area.ls()
>>> print len(out_zip_fpaths)
2

>>> if out_zip_fpaths[0].endswith('_av.7z'):
...     av_zip_fpath, zip_fpath = out_zip_fpaths
... else:
...     zip_fpath, av_zip_fpath = out_zip_fpaths

>>> num_manifests = 2 # a delivery and an image manifest
>>> #
>>> # First, check the NON av zip ----------------------------------
>>> #
>>> # check the number of files
>>> fpaths = fpaths_in_zip(zip_fpath)
>>> num_assets = num_image_assets + num_manifests
>>> print len(fpaths) == num_assets
True

>>> # check the file paths (structure is important for Callisto)
>>> # WARNING: We've elided the slash to allow this to run on windwont :(
>>> # WARNING: This pattern is too greedy, so matches things that it shouldn't match 
>>> # (however, the len() test above helps get around this)
>>> print '\n'.join(sorted(fpaths)) #doctest:+ELLIPSIS
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_delivery_manifest_cho_meet_0001_0001_0001..._..._..._..._..._..._....txt
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0001.jpg
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0002.jpg
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0003.jpg
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0004.jpg
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0005.jpg
cho_meet_0001_0001_0001_..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_image_manifest_cho_meet_0001_0001_0001.xml

# This is what the real structure looks like for reference (inlcudes now timestamps)
# 2 manifesst plus all the binary assets (no _item_ xml file, just one manifest.xml file)
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_delivery_manifest_cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903.txt
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0001.jpg
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0001.mp3
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0002.jpg
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0003.jpg
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0004.jpg
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_0001_0001_0001_0005.jpg
#cho_meet_0001_0001_0001_2012_08_23_16_11_25_111903/cho_meet_0001_0001_0001/cho_image_manifest_cho_meet_0001_0001_0001.xml

>>> # Second, check the AV zip ----------------------------------
>>> fpaths = fpaths_in_zip(av_zip_fpath)
>>> # check the number of files
>>> num_assets = num_av_assets + num_manifests
>>> print len(fpaths) == num_assets
True

>>> # check the file paths (structure is important for Callisto)
>>> # WARNING: We've elided the slash to allow this to run on windwont :(
>>> # WARNING: This pattern is too greedy, so matches things that it shouldn't match 
>>> # (however, the len() test above helps get around this)
>>> print '\n'.join(sorted(fpaths)) #doctest:+ELLIPSIS
cho_meet_0001_0001_0001_..._..._..._..._..._..._..._...AV_CONTENT_SET_delivery_manifest_cho_meet_0001_0001_0001..._..._..._..._..._..._..._av.txt
cho_meet_0001_0001_0001_..._..._..._..._..._..._..._...cho_meet_0001_0001_0001...AV_CONTENT_SET_image_manifest_cho_meet_0001_0001_0001.xml
cho_meet_0001_0001_0001_..._..._..._..._..._..._..._...cho_meet_0001_0001_0001...cho_0001_0001_0001_0001.mp3

>>> test.tearDown()

'''
