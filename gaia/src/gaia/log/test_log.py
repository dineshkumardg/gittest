import os
import unittest
import logging
import time
from testing.gaia_test import GaiaTest
from mock import patch, MagicMock, create_autospec
from gaia.log.log import Log, _GaiaFormatter
from gaia.error import GaiaError

class Test_GaiaFormatter(GaiaTest):
    
    def _set_up_test_format(self, level):
        record = create_autospec(logging.LogRecord, instance=True)
        record.levelno = level
        record.created = time.time()
        record.name = 'RECORD_NAME'
        record.msecs = 1234567890
        record.funcName = 'test_func'
        record.getMessage.return_value = 'A super dooper log message!!'
        local_time = time.localtime(time.time())
        
        # Careful here - this may change if _GaiaFormatter overrides logging.Formatter.formatTime() to pass in a date format
        expected_time_stamp = time.strftime("%Y-%m-%d %H:%M:%S", local_time)

        mock_formatter = MagicMock()
        mock_formatter.formatTime.return_value = expected_time_stamp
        
        return record, expected_time_stamp, mock_formatter
    
    def test_format_ENTER(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(Log.ENTER)
        
        expected_msg = '[%s,%d] DEBUG: >>> %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_EXIT(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(Log.EXIT)
        
        expected_msg = '[%s,%d] DEBUG: <<< %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_DEBUG(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(logging.DEBUG)
        
        expected_msg = '[%s,%d] DEBUG: ... %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_INFO(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(logging.INFO)
        
        expected_msg = '[%s,%d] INFO:  ... %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_WARN(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(logging.WARN)
        
        expected_msg = '[%s,%d] WARN:  ooo %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_ERROR(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(logging.ERROR)
        
        expected_msg = '[%s,%d] ERROR: *** %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))

    def test_format_CRITICAL(self):
        formatter = _GaiaFormatter()
        record, expected_time_stamp, mock_formatter = self._set_up_test_format(logging.CRITICAL)
        
        expected_msg = '[%s,%d] CRIT!: *** %s.%s(): %s' % (expected_time_stamp, record.msecs, record.name, record.funcName, record.getMessage())

        with patch('logging.Formatter') as mock_formatter:
            self.assertEqual(expected_msg, formatter.format(record))
            
class TestLog(GaiaTest):
    
    @patch('logging.getLogger')
    def test_get_logger(self, getLogger):
        l = MagicMock()
        getLogger.return_value = l
        for_object = object()
        logger = Log.get_logger(for_object)
        getLogger.assert_called_once_with('object')
        self.assertEqual(l, logger)
    
    @patch('gaia.log.log._GaiaFormatter')
    @patch('logging.handlers.RotatingFileHandler')
    @patch('logging.getLogger')
    @patch('logging.setLoggerClass')    
    @patch('os.getpid')
    def test_configure_logging_MULTI_PROCESS_WITH_ROLLOVER(self, getpid, setLoggerClass, getLogger, RotatingFileHandler, _GaiaFormatter): # Note order the mocks are passed in... stack them upwards!!
        # Setup
        log_name = 'NAME'
        log_dir = self.test_dir
        log_level = Log.ENTER

        pid = '1234'
        getpid.return_value = pid
        
        mock_logger = MagicMock()
        getLogger.return_value = mock_logger
        
        mock_rotating_file_handler = MagicMock()
        RotatingFileHandler.return_value = mock_rotating_file_handler
        
        mock_formatter = MagicMock()
        _GaiaFormatter.return_value = mock_formatter
        
        config = MagicMock()
        config.log_dir = log_dir
        config.log_level = log_level

        # Expectations        
        expected_fname = os.path.join(self.test_dir, '%s_%s.log' % (log_name, pid))
        
        # Test
        fname = Log.configure_logging(log_name, config, multi_process=True, rollover=True)

        # Assertions        
        setLoggerClass.assert_called_once_with(Log)
        getpid.assert_called_once_with()
        mock_rotating_file_handler.doRollover.assert_called_once_with()
        mock_rotating_file_handler.setFormatter.assert_called_once_with(mock_formatter)
        mock_logger.addHandler.assert_called_once_with(mock_rotating_file_handler)
        mock_logger.setLevel.assert_called_once_with(log_level)
        self.assertEqual(expected_fname, fname)
        
    @patch('logging.FileHandler')
    @patch('logging.getLogger')
    @patch('logging.setLoggerClass')    
    def test_configure_logging_SINGLE_PROCESS_NO_ROLLOVER(self, setLoggerClass, getLogger, FileHandler): # Note order the mocks are passed in... stack them upwards!!
        # Setup
        log_name = 'NAME'
        log_dir = self.test_dir
        log_level = Log.ENTER
        
        mock_logger = MagicMock()
        getLogger.return_value = mock_logger
        
        mock_file_handler = MagicMock()
        FileHandler.return_value = mock_file_handler
        
        config = MagicMock()
        config.log_dir = log_dir
        config.log_level = log_level

        # Expectations        
        expected_fname = os.path.join(self.test_dir, '%s.log' % log_name)
        
        # Test
        fname = Log.configure_logging(log_name, config, multi_process=False, rollover=False)

        # Assertions        
        setLoggerClass.assert_called_once_with(Log)
        mock_logger.addHandler.assert_called_once_with(mock_file_handler)
        mock_logger.setLevel.assert_called_once_with(log_level)
        self.assertEqual(expected_fname, fname)
        
    def _test_log_func(self, func_to_test, expected_level, expected_msg, *args, **kwargs):
        log = Log('NAME')
        log.log = create_autospec(log.log)
        getattr(log, func_to_test)(*args, **kwargs) # Call the function func on the log object
        log.log.assert_called_with(expected_level, msg=expected_msg)
                
    def test_enter_no_args(self):
        self._test_log_func('enter', Log.ENTER, '')
        
    def test_enter_with_args(self):
        self._test_log_func('enter', Log.ENTER, 'one 2 three', 'one', '2', 'three')
        
    def test_enter_with_kwargs(self):
        self._test_log_func('enter', Log.ENTER, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_enter_with_args_and_kwargs(self):
        self._test_log_func('enter', Log.ENTER, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_exit_no_args(self):
        self._test_log_func('exit', Log.EXIT, '')
        
    def test_exit_with_args(self):
        self._test_log_func('exit', Log.EXIT, 'one 2 three', 'one', '2', 'three')
        
    def test_exit_with_kwargs(self):
        self._test_log_func('exit', Log.EXIT, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_exit_with_args_and_kwargs(self):
        self._test_log_func('exit', Log.EXIT, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_debug_no_args(self):
        self._test_log_func('debug', logging.DEBUG, '')
        
    def test_debug_with_args(self):
        self._test_log_func('debug', logging.DEBUG, 'one 2 three', 'one', '2', 'three')
        
    def test_debug_with_kwargs(self):
        self._test_log_func('debug', logging.DEBUG, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_debug_with_args_and_kwargs(self):
        self._test_log_func('debug', logging.DEBUG, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_info_no_args(self):
        self._test_log_func('info', logging.INFO, '')
        
    def test_info_with_args(self):
        self._test_log_func('info', logging.INFO, 'one 2 three', 'one', '2', 'three')
        
    def test_info_with_kwargs(self):
        self._test_log_func('info', logging.INFO, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_info_with_args_and_kwargs(self):
        self._test_log_func('info', logging.INFO, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_warning_no_args(self):
        self._test_log_func('warning', logging.WARN, '')
        
    def test_warning_with_args(self):
        self._test_log_func('warning', logging.WARN, 'one 2 three', 'one', '2', 'three')
        
    def test_warning_with_kwargs(self):
        self._test_log_func('warning', logging.WARN, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_warning_with_args_and_kwargs(self):
        self._test_log_func('warning', logging.WARN, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_error_no_args(self):
        self._test_log_func('error', logging.ERROR, '')
        
    def test_error_with_args(self):
        self._test_log_func('error', logging.ERROR, 'one 2 three', 'one', '2', 'three')
        
    def test_error_with_kwargs(self):
        self._test_log_func('error', logging.ERROR, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])

    def test_error_with_kwargs_with_error_object(self):
        e = GaiaError('This is an error')
        self._test_log_func('error', logging.ERROR, '(error="GaiaError: This is an error")', error=e)
        
    def test_error_with_args_and_kwargs(self):
        self._test_log_func('error', logging.ERROR, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])

    def test_critical_no_args(self):
        self._test_log_func('critical', logging.CRITICAL, '')
        
    def test_critical_with_args(self):
        self._test_log_func('critical', logging.CRITICAL, 'one 2 three', 'one', '2', 'three')
        
    def test_critical_with_kwargs(self):
        self._test_log_func('critical', logging.CRITICAL, '(parts="[1, 2, 3]", hello="world", goodbye="universe")', hello='world', goodbye='universe', parts=[1,2,3])
        
    def test_critical_with_args_and_kwargs(self):
        self._test_log_func('critical', logging.CRITICAL, 'one 2 three (parts="[1, 2, 3]", hello="world", goodbye="universe")', 'one', '2', 'three', hello='world', goodbye='universe', parts=[1,2,3])
    

class TestUnicode(GaiaTest):
    def test_unicode(self):
        log = Log('foo')
        msg = log._args_str(u'one\u1234two', '2', 'three', hello=u'w\u9876orld', goodbye='universe', parts=[1, u'uh\u3456oh', 3])
        # Hmm.. the array printing doesn't match the rest, but it works out okay for us (for now).
        # Roll on py3k!
        # WARNING: in pydev this assert requires run configuration > Common > Encoding = US-ASCII
        self.assertEqual(r'''one?two 2 three (parts="[1, u'uh\u3456oh', 3]", hello="w?orld", goodbye="universe")''', msg)

    def test_unicode_with_kwarg_object(self):
        class UnicodeThing:
            def __str__(self):
                return u'SOME_UNICODE\u1234THING'

        thing = UnicodeThing()

        log = Log('foo')
        msg = log._args_str(u'one\u1234two', '2', 'three', hello=u'w\u9876orld', goodbye='universe', parts=[1, u'uh\u3456oh', 3], thing=thing)
        # Hmm.. the array printing doesn't match the rest, but it works out okay for us (for now).
        # Roll on py3k!
        # This will have an object id in it for "thing", eg:
        # one?two 2 three (thing="_cannot_print_unicode_data_for_object_id:33740560", parts="[1, u'uh\u3456oh', 3]", hello="w?orld", goodbye="universe")
        # WARNING: in pydev this assert requires run configuration > Common > Encoding = US-ASCII
        first_part_of_msg = r'''one?two 2 three (thing="_cannot_print_unicode_data_for_object_id:''' # 33740560"
        last_part_of_msg = r'''parts="[1, u'uh\u3456oh', 3]", hello="w?orld", goodbye="universe")'''
        self.assertEqual(first_part_of_msg, msg[:len(first_part_of_msg)])
        self.assertEqual(last_part_of_msg, msg[-len(last_part_of_msg):])

    def test_unicode_from_file(self):
        # TUSH: no idea why this test is reqauired...? REMOVE? TODO (ask James)
        f = open(os.path.join(os.path.dirname(__file__), 'test_files/unicode-cho_iprx_1947_0001_000_0000.xml'), 'r')
        unicode_data = f.read()
        f.close()

        try:
            log = Log.get_logger(self)
            log.debug(unicode_data)
        except UnicodeEncodeError:
            self.fail('.debug not coped with unicode')
    

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(Test_GaiaFormatter),
    unittest.TestLoader().loadTestsFromTestCase(TestLog),
    unittest.TestLoader().loadTestsFromTestCase(TestUnicode),
    ])

if __name__ == '__main__':
    import testing
    testing.main(suite)
