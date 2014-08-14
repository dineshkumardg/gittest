#!python -m doctest -v test_cho.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
#
# when updating doctest need to us py after something like the following:
# export PYTHONPATH=GIT_REPOS/gaia/src
# cd GIT_REPOS/gaia/src/project/cho/gaia_dom_adapter
#
import doctest
suite = doctest.DocFileSuite('test_cho_book.py')

if __name__ == '__main__':
    doctest.testfile("test_cho_book.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from pprint import pprint
>>> from gaia.asset.asset import Asset
>>> from project.cho.gaia_dom_adapter.cho import Cho
>>> import os
>>> import os.path
>>> from test_utils.create_cho_xml import CreateChoXML

# cho_book_1929_heald_000_0000 ====================================================================================

>>> fname_siax = os.path.join(os.path.dirname(__file__), '../test_samples/cho_book_1929_heald_000_0000.xml')
>>> asset = Asset(fname_siax)
>>> dom_adapter_siax = Cho(asset)
>>> print(dom_adapter_siax.document().dom_id)
cho_book_1929_heald_000_0000

# cho_book_1930_heald_000_0000 ====================================================================================

>>> fname_siax = os.path.join(os.path.dirname(__file__), '../test_samples/cho_book_1930_heald_000_0000.xml')
>>> asset = Asset(fname_siax)
>>> dom_adapter_siax = Cho(asset)
>>> print(dom_adapter_siax.document().dom_id)
cho_book_1930_heald_000_0000

'''
