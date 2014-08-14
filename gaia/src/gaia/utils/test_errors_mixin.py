import unittest
from gaia.utils.errors_mixin import ErrorsMixin
from gaia.error import GaiaErrors


class TestErrorsMixin(unittest.TestCase):
    
    def test__init__(self):
        em = ErrorsMixin()
        em._collected_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        em.__init__()
        self.assertEqual(None, em.errors())

    def test_raise_if_errors(self):
        em = ErrorsMixin()
        em._collected_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        self.assertRaises(GaiaErrors, em.raise_if_errors)

    def test_errors(self):
        em = ErrorsMixin()
        em._collected_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        self.assertEqual(GaiaErrors(*em._collected_errors).errors, em.errors().errors)

    def test_reset_errors(self):
        em = ErrorsMixin()
        em._collected_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        em.reset_errors()
        self.assertEqual(None, em.errors())

    def test_add_error(self):
        existing_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        error_to_be_added = Exception('ADDED ERROR')

        em = ErrorsMixin()
        em._collected_errors = existing_errors
        
        em.add_error(error_to_be_added)

        self.assertIn(error_to_be_added, em.errors().errors)
        
        for e in existing_errors:
            self.assertIn(e, em.errors().errors)

    def test_errors_WITH_COLLECTED_ERRORS(self):
        em = ErrorsMixin()
        em._collected_errors = [Exception('Error1'), Exception('Error2'), Exception('Error3')]
        result = em.errors()
        
        self.assertIsInstance(result, GaiaErrors)
        
        for e in result.errors:
            self.assertIn(e, em._collected_errors)
            
    def test_errors_COLLECTED_ERRORS_NONE(self):
        em = ErrorsMixin()
        em._collected_errors = None
        
        self.assertEqual(None, em.errors())

    def test_errors_COLLECTED_ERRORS_EMPTY(self):
        em = ErrorsMixin()
        em._collected_errors = []
        
        self.assertEqual(None, em.errors())

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestErrorsMixin),
    ])


if __name__ == "__main__":
    unittest.main()
