'''
Make sure the xml created by CreateChoXML is valid
'''
import doctest

suite = doctest.DocFileSuite('test_create_cho_xml.py')
if __name__ == '__main__':
    doctest.testfile("test_create_cho_xml.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)


'''
>>> import os
>>> from test_utils.create_cho_xml import CreateChoXML
>>> from gaia.error import GaiaErrors


>>> num_pages = 1
>>> img_file_ext = 'jpg'
>>> item_num = 1
>>> fpath_xsd = os.path.join(os.path.dirname(__file__), '../gaia/config/dtds/chatham_house.xsd')
>>> data_type = ''

>>> def create_cho_xml(item_type, item_name_stem, data_type=''):
...     try:
...         xml = CreateChoXML.create_xml_asset(num_pages, img_file_ext, item_type, item_num, item_name_stem, fpath_xsd, data_type)
...         print 'pass'
...     except GaiaErrors, e:
...         for error in e.errors:
...             print error

# Journal =============================================================
>>> item_type = 'iaxx'
>>> item_name_stem = 'cho_iaxx_2010_7771_001'
>>> create_cho_xml(item_type, item_name_stem)
pass

# Meeting =============================================================
>>> item_type = 'meet'
>>> item_name_stem = 'cho_meet_2010_7771_001'
>>> create_cho_xml(item_type, item_name_stem)
pass

# Meeting with audio =============================================================
>>> item_type = 'meet'
>>> item_name_stem = 'cho_meet_2010_7771_001'
>>> create_cho_xml(item_type, item_name_stem, data_type='Audio')
pass

# Conference Series =============================================================
>>> item_type = 'bcrc'
>>> item_name_stem = 'cho_bcrc_1938_0004_000'
>>> create_cho_xml(item_type, item_name_stem, data_type='')
pass

# Reports =============================================================
>>> item_type = 'rpax'
>>> item_name_stem = 'cho_rpax_2010_7771_001'
>>> create_cho_xml(item_type, item_name_stem)
pass

'''
