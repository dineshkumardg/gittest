import unittest
from gaia.error import GaiaError
from gaia.dom.model.dom_error import GaiaDomError

class TestGaiaDomError(unittest.TestCase):

    def test__init__(self):
        e = GaiaDomError()
        self.assertIsInstance(e, GaiaError)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestGaiaDomError),
    ])

if __name__ == "__main__":
    unittest.main()
