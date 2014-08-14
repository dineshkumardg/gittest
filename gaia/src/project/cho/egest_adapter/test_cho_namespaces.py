import unittest
from test_utils.gaia_test import GaiaTest
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces


class TestChoNamespaces(GaiaTest):
    def test_remove_ns(self):
        # EXPECTATION
        expected_xml_without_ns = '''
      <gift-doc:node-metadata>
        <meta:descriptive-indexing>
          <meta:indexing-term>
            <meta:term>
              <meta:term-type>PUB_SEG_TYPE</meta:term-type>
          </meta:indexing-term>
        </meta:descriptive-indexing>
        <gift-doc:pagination-group>
          <gift-doc:pagination>
            <meta:total-pages>14</meta:total-pages>
          </gift-doc:pagination>
        </gift-doc:pagination-group>
      </gift-doc:node-metadata>'''

        # TEST
        xml_with_ns = '''
      <gift-doc:node-metadata>
        <meta:descriptive-indexing xmlns:meta="http://www.gale.com/goldschema/metadata">
          <meta:indexing-term>
            <meta:term>
              <meta:term-type>PUB_SEG_TYPE</meta:term-type>
          </meta:indexing-term>
        </meta:descriptive-indexing>
        <gift-doc:pagination-group>
          <gift-doc:pagination>
            <meta:total-pages xmlns:meta="http://www.gale.com/goldschema/metadata">14</meta:total-pages>
          </gift-doc:pagination>
        </gift-doc:pagination-group>
      </gift-doc:node-metadata>'''

        actual_xml = ChoNamespaces.remove_ns(xml_with_ns)

        # ASSERTION
        self.assertEquals(expected_xml_without_ns, actual_xml)

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestChoNamespaces),
    ])

if __name__ == "__main__":
    testing.main(suite)