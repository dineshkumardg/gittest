import doctest
suite = doctest.DocFileSuite('test_feed_file.py')

if __name__ == '__main__':
    doctest.testfile("test_feed_file.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> test = GaiaDjangoTest()
>>> test.setUp()
>>> import os
>>> #from test_utils.sorted_dict import sorted_dict
>>> from gaia.asset.asset import Asset
>>> from qa.models import Item
>>> from qa.models import FeedFile as FeedFileTable
>>> from project.cho.egest_adapter.feed.feed_file import FeedFile

>>> #
>>> # create a few items to go into the feed.
>>> item_names = []
>>> items = []
>>> for i in range(0, 3):
...     item_name = 'item_%d' % i
...     item_names.append(item_name)
...     item = Item(dom_name=item_name, dom_id=str(i))
...     item.save()
...     items.append(item)
>>> # create a few assets to replicate document instamces (for these items)
>>> assets = []
>>> for i in range(0, 5):
...     fname = os.path.join(test.test_dir, 'asset_%d.txt' % i)
...     asset = Asset(fname, 'w')
...     asset.write(str(i))
...     asset.close()
...     assets.append(asset)

>>> ff_dir = os.path.join(test.test_dir, 'output')
>>> os.mkdir(ff_dir)
>>> # test_fname indexed
>>> is_indexed = True
>>> group='functional_type_a'
>>> ff = FeedFile(assets, is_indexed, item_names, group)
>>> ff.write(ff_dir)
>>> # eg['PSM-CHOA-20130417-001.xml.gz']
>>> os.listdir(ff_dir) # doctest: +ELLIPSIS
['PSM-CHOA_..._00001.xml.gz']

>>> # test_fname NON-indexed
>>> is_indexed = False
>>> group='functional_type_a'
>>> ff = FeedFile(assets, is_indexed, item_names, group)
>>> ff.write(ff_dir)
>>> # eg ['NOINDEX-CHOA-20130417-002.xml.gz', 'PSM-CHOA-20130417-001.xml.gz']
>>> print sorted(os.listdir(ff_dir)) # doctest: +ELLIPSIS
['NOINDEX-CHOA_..._00002.xml.gz', 'PSM-CHOA_..._00001.xml.gz']

>>> test.tearDown()

'''
