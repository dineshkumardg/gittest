import os
import unittest
import datetime
from mock import MagicMock, call, create_autospec, patch
from testing.gaia_test import GaiaTest
from gaia.provider.provider import Provider
from gaia.gtp.gtp_status import GtpStatus
from gaia.utils.lock import LockError
from gaia.provider.provider_error import TransferAbort, TransferError, ProviderError
from gaia.utils.ftp import Ftp, FtpError
from gaia.ingest.inbox import Inbox
from gaia.gtp.gtp_site import GtpSite
from gaia.gtp.manifest import Manifest

class FakeConfig:
    def __init__(self, project_code, working_dir):
        self.project_code = project_code
        self.working_dir = working_dir
    
class TestProvider(GaiaTest):

    maxDiff = None
    
    def setUp(self):
        GaiaTest.setUp(self)
        self.project_code = 'CODE'
        self.working_dir = self.test_dir
        self.config = FakeConfig(self.project_code, self.working_dir)

    def test__init__(self):
        
        class FakeTransferAgent:
            pass
            
        class FakeConfig:
            project_code = 'PROJECT_CODE'
            
        class TestableProvider(Provider):
            def _empty_file(self):
                self._empty_file_called = True
        
        name = 'Provider Name'
        transfer_agent = FakeTransferAgent()
        config = FakeConfig()
        p = TestableProvider(name, transfer_agent, config)
        self.assertTrue(p._empty_file_called)
        
    def test_list_new_items_ALL_READY(self):
        # Setup
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        name = 'PROVIDER_NAME'
        ta_group_dirs = ['group_dir_1', 'group_dir_2',]
        ta_item_dirs  = ['item_dir_a', 'item_dir_b', 'item_dir_c',]
        ta_fnames     = ['item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg', GtpStatus.READY_FNAME,]
        
        ta_ls_ordered_call_returns = [ ta_group_dirs,
                                       ta_item_dirs,
                                       ta_fnames,
                                       ta_fnames,
                                       ta_fnames,
                                       ta_item_dirs,
                                       ta_fnames,
                                       ta_fnames,
                                       ta_fnames,
                                       ta_fnames,]
        
        def ta_ls_return(*args):
            return ta_ls_ordered_call_returns.pop(0)
        
        mock_ta.ls.side_effect = ta_ls_return

        # Expectations
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_ta_ls_calls = [call(expected_items_dir),
                                call(expected_items_dir + '/group_dir_1'),
                                call(expected_items_dir + '/group_dir_1/item_dir_a'),
                                call(expected_items_dir + '/group_dir_1/item_dir_b'),
                                call(expected_items_dir + '/group_dir_1/item_dir_c'),
                                call(expected_items_dir + '/group_dir_2'),
                                call(expected_items_dir + '/group_dir_2/item_dir_a'),
                                call(expected_items_dir + '/group_dir_2/item_dir_b'),
                                call(expected_items_dir + '/group_dir_2/item_dir_c'),]
        
        expected_ta_cd_calls = [call(expected_items_dir + '/group_dir_1/item_dir_a'),
                                call(expected_items_dir + '/group_dir_1/item_dir_b'),
                                call(expected_items_dir + '/group_dir_1/item_dir_c'),
                                call(expected_items_dir + '/group_dir_2/item_dir_a'),
                                call(expected_items_dir + '/group_dir_2/item_dir_b'),
                                call(expected_items_dir + '/group_dir_2/item_dir_c'),]
        
        expected_empty_fpath = os.path.join(self.working_dir, 'empty_file.txt')
        expected_ta_put_call_arg = call(expected_empty_fpath, remote_fname='_status_PROCESSING.txt')

        expected_new_items = [('group_dir_1', 'item_dir_a'),
                              ('group_dir_1', 'item_dir_b'),
                              ('group_dir_1', 'item_dir_c'),
                              ('group_dir_2', 'item_dir_a'),
                              ('group_dir_2', 'item_dir_b'),
                              ('group_dir_2', 'item_dir_c'),]  
        
        # Test
        config = self.config
        p = Provider(name, mock_ta, config)
        new_items = p.list_new_items()

        # Assertions        
        self.assertListEqual(sorted(expected_ta_ls_calls), sorted(mock_ta.ls.call_args_list))
        self.assertListEqual(sorted(expected_ta_cd_calls), sorted(mock_ta.cd.call_args_list))
        self.assertEqual(len(expected_new_items), mock_ta.put.call_count)
        self.assertEqual(expected_ta_put_call_arg, mock_ta.put.call_args)
        self.assertEqual(len(expected_new_items), len(new_items))
        self.assertListEqual(sorted(expected_new_items), sorted(new_items))
        
    def test_list_new_items_MIXED_ITEM_STATE(self):
        # Setup
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        provider_name = 'PROVIDER'
        ta_group_dirs = ['group_dir_1', 'group_dir_2',]
        ta_item_dirs  = ['item_dir_a', 'item_dir_b', 'item_dir_c',]
        ta_fnames     = ['item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']
        
        ta_ls_ordered_call_returns = [ ta_group_dirs,
                                       ta_item_dirs,
                                       ['item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg', GtpStatus.READY_FNAME,], # This is the only one that should be returned!!
                                       ta_fnames,
                                       ta_fnames,
                                       ta_item_dirs,
                                       ['item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg', GtpStatus.PROCESSING_FNAME,],
                                       ta_fnames,
                                       ta_fnames,
                                       ta_fnames,]
        
        def ta_ls_return(*args):
            return ta_ls_ordered_call_returns.pop(0)
        
        mock_ta.ls.side_effect = ta_ls_return

        # Expectations        
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_ta_ls_calls = [call(expected_items_dir),
                                call(expected_items_dir + '/group_dir_1'),
                                call(expected_items_dir + '/group_dir_1/item_dir_a'),
                                call(expected_items_dir + '/group_dir_1/item_dir_b'),
                                call(expected_items_dir + '/group_dir_1/item_dir_c'),
                                call(expected_items_dir + '/group_dir_2'),
                                call(expected_items_dir + '/group_dir_2/item_dir_a'),
                                call(expected_items_dir + '/group_dir_2/item_dir_b'),
                                call(expected_items_dir + '/group_dir_2/item_dir_c'),]

        
        expected_ta_cd_calls = [call(expected_items_dir + '/group_dir_1/item_dir_a'),]
        expected_empty_fpath = os.path.join(self.working_dir, 'empty_file.txt')
        expected_ta_put_call_arg = call(expected_empty_fpath, remote_fname='_status_PROCESSING.txt')
        expected_num_items = 1
        expected_new_items = [('group_dir_1', 'item_dir_a'),]

        # Test        
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_items = p.list_new_items()

        # Assertions
        self.assertListEqual(sorted(expected_ta_ls_calls), sorted(mock_ta.ls.call_args_list))
        self.assertListEqual(sorted(expected_ta_cd_calls), sorted(mock_ta.cd.call_args_list))
        self.assertEqual(expected_num_items, mock_ta.put.call_count)
        self.assertEqual(expected_ta_put_call_arg, mock_ta.put.call_args)
        self.assertEqual(expected_num_items, len(new_items))
        self.assertListEqual(sorted(expected_new_items), sorted(new_items))
        
    def test_get_item_NO_MANIFEST(self):
        # Setup
        provider_name = 'PROVIDER'
        group_name = 'group_name'
        item_name = 'item'
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_ta.ls.return_value = ['item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
            
        # Expectations        
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_error = 'MissingManifestError: No manifest file for item "%s" in group "%s"' % (item_name, group_name)
        expected_item_dir = '%s/%s/%s' % (expected_items_dir, group_name, item_name)
        
        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_assets, errors = p.get_item(group_name, item_name, mock_inbox)
        
        # Assertions
        mock_inbox.lock.assert_called_once_with(item_name)
        mock_ta.cd.assert_called_once_with(expected_item_dir)
        mock_ta.ls.assert_called_once_with()
        self.assertEqual(0, len(new_assets))
        self.assertEqual(1, len(errors))
        self.assertEqual(expected_error, str(errors[0]))
        
    def test_get_item(self):
        # Set up
        provider_name = 'PROVIDER'
        item_name = 'item_name'
        group_name = 'group_name'
        item_files = [Manifest.fname, 'item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']

        class FakeManifest:
            def __init__(self, fpath):
                self._fpath = fpath
                
            def checksums(self):
                _checksums = {}
                for f in item_files[1:]: # We don't want the manifest file
                    _checksums[f] = 'checksum_%s' % f
                
                return _checksums
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True) # Create transfer agent object with the spec of Ftp
        mock_ta.ls.return_value = item_files
        
        
        inbox_new_asset_ordered_returns = [ MagicMock(name='asset_' + item_files[0]),
                                            MagicMock(name='asset_' + item_files[1]),
                                            MagicMock(name='asset_' + item_files[2]),
                                            MagicMock(name='asset_' + item_files[3]),
                                            MagicMock(name='asset_' + item_files[4]), ]
        
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        mock_inbox.new_asset.side_effect = inbox_new_asset_ordered_returns

        # Expectations
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_ta_method_calls = [call.cd(expected_items_dir + '/group_name/item_name'),
                                    call.ls(),
                                    call.copy('manifest.md5', inbox_new_asset_ordered_returns[0]),
                                    call.copy('item.xml', inbox_new_asset_ordered_returns[1], 'checksum_item.xml'),
                                    call.copy('image_1.jpg', inbox_new_asset_ordered_returns[4], 'checksum_image_1.jpg'),
                                    call.copy('image_2.jpg', inbox_new_asset_ordered_returns[2], 'checksum_image_2.jpg'),
                                    call.copy('image_3.jpg', inbox_new_asset_ordered_returns[3], 'checksum_image_3.jpg'),]
        
        expected_ordered_inbox_method_calls = [call.lock(item_name),
                                               call.new_asset('manifest.md5', item_name),
                                               #call.delete_asset(inbox_new_asset_ordered_returns[0], item_name),  # we keep the manifest file now!
                                               call.new_asset('item.xml', item_name),
                                               call.lock_renew(item_name),
                                               call.new_asset('image_2.jpg', item_name),
                                               call.lock_renew(item_name),
                                               call.new_asset('image_3.jpg', item_name),
                                               call.lock_renew(item_name),
                                               call.new_asset('image_1.jpg', item_name),
                                               call.lock_renew(item_name),
                                               call.unlock(item_name)]
        
        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_assets, errors = p.get_item(group_name, item_name, mock_inbox, _manifest_class=FakeManifest)

        # Assertions
        mock_inbox.lock.assert_called_once_with(item_name)
        mock_ta.assert_has_calls(expected_ta_method_calls, any_order=True)
        self.assertEqual(expected_ordered_inbox_method_calls, mock_inbox.method_calls)
        self.assertEqual(0, len(errors))
        self.assertListEqual(sorted(inbox_new_asset_ordered_returns[1:]), sorted(new_assets))
        
    def test_get_item_CANNOT_LOCK_ITEM(self):
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        mock_inbox.lock.side_effect = LockError('Euston, we have a problem!')
        
        # Expectations
        expected_inbox_calls = [call.lock_item(item_name),]
        
        # Test + Assertions
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        
        self.assertRaises(TransferAbort, p.get_item, group_name, item_name, mock_inbox)
        self.assertEqual(0, len(mock_ta.method_calls))
        self.assertEqual(expected_inbox_calls, mock_inbox.lock.call_args_list)

    def test_get_item_LOCK_RENEW_FAILS_AFTER_FIRST_FILE_COPY(self): # TODO: NEEDS REVIEW - WHAT SHOULD THE EXPECTATION BE?
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        item_files = [Manifest.fname, 'item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_ta.ls.return_value = item_files
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        mock_inbox.lock_renew.side_effect = LockError('Euston, we have a lock_renew problem!')
        

        class FakeManifest:
            def __init__(self, fpath):
                self._fpath = fpath
                
            def checksums(self):
                _checksums = {}
                for f in item_files[1:]: # We don't want the manifest file
                    _checksums[f] = 'checksum_%s' % f
                
                return _checksums

        # Test + Assertions
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        
        self.assertRaises(TransferAbort, p.get_item, group_name, item_name, mock_inbox, _manifest_class=FakeManifest)

    def test_get_item_TRANSFER_AGENT_LS_FAILS(self):
        # Setup
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        
        # Expectations
        expected_error = FtpError('Euston, we have another problem!')
        mock_ta.ls.side_effect = expected_error
        
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_ta_calls = [call.cd('%s/%s/%s' % (expected_items_dir, group_name, item_name)),
                             call.ls(),]

        expected_inbox_calls = [call.lock_item(item_name),]
        
        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_assets, errors = p.get_item(group_name, item_name, mock_inbox)

        # Assertions
        self.assertListEqual(expected_ta_calls, mock_ta.method_calls)
        self.assertEqual(0, len(new_assets))
        self.assertEqual(expected_inbox_calls, mock_inbox.lock.call_args_list)
        self.assertEqual(1, len(errors))
        self.assertEqual(str(expected_error), str(errors[0]))
        
    def test_get_item_TRANSFER_AGENT_COPY_FAILS_TRANFERRING_MANIFEST(self):
        # Setup
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        
        mock_ta.ls.return_value = [Manifest.fname, 'item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']
        copy_error = FtpError('Manifest copy error')
        mock_ta.copy.side_effect = copy_error
        asset = MagicMock(name='Manifest asset')
        mock_inbox.new_asset.return_value = asset
        
        # Expectations
        expected_items_dir = GtpSite(self.project_code).items_dir
        
        expected_ta_calls = [call.cd('%s/%s/%s' % (expected_items_dir, group_name, item_name)),
                             call.ls(),
                             call.copy(Manifest.fname, asset),]
        
        expected_inbox_calls = [call.lock(item_name),
                                call.new_asset('manifest.md5', item_name),
                                call.unlock(item_name),]
        
        expected_errors = [copy_error,]

        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_assets, errors = p.get_item(group_name, item_name, mock_inbox)
        
        # Assertions
        self.assertListEqual(expected_ta_calls, mock_ta.method_calls)
        self.assertListEqual(expected_inbox_calls, mock_inbox.method_calls)
        self.assertEqual(0, len(new_assets))
        self.assertListEqual(expected_errors, errors)
        
    def test_get_item_TRANSFER_AGENT_COPY_FAILS_TRANFERRING_LAST_NON_MANIFEST_ASSET(self):
        # Setup
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'

        manifest_asset = MagicMock()
        item_xml_asset = MagicMock()
        image_1_asset = MagicMock()
        image_2_asset = MagicMock()
        copy_error_asset = MagicMock()
        
        copy_error_fname = 'COPY_ERROR.jpg'
        copy_error = FtpError('Asset copy error')
        
        # This structure represents the item files returned from transfer_agent.ls()
        # for the item and the assets returned from the inbox when inbox.new_asset
        # is called for the item file name...
        items = { Manifest.fname: manifest_asset,
                  'item.xml': item_xml_asset,
                  'image_1.jpg': image_1_asset,
                  'image_2.jpg': image_2_asset,
                  copy_error_fname: copy_error_asset, }
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_ta.ls.return_value = items.keys()

        mock_inbox = create_autospec(Inbox, spec_set=True, instance=True)
        
        def new_asset_side_effect(*args):
            return items[args[0]]
        
        mock_inbox.new_asset.side_effect = new_asset_side_effect

        class FakeManifest:
            def __init__(self, fpath):
                self._fpath = fpath
                
            def checksums(self):
                _checksums = {}
                for k in items.iterkeys():
                    if k != Manifest.fname:  # The manifest file won't be included in the checksums
                        _checksums[k] = 'checksum_%s' % k
                
                return _checksums
        
        def ta_copy_behaviour(*args):
            if args[0] == copy_error_fname:
                raise copy_error
        
        mock_ta.copy.side_effect = ta_copy_behaviour
        
        # Expectations
        expected_items_dir = GtpSite(self.project_code).items_dir
        expected_ta_calls = [call.cd('%s/%s/%s' % (expected_items_dir, group_name, item_name)),
                             call.ls(),
                             call.copy(Manifest.fname, manifest_asset),
                             call.copy('item.xml', item_xml_asset, 'checksum_item.xml'),
                             call.copy('image_1.jpg', image_1_asset, 'checksum_image_1.jpg'),
                             call.copy('image_2.jpg', image_2_asset, 'checksum_image_2.jpg'),
                             call.copy(copy_error_fname, copy_error_asset, 'checksum_COPY_ERROR.jpg'),
                             ]
        
        expected_inbox_new_asset_calls = [ call(Manifest.fname, item_name), 
                                           call('item.xml', item_name),
                                           call('image_1.jpg', item_name),
                                           call('image_2.jpg', item_name),
                                           call('COPY_ERROR.jpg', item_name),]
        
        expected_num_inbox_lock_renew_calls = 3
        expected_inbox_unlock_calls = [call(item_name),]
        expected_new_assets = [item_xml_asset, image_1_asset, image_2_asset,]
        
        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        new_assets, errors = p.get_item(group_name, item_name, mock_inbox, _manifest_class=FakeManifest)
        
        # Assertions
        mock_ta.assert_has_calls(expected_ta_calls, any_order=True)
        mock_inbox.new_asset.assert_has_calls(expected_inbox_new_asset_calls, any_order=True)
        self.assertEqual(expected_num_inbox_lock_renew_calls, len(mock_inbox.lock_renew.mock_calls))
        self.assertListEqual(expected_inbox_unlock_calls, mock_inbox.unlock.call_args_list)
        self.assertListEqual(expected_new_assets, new_assets)
        self.assertEqual(1, len(errors))
        self.assertIsInstance(errors[0], TransferError)
        
    def test_delete_item(self):
        # Set up
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        
        item_fnames = [Manifest.fname, 'item.xml', 'image_1.jpg', 'image_2.jpg', 'image_3.jpg']
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_ta.ls.return_value = item_fnames

        # Expectations
        expected_ta_delete_calls = [call.delete(item_fnames[0]),
                                    call.delete(item_fnames[1]),
                                    call.delete(item_fnames[2]),
                                    call.delete(item_fnames[3]),
                                    call.delete(item_fnames[4]),]
        
        # Test
        config = self.config
        p = Provider(provider_name, mock_ta, config)
        p.delete_item(group_name, item_name)
        
        # Assertions
        mock_ta.assert_has_calls(expected_ta_delete_calls)
        mock_ta.rmdir.assert_called_once_with(item_name)
        
    def test_delete_item_TRANSFER_AGENT_FAILS(self):
        provider_name = 'provider_name'
        item_name = 'item_name'
        group_name = 'group_name'
        
        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        mock_ta.ls.side_effect = FtpError('Problem listing items!')
        
        p = Provider(provider_name, mock_ta, self.config)
        self.assertRaises(ProviderError, p.delete_item, group_name, item_name)
        
    def test_ok(self):
        provider_name = 'PROVIDER'
        item_name = 'item_name'
        group_name = 'group_name'
        report_fpath = '/report/path'

        mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        p = Provider(provider_name, mock_ta, self.config)
        p._report = create_autospec(p._report)
        p.delete_item = create_autospec(p.delete_item)
        
        p.ok(group_name, item_name, report_fpath)
        
        p._report.assert_called_with(item_name, report_fpath, is_good=True)
        p.delete_item.assert_called_with(group_name, item_name)
        
    def test_failed(self):
        provider_name = 'PROVIDER'
        item_name = 'item_name'
        group_name = 'group_name'
        report_fpath = '/report/path'

        mock_ta = MagicMock()
        
        p = Provider(provider_name, mock_ta, self.config)
        p._report = create_autospec(p._report)
        p.delete_item = create_autospec(p.delete_item)
        
        p.failed(group_name, item_name, report_fpath)
        
        p._report.assert_called_with(item_name, report_fpath, is_good=False)
        p.delete_item.assert_called_with(group_name, item_name)
        
    def test__empty_file(self):
        
        class TransferAgent:
            pass
        
        p = Provider('PROVIDER_NAME', TransferAgent(), self.config)
        
        expected_fpath = os.path.join(self.test_dir, 'empty_file.txt')
        
        actual_fpath = p._empty_file()
        self.assertEqual(expected_fpath, actual_fpath)
        self.assertTrue(os.path.exists(actual_fpath))
        
    def test__report_IS_GOOD(self): # 
        provider_name = 'PROVIDER'
        item_name = 'item_name'
        report_fpath = '/report/path'

        fixed_date = datetime.datetime(2012, 12, 31, 23, 59, 58, 123456)
        
        with patch('datetime.datetime') as date_time:
            date_time.utcnow.return_value = fixed_date
            mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
            
            expected_cd_arg = '/%s/reports/good' % self.project_code
            
            p = Provider(provider_name, mock_ta, self.config)
            p._report(item_name, report_fpath, is_good=True)
            mock_ta.cd.assert_called_with(expected_cd_arg)

            mock_ta.put.assert_called_with(report_fpath, '%s_2012_12_31_23_59_58_123456.txt' % item_name)
        
    def test__report_IS_BAD(self):
        provider_name = 'PROVIDER'
        item_name = 'item_name'
        report_fpath = '/report/path'
        
        fixed_date = datetime.datetime(2012, 12, 31, 23, 59, 58, 123456)
        
        with patch('datetime.datetime') as date_time:
            date_time.utcnow.return_value = fixed_date
            mock_ta = create_autospec(Ftp, spec_set=True, instance=True)
        
            expected_cd_arg = '/%s/reports/bad' % self.project_code
            
            p = Provider(provider_name, mock_ta, self.config)
            p._report(item_name, report_fpath, is_good=False)
            
            mock_ta.cd.assert_called_with(expected_cd_arg)
            mock_ta.put.assert_called_with(report_fpath, '%s_2012_12_31_23_59_58_123456.txt' % item_name)
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestProvider),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
