import unittest
from gaia.dom.document_error import DocumentError, InvalidXmlSchema, InvalidXml

class TestDocumentError(unittest.TestCase):
    # Some of the tests have unused variable warnings; these are necessary to ensure the class is tested correctly.

    def test__str__(self):
        expected_str = 'DocumentError: A problem'

        e = DocumentError('A problem')

        self.assertEqual(expected_str, str(e))
        
class TestInvalidXmlSchema(unittest.TestCase):

    def test__str__(self):
        expected_str = 'InvalidXmlSchema: xsd="/full/path/to/a_schema.xsd", error="A problem"'

        e = InvalidXmlSchema('/full/path/to/a_schema.xsd', Exception('A problem'))

        self.assertEqual(expected_str, str(e))
        
class TestInvalidXml(unittest.TestCase):

    def test__str__(self):
        expected_str = 'InvalidXml: line="99", error="A problem", file="a_file.xml", schema="a_schema.xsd"'

        e = InvalidXml('/full/path/to/a_file.xml', '/full/path/to/schema/a_schema.xsd', 99,  Exception('A problem'))

        self.assertEqual(expected_str, str(e))

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestDocumentError),
    ])


if __name__ == "__main__":
    unittest.main()
