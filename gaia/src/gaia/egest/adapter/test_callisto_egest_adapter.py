import doctest
suite = doctest.DocFileSuite('test_callisto_egest_adapter.py')

if __name__ == '__main__':
    doctest.testfile("test_callisto_egest_adapter.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> import glob  # allow wildcards for fpath
>>> from testing.gaia_test import GaiaTest
>>> from gaia.utils.import_class import import_class
>>> from gaia.log.log import Log
>>> from gaia.asset.asset import Asset
>>> from gaia.dom.model.item import Item
>>> from gaia.egest.adapter.callisto_egest_adapter import CallistoExportError
>>> from mock import patch
>>> import sys

>>> def create_item(test_dir, dom_id, dom_name, config):
...     ' only with 1 asset! '
...     assets = []
...     img_asset = Asset(os.path.join(test_dir, '%s.jpg' % dom_id), 'wb')
...     assets.append(img_asset)
...     audio_asset = Asset(os.path.join(test_dir, '%s.mp3' % dom_id), 'wb')
...     assets.append(audio_asset)
...     img_asset.close()
...     return Item(dom_id, dom_name, assets, config)

# ============================================================
# SETUP ======================================================
# ============================================================
>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config

>>> #config.imagebox = os.path.join(test_dir, 'imagebox')
>>> dom_id = 'cho_meet_1922_0010_000_0000'
>>> dom_name = dom_id
>>> config.working_dir = os.path.join(test_dir, 'egest_working_dir')
>>> config.inbox = os.path.join(test_dir, 'inbox')
>>> config.content_set_name = dom_id
>>> config.av_content_set_name = dom_id + '_AV'

>>> if os.path.exists(config.working_dir):
...     shutil.rmtree(config.working_dir)
>>> os.makedirs(config.working_dir)

>>> if os.path.exists(config.inbox):
...     shutil.rmtree(config.inbox)
>>> os.makedirs(config.inbox)

>>> if sys.platform.startswith("win"):
...     config.zip_fpath = r'c:\Program Files\7-zip\7z.exe'
... else:
...     config.zip_fpath= '/usr/bin/7z'

>>> adapter_class_name = 'gaia.egest.adapter.callisto_egest_adapter.CallistoEgestAdapter'
>>> logger_fname = Log.configure_logging('logger', config)
>>> adapter_params = {'server': '',  'uid': '',  'pwd': '',  'initial_dir': '', }
>>> callisto_egest_adapter = import_class(adapter_class_name)(config, **adapter_params)

# ============================================================
# TEST =======================================================
# ============================================================
>>> transfer_prep_dir = os.path.join(test_dir, 'transfer_prep_dir')
>>> item = create_item(config.inbox, dom_id, dom_name, config)
>>> item_index = '1'
>>> release_type = 'both'
>>> item_changes = {
...     'asset_id': { 'chunks': {u'1': u'HGQEKK343381964'}, 'document': u'BTHZMP611597712', 'pages': {u'24': u'DUVPUE496390333',} },
...     'file_size': { 'cho_meet_1922_0010_000_0000.jpg' : 0, 'cho_meet_1922_0010_000_0000.mp3': 0, },
...     'item_folder_name': 'cho_meet_1922_0010_000_0000',
...     }
>>> with patch('gaia.egest.adapter.egest_adapter.EgestAdapter._transfer'), patch('gaia.utils.work_area.WorkArea.remove'):
...     callisto_egest_adapter.egest(transfer_prep_dir, item, item_index, release_type, item_changes)

>>> # wait so glob has time to glob something! This is for anyone using Win7!
>>> import time
>>> time.sleep(2)

# ============================================================
# ASSERT =====================================================
# ============================================================
# check av + img 7z's in transfer prep dir # TODO: change to expect in out_dir
>>> sorted(glob.glob('%s/egest_working_dir/egest_callisto_*/%s*' % (test_dir, dom_id)))  # doctest:+ELLIPSIS
['...cho_meet_1922_0010_000_0000...7z', '...cho_meet_1922_0010_000_0000..._av.7z']

# TODO do more assertions - i.e. contents of 7z

>>> test.tearDown()

'''
