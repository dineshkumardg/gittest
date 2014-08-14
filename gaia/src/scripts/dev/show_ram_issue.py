'''
Show's that an xml tree is not released from ram when it goes out of scope & the OS does not get the ram back from the python vm
'''
import os
from lxml import etree
import sys
from StringIO import StringIO

xml_fpath = open(os.path.join(os.path.dirname(__file__), '../../project/cho/test_samples/cho_siax_1963_0000_000_0000.xml')).read()
parser = etree.XMLParser()
tree = etree.parse(StringIO(xml_fpath), parser)
print sys.getsizeof(tree)

# del tree

tree = None
print sys.getsizeof(tree)

import gc
gc.collect()
print sys.getsizeof(tree)

pass