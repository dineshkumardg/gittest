import unittest
import os
from StringIO import StringIO
from testing.gaia_test import GaiaTest
from gaia.error import GaiaErrors
from gaia.schema.schema import Dtd, XmlParseError
from lxml.etree import DTDParseError
from gaia.dom.document_error import InvalidXml

class TestDtd(GaiaTest):

    def _write_xml(self, xml):
        self.xml_fname = 'test.xml'
        self.xml_fpath = os.path.join(self.test_dir, self.xml_fname)
        f = open(self.xml_fpath, 'w')
        f.write(xml)
        f.close()
        
    def _write_schema(self, content, ext):
        self.schema_fname = 'test.' + ext
        self.schema_fpath = os.path.join(self.test_dir, self.schema_fname)
        f = open(self.schema_fpath, 'w')
        f.write(content)
        f.close()

    def test_validate_XML_VALID_DTD_VALID(self):
        
        dtd = '''<?xml version="1.0" encoding="UTF-8"?>
<!ELEMENT emails (email)>
<!ELEMENT email (from,to+,subject,body)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT subject (#PCDATA)>
<!ELEMENT body (#PCDATA)> 
'''
        self._write_schema(dtd, 'dtd')
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com</from>
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''
        
        self._write_xml(xml)
        try:
            Dtd.validate(self.xml_fpath, self.schema_fpath)
        except GaiaErrors, e:
            self.fail('UNEXPECTEDLY FAILED: %s' % str(e))

    def test_validate_against_dtd_XML_VALID_BUT_DTD_NOT_VALID(self):
        dtd = '''INVALID DTD! Oops'''

        self._write_schema(dtd, 'dtd')
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com</from>
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''
        
        self._write_xml(xml)
        # Note: should be XmlParseError ?
        self.assertRaises(DTDParseError, Dtd.validate, self.xml_fpath, self.schema_fpath)

    def test_validate_XML_INVALID_AGAINST_DTD(self):
        dtd = '''<?xml version="1.0" encoding="UTF-8"?>
<!ELEMENT emails (email)>
<!ELEMENT email (from,to+,subject,body)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT subject (#PCDATA)>
<!ELEMENT body (#PCDATA)> 
'''
        self._write_schema(dtd, 'dtd')
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com</from> <!-- THIS IS INCORRECT ACCORDING TO ABOVE SCHEMA -->
    <from>tush@meister.com</from>
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''
        
        self._write_xml(xml)
        
        expected_error = 'InvalidXml: line="3", error="Element email content does not follow the DTD, expecting (from , to+ , subject , body), got (from from to to subject body )", file="%s", schema="%s"' % (self.xml_fname, self.schema_fname)
        
        try:
            Dtd.validate(self.xml_fpath, self.schema_fpath)
            self.fail('UNEXPECTEDLY PASSED!')
        except GaiaErrors, e:
            self.assertEqual(1, len(e.errors))
            err = e.errors[0]
            self.assertIsInstance(err, InvalidXml)
            self.assertEqual(expected_error, str(err))

    def test_validate_USING_STRINGIO(self):
        dtd = '''<?xml version="1.0" encoding="UTF-8"?>
<!ELEMENT emails (email)>
<!ELEMENT email (from,to+,subject,body)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT subject (#PCDATA)>
<!ELEMENT body (#PCDATA)> 
'''

        self._write_schema(dtd, 'dtd')
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com</from>
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''
        
        try:
            Dtd.validate(StringIO(xml), self.schema_fpath)
        except GaiaErrors, e:
            self.fail('UNEXPECTEDLY FAILED: %s' % str(e))

    def test_validate_NOT_WELL_FORMED(self):
        
        dtd = '''<?xml version="1.0" encoding="UTF-8"?>
<!ELEMENT emails (email)>
<!ELEMENT email (from,to+,subject,body)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT subject (#PCDATA)>
<!ELEMENT body (#PCDATA)> 
'''

        self._write_schema(dtd, 'dtd')
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com   ** NOT WELL FORMED **
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''

        self._write_xml(xml)
        
        self.assertRaises(XmlParseError, Dtd.validate, xml_fpath=self.xml_fpath, xsd_fpath=self.schema_fpath)

    def test_validate_XSD_NOT_FOUND(self):
        
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<emails>
  <email>
    <from>tush@meister.com</from>
    <to>steve@boom.net</to>
    <to>dave@bust.net</to>
    <subject>Le singe est sur la branche</subject>
    <body>Et, la souris est en-dessous de la table</body>
  </email>
</emails>'''

        self._write_xml(xml)
        # should be InvalidXmlSchema error?
        self.assertRaises(DTDParseError, Dtd.validate, xml_fpath=self.xml_fpath, xsd_fpath='/tmp/non_existant')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestDtd),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
