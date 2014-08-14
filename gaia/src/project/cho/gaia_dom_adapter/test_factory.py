import unittest
import project.cho.gaia_dom_adapter.cho
from project.cho.gaia_dom_adapter.factory import Factory
from testing.gaia_test import GaiaTest

class TestCHODomAdapterFactory(GaiaTest):
    
    def test_journal(self):
        for fname, expected_class in [
                    ('cho_iaxx_1963_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),
                    ('cho_binx_1963_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),
                    ('cho_diax_1963_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),
                    ('cho_siax_1963_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),
                    ('cho_wtxx_1963_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),
                    ('cho_wtxx_1935-1936_0039_000_0001.xml', project.cho.gaia_dom_adapter.cho.Cho),   # multiyear
                ]:
            self._test_class(fname, expected_class)

    def _test_class(self, fname, expected_type):
        f = Factory()
        self.assertEqual(expected_type, f.adapter_class(fname))
            

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestCHODomAdapterFactory),
    ])


if __name__ == "__main__":
    import testing
    testing.main(suite)
