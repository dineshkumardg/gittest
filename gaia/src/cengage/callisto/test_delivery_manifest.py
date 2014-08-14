#!python -m doctest -v test_delivery_manifest.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.

import doctest
suite = doctest.DocFileSuite('test_delivery_manifest.py')

if __name__ == '__main__':
    doctest.testfile("test_delivery_manifest.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> from pprint import pprint
>>> from cengage.callisto.delivery_manifest import DeliveryManifest
>>> from testing.gaia_test import GaiaTest
>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir

# Set it up
>>> package_name = 'cho_iaax_0001_0001_1_2_2_3_4_2012'
>>> item_id = 'cho_meet_0001_0001_0001'
>>> content_set_name = 'CSN'
>>> os.mkdir(os.path.join(test_dir, item_id))
>>> package_dir = test_dir

>>> manifest = DeliveryManifest(package_name, package_dir, content_set_name)

# Test the manifest

>>> content = manifest.create()
>>> print content
cho_meet_0001_0001_0001, CSN
<BLANKLINE>

>>> print manifest.fname
CSN_delivery_manifest_cho_iaax_0001_0001_1_2_2_3_4_2012.txt

>>> test.tearDown()

'''
