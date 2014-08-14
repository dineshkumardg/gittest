import sys
import unittest
from gaia.utils.try_cmd import try_cmd, CommandError, CommandFailed, CommandStartError

class TestCommandError(unittest.TestCase):

    def test_str(self):
        msg = 'do_this --with that --and that did not work: whoops!'
        expected_err_msg = 'CommandError: ' + msg

        err = CommandError(msg)
        self.assertEquals(expected_err_msg, str(err))
        
class TestCommandFailed(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'CommandFailed: cmd="[\'do_this\', \'arg1\', \'arg2\']" (retcode="-9", stdout="some output", stderr="some errors")'
        
        cmd = ['do_this',  'arg1', 'arg2']
        retcode = -9
        stdout = 'some output'
        stderr = 'some errors'

        err = CommandFailed(cmd, retcode, stdout, stderr)
        self.assertEquals(expected_err_msg, str(err))
        
class TestCommandStartError(unittest.TestCase):
    
    def test_str(self):
        cmd = ['do_this',  'arg1', 'arg2']
        err = 'This is the error'
        
        expected_err_msg = 'CommandStartError: Could not run command (cmd="%s", cause="%s")' % (str(cmd), str(err))
        
        err = CommandStartError(cmd, err)
        self.assertEqual(expected_err_msg, str(err))
        
class TestTryCmd(unittest.TestCase):

    @unittest.skipUnless(sys.platform.startswith("win"), 'a windows command test')
    def test_try_cmd_WIN(self):
        #WArning: WE NEED TO CHANGE THIS TO SOMETHING RELIABLY USABLE!...TODO # :( dir requires shell as it's a built-in :(
        cmd = [r'c:\Program Files\ImageMagick\convert.exe',  '-version'] 
        output = try_cmd(*cmd)
        self.assertTrue('Version' in output)
        self.assertTrue('ImageMagick' in output)
        
    @unittest.skipUnless(sys.platform.startswith("linux"), 'a linux command test')
    def test_try_cmd_UNIX(self):
        cmd = ['ls',  '--version'] 
        output = try_cmd(*cmd)
        self.assertTrue('Copyright' in output)
        self.assertTrue('Free Software Foundation' in output)
        
    def test_try_cmd_BAD_CMD(self):
        cmd = ['/usr/bin/a_non_existent_program',  '--version'] 
        self.assertRaises(CommandStartError, try_cmd, *cmd)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestCommandStartError),
    unittest.TestLoader().loadTestsFromTestCase(TestCommandError),
    unittest.TestLoader().loadTestsFromTestCase(TestTryCmd),
    ])

if __name__ == "__main__":
    unittest.main()
