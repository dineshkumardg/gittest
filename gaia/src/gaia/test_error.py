import unittest
from gaia.error import GaiaError, GaiaSystemError, GaiaCodingError, GaiaErrors

class TestGaiaError(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'GaiaError: This is an error msg'
        
        self.assertEquals(expected_err_msg, str(GaiaError('This is an error msg')))
        
    def test_with_args_STR_INT(self):
        expected_err_msg = 'GaiaError: uhoh! (problem="houston", mission="apollo", error="13")'
        
        e = GaiaError('uhoh!', problem='houston', mission='apollo', error=13)
        self.assertEquals(expected_err_msg, str(e))
        
    def test_with_args_NONE(self):
        expected_err_msg = 'GaiaError: uhoh! (nothing="None", problem="houston", mission="apollo", error="13")'
        
        e = GaiaError('uhoh!', problem='houston', mission='apollo', error=13, nothing=None)
        self.assertEquals(expected_err_msg, str(e))
        
    def test_with_kwargs_UNICODE(self):
        expected_err_msg ='GaiaError: nothing="None", problem="houston", error="13", uhoh="uhoh\xe1\x88\xb4!", mission="apollo"'
        
        # NOTE: this is *not* supported!! (only allowed to have unicode chars in kwargs)
        #e = GaiaError(u'uhoh\u1234!', problem='houston', mission='apollo', error=13, nothing=None)
        e = GaiaError(uhoh=u'uhoh\u1234!'.encode('utf-8'), problem='houston', mission='apollo', error=13, nothing=None)
        self.assertEquals(expected_err_msg, str(e))
        
    def test_no_msg_or_kwargs_OK(self):
        e = GaiaError()
        self.assertEquals('GaiaError: ', str(e))
        
    #def test_no_msg_or_kwargs_FAILS(self):
        #self.assertRaises(GaiaCodingError, GaiaError)
        
    def test_no_msg_with_args_HAS_NO_BRACKETS(self):
        expected_err_msg = 'GaiaError: hello="world"'   # Note: no brackets.
        
        e = GaiaError(hello='world')
        self.assertEquals(expected_err_msg, str(e))
        
class TestGaiaSystemError(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'GaiaSystemError: This is an error msg'
        
        self.assertEquals(expected_err_msg, str(GaiaSystemError('This is an error msg')))
        self.assertTrue(issubclass(GaiaSystemError, GaiaError))

class TestGaiaCodingError(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'GaiaCodingError: a programming mistake.'
        
        self.assertEquals(expected_err_msg, str(GaiaCodingError('a programming mistake.')))
        self.assertTrue(issubclass(GaiaCodingError, GaiaSystemError))
        self.assertTrue(issubclass(GaiaCodingError, GaiaError))

class TestGaiaErrors(unittest.TestCase):

    def test_str(self):
        expected_err_msg = 'GaiaError: This is an error msg'
        self.assertEquals(expected_err_msg, str(GaiaErrors(GaiaError('This is an error msg'))))
        self.assertTrue(issubclass(GaiaErrors, GaiaError))
        
    def test_str_errors_passed_in_init(self):
        expected_err_msg = ''
        num_errors = 10

        errs = []
        for i in range(0, num_errors):
            err_msg = 'This is a error msg %d' % i
            expected_err_msg = expected_err_msg + 'GaiaError: ' + err_msg  + '\n'
            errs.append(GaiaError(err_msg))

        expected_err_msg = expected_err_msg[:-1]    # no trailing newline
        gaia_errors = GaiaErrors(*errs)
        self.assertEquals(expected_err_msg, str(gaia_errors))
        self.assertEquals(num_errors, len(gaia_errors.errors))

        for i in range(0, num_errors):
            self.assertEquals(errs[i], gaia_errors.errors[i])
            
    def test_single_error_passed_in(self):
        err = Exception('An Error')
        gaia_errors = GaiaErrors(err)
        expected_err = 'An Error'
        self.assertEqual(expected_err, str(gaia_errors))

    def test_str_errors_append(self):
        expected_err_msg = ''
        num_errors = 10
        gaia_errors = GaiaErrors()
        expected_errs = []

        for i in range(0, num_errors):
            err_msg = 'This is a error msg %d' % i
            expected_err_msg = expected_err_msg + 'GaiaError: ' + err_msg  + '\n'
            err = GaiaError(err_msg)
            expected_errs.append(err)
            gaia_errors.append(err)

        expected_err_msg = expected_err_msg[:-1]    # no trailing newline
        self.assertEquals(expected_err_msg, str(gaia_errors))
        self.assertEquals(num_errors, len(gaia_errors.errors))

        for i in range(0, num_errors):
            self.assertEquals(expected_errs[i], gaia_errors.errors[i])
        
        
suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaError),
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaSystemError),
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaCodingError),
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaErrors),
    ])

if __name__ == "__main__":
    unittest.main()
