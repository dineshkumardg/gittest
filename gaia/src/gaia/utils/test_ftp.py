import unittest
from gaia.utils.ftp import FtpError, Ftp


class TestFtpError(unittest.TestCase):
    def test_str(self):
        expected_err_msg = 'FtpError: err msg'
        err = FtpError('err msg')
        self.assertEquals(expected_err_msg, str(err))


class TestFtp(unittest.TestCase):   # unit tests
    def test_open_FAIL_bad_server(self):
        # FTP ERROR: Could not connect to FTP Server (server="%s", uid="%s", pwd="****", err="[Errno 11001] getaddrinfo failed")
        server = 'not real'
        uid = 'tester'
        pwd = 'test8ble'
        expected_retry_counter = 3

        ftp = Ftp(server, uid, pwd, timeout_secs=0, retry_counter=expected_retry_counter, retry_timer=0)
        self.assertRaises(FtpError, ftp.open)
        self.assertEqual(ftp.retry_counter, expected_retry_counter)

'''
class SystemTestFtp(unittest.TestCase):
    # Warning: SYSTEM TESTS!
    # These tests require a ftp server running on 127.0.0.1 with a tester/keepitunreal account
    # and a /start/here /test, and /cho/items folder?.

    def setUp(self):
        self.server = '127.0.0.1'
        self.uid = 'tester'
        self.pwd = 'keepitunreal'
        self.initial_dir = '/cho/items'

        self.test_dir = '/tmp/gaia_tests/gaia/utils/ftp/'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir)
        
    def test_connect_OK(self):
        try:
            ftp = Ftp(self.server, self.uid, self.pwd)
            ftp.open()
        except Exception, e:
            self.fail('Connect failed with unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()
        
    def test_connect_OK_with_initial_dir(self):
        ftp = None
        try:
            ftp = Ftp(self.server, self.uid, self.pwd, self.initial_dir)
            ftp.open()
        except Exception, e:
            self.fail('Connect with initial_dir failed with unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()
        self.assertEqual(self.initial_dir, ftp._cwd)
        self.assertEqual(self.initial_dir, ftp._get_cwd())
        ftp.close()
        
    def test_connect_FAIL_with_initial_dir(self):
        BAD_initial_dir = self.initial_dir + '_NOT'
        ftp = Ftp(self.server, self.uid, self.pwd, BAD_initial_dir)
        self.assertRaises(FtpError, ftp.open)
        
    def test_connect_FAIL_bad_uid(self):
        # FTP ERROR: Could not connect to FTP Server (server="127.0.0.1", uid="guestNOT", pwd="****", err="530 Login or password incorrect!")
        BAD_uid = 'guestNOT'
        ftp = Ftp(self.server, BAD_uid, self.pwd)
        self.assertRaises(FtpError, ftp.open)
        
    def test_connect_FAIL_bad_pwd(self):
        # FTP ERROR: Could not connect to FTP Server (server="127.0.0.1", uid="guestNOT", pwd="****", err="530 Login or password incorrect!")
        BAD_pwd = 'guestBAD'
        ftp = Ftp(self.server, self.uid, BAD_pwd)
        self.assertRaises(FtpError, ftp.open)
        #Ftp(server, uid, pwd)  # DEBUG: use this to see the error.
        
    def test_close_OK(self):
        ftp = Ftp(self.server, self.uid, self.pwd)

        try:
            ftp.close()
        except Exception, e:
            self.fail('Quit failed with unexpected problem: "%s"' % str(e))
        
    def test_close_OK_retried(self):
        ftp = Ftp(self.server, self.uid, self.pwd)

        try:
            ftp.close()
            ftp.close()  # should _NOT_ do this, but the code should protect us.
        except Exception, e:
            self.fail('Quit failed with unexpected problem: "%s"' % str(e))
        
    def test_put_delete_OK(self):
        # Test put and delete in the same method to make sure this case doesn't break
        # other test cases.

        fname = 'put_data1.txt'
        fpath = os.path.join(self.test_dir, fname)
        f = open(fpath, 'wb')
        f.write('Hello ftp world')
        f.close()

        ftp = Ftp(self.server, self.uid, self.pwd)
        ftp.open()
        try:
            ftp.put(fpath)
            self.assertIn(fname,  ftp.ls())
            
            ftp.delete(fname)
            self.assertNotIn(fname, ftp.ls())
        except Exception, e:
            self.fail('Put failed with unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()
            
    def test_ls(self):
        expected_list = ['cho']
        #expected_filtered_list = ['test_10000.dat', 'test_8192.dat']
        
        ftp = Ftp(self.server, self.uid, self.pwd)
        ftp.open()
        try:
            actual_list = ftp.ls()
            #actual_filtered_list = ftp.ls('*.dat')            
        except Exception, e:
            self.fail('test_ls_OK failed with unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()            

        self.assertListEqual(sorted(expected_list), sorted(actual_list))
        #self.assertListEqual(sorted(expected_filtered_list), sorted(actual_filtered_list))

    def test_get_OK(self):
        hash_list = []
        fpath_list = []
        fname_list = ["test1.txt", "test2.txt", "test3.txt"]
        for fname in fname_list:
            fpath = os.path.join(self.test_dir, fname)
            f = open(fpath, 'wb')
            f.write('Hello ftp world')
            f.close()
            f = open(fpath, 'rb')
            checksum = hashlib.md5()
            checksum.update(f.read())
            hash_list.append(checksum.hexdigest())
            fpath_list.append(fpath)
            f.close()

        ftp = Ftp(self.server, self.uid, self.pwd)
        ftp.open()
        try:
            for i in range(0, len(fname_list)):
                fpath = fpath_list[i]
                fname = fname_list[i]
                ftp.put(fpath)
                self.assertIn(fname,  ftp.ls())
                os.remove(fpath)

                ftp.get(fname, fpath)

                f = open(fpath)
                checksum = hashlib.md5()
                checksum.update(f.read())
                self.assertEqual(hash_list[i], checksum.hexdigest())
                f.close()
                ftp.delete(fname)
                os.remove(fpath)
        except Exception, e:
            self.fail('test_get_OK failed with unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()
            
    def test_copy_OK(self):
        hash_list = []
        fpath_list = []
        fname_list = ["test1.txt", "test2.txt", "test3.txt"]
        for fname in fname_list:
            fpath = os.path.join(self.test_dir, fname)
            f = open(fpath, 'wb')
            f.write('Hello ftp world')
            f.close()
            f = open(fpath, 'rb')
            checksum = hashlib.md5()
            checksum.update(f.read())
            hash_list.append(checksum.hexdigest())
            fpath_list.append(fpath)
            f.close()

        ftp = Ftp(self.server, self.uid, self.pwd)
        ftp.open()

        try:
            for i in range(0, len(fname_list)):
                fpath = fpath_list[i]
                fname = fname_list[i]
                ftp.put(fpath)
                self.assertIn(fname,  ftp.ls())
                os.remove(fpath)

                to_file = Asset(fpath, "wb")
                ftp.copy(fname, to_file, required_checksum=hash_list[i])

                f = open(fpath)
                checksum = hashlib.md5()
                checksum.update(f.read())
                self.assertEqual(hash_list[i], checksum.hexdigest())
                f.close()
                ftp.delete(fname)
                os.remove(fpath)
        except Exception, e:
            self.fail('test_copy_OK failed with an unexpected problem: "%s"' % str(e))
        finally:
            ftp.close()

    

    def test_get_BAD(self):
        fname = 'bad.file'
        target_fpath = os.path.join(self.test_dir, fname)
        
        ftp = Ftp(self.server, self.uid, self.pwd)
        ftp.open()
        self.assertRaises(FtpError, ftp.get, fname, target_fpath)
        ftp.close()



class SystemTestFtpTIMEOUT(unittest.TestCase):
    # Note: this test sometimes will fail, sometime not!
    # Change the timeout value or file size to create the error (or just re-run and it _might_ fail)
    # Also note that a small timeout vvalue will cause the connect() to fail rather than
    # a data transfer operation.

    def setUp(self):
        self.server = '127.0.0.1'
        self.uid = 'htc'
        self.pwd = 'qwerty123'
        self.initial_dir = '/cho/items'

        self.test_dir = '/tmp/gaia_tests/gaia/utils/ftp/'
        if not os.path.exists(self.test_dir):
            os.makedirs(self.test_dir) 

    def test_copy_TIMEOUT(self):
        fname = "big_file_1"
        fpath = os.path.join(self.test_dir, fname)
        f = open(fpath, 'wb')
        size = 100000000   # nearly 100MB
        f.write("\0" * size)
        f.close()

        ftp = Ftp(self.server, self.uid, self.pwd, timeout_secs=0.16)   # NOTE maybe play with this timeout value :)
        ftp.open()

        try:
            ftp.put(fpath)
            self.assertIn(fname,  ftp.ls())
            os.remove(fpath)

            to_file = Asset(fpath, "wb")
            self.assertRaises(FtpError, ftp.copy, fname, to_file)

        except Exception, e:
            self.fail('test_copy_timeout failed with an unexpected problem: "%s"' % str(e))
        finally:
            ftp.delete(fname)
            ftp.close()
            try: # if FtpError not raise, means file copyed succeefully, need to remove this file
                os.remove(fpath)
            except Exception, e:
                pass
'''

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestFtpError),
    unittest.TestLoader().loadTestsFromTestCase(TestFtp),
    ])


if __name__ == "__main__":
    unittest.main()
