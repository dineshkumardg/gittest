import os
import unittest
from StringIO import StringIO
from testing.gaia_test import GaiaTest
from gaia.error import GaiaErrors
from gaia.schema.schema import Xsd, XmlParseError
from gaia.dom.document_error import InvalidXmlSchema, InvalidXml

class TestXmlParseError(unittest.TestCase):
    
    def test__str__(self):
        expected_str = 'XmlParseError: A problem'

        e = XmlParseError('A problem')

        self.assertEqual(expected_str, str(e))

class TestXsd(GaiaTest):

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

    def test_validate_XML_VALID_XSD_VALID(self):
        
        xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

    <xs:element name="emails">
      <xs:complexType>
          <xs:sequence>
            <xs:element name="email" minOccurs="1" maxOccurs="unbounded">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="from" type="xs:string" />
                  <xs:element name="to" type="xs:string" minOccurs="1" maxOccurs="unbounded" />
                  <xs:element name="subject" type="xs:string" />
                  <xs:element name="body" type="xs:string" />
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
      </xs:complexType>
    </xs:element>

  <xs:element name="to" type="xs:string" />
  <xs:element name="from" type="xs:string" />
  <xs:element name="subject" type="xs:string" />
  <xs:element name="body" type="xs:string" />
  
</xs:schema>
'''

        self._write_schema(xsd, 'xsd')
        
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
            Xsd.validate(self.xml_fpath, self.schema_fpath)
        except GaiaErrors, e:
            self.fail('UNEXPECTEDLY FAILED: %s' % str(e))
            
    def test_validate_against_xsd_XML_VALID_BUT_XSD_NOT_VALID(self):
        
        xsd = '''INVALID XSD! Oops'''

        self._write_schema(xsd, 'xsd')
        
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
        self.assertRaises(InvalidXmlSchema, Xsd.validate, self.xml_fpath, self.schema_fpath)
        
    def test_validate_XML_INVALID_AGAINST_XSD(self):
                
        xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

    <xs:element name="emails">
      <xs:complexType>
          <xs:sequence>
            <xs:element name="email" minOccurs="1" maxOccurs="unbounded">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="from" type="xs:string" />
                  <xs:element name="to" type="xs:string" minOccurs="1" maxOccurs="unbounded" />
                  <xs:element name="subject" type="xs:string" />
                  <xs:element name="body" type="xs:string" />
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
      </xs:complexType>
    </xs:element>

  <xs:element name="to" type="xs:string" />
  <xs:element name="from" type="xs:string" />
  <xs:element name="subject" type="xs:string" />
  <xs:element name="body" type="xs:string" />
  
</xs:schema>
'''

        self._write_schema(xsd, 'xsd')
        
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
        
        expected_error = 'InvalidXml: line="5", error="Element \'from\': This element is not expected. Expected is ( to ).", file="%s", schema="%s"' % (self.xml_fname, self.schema_fname)
        
        try:
            Xsd.validate(self.xml_fpath, self.schema_fpath)
            self.fail('UNEXPECTEDLY PASSED!')
        except GaiaErrors, e:
            self.assertEqual(1, len(e.errors))
            err = e.errors[0]
            self.assertIsInstance(err, InvalidXml)
            self.assertEqual(expected_error, str(err))
            
    def test_validate_USING_STRINGIO(self):
        
        xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

    <xs:element name="emails">
      <xs:complexType>
          <xs:sequence>
            <xs:element name="email" minOccurs="1" maxOccurs="unbounded">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="from" type="xs:string" />
                  <xs:element name="to" type="xs:string" minOccurs="1" maxOccurs="unbounded" />
                  <xs:element name="subject" type="xs:string" />
                  <xs:element name="body" type="xs:string" />
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
      </xs:complexType>
    </xs:element>

  <xs:element name="to" type="xs:string" />
  <xs:element name="from" type="xs:string" />
  <xs:element name="subject" type="xs:string" />
  <xs:element name="body" type="xs:string" />
  
</xs:schema>
'''

        self._write_schema(xsd, 'xsd')
        
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
            Xsd.validate(StringIO(xml), self.schema_fpath)
        except GaiaErrors, e:
            self.fail('UNEXPECTEDLY FAILED: %s' % str(e))
        
        
    def test_validate_NOT_WELL_FORMED(self):
        
        xsd = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">

    <xs:element name="emails">
      <xs:complexType>
          <xs:sequence>
            <xs:element name="email" minOccurs="1" maxOccurs="unbounded">
              <xs:complexType>
                <xs:sequence>
                  <xs:element name="from" type="xs:string" />
                  <xs:element name="to" type="xs:string" minOccurs="1" maxOccurs="unbounded" />
                  <xs:element name="subject" type="xs:string" />
                  <xs:element name="body" type="xs:string" />
                </xs:sequence>
              </xs:complexType>
            </xs:element>
          </xs:sequence>
      </xs:complexType>
    </xs:element>

  <xs:element name="to" type="xs:string" />
  <xs:element name="from" type="xs:string" />
  <xs:element name="subject" type="xs:string" />
  <xs:element name="body" type="xs:string" />
  
</xs:schema>
'''

        self._write_schema(xsd, 'xsd')
        
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
        
        self.assertRaises(XmlParseError, Xsd.validate, xml_fpath=self.xml_fpath, xsd_fpath=self.schema_fpath)


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
        
        self.assertRaises(InvalidXmlSchema, Xsd.validate, xml_fpath=self.xml_fpath, xsd_fpath='/tmp/non_existant')

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestXsd),
    unittest.TestLoader().loadTestsFromTestCase(TestXmlParseError),
    ])

if __name__ == "__main__":
    import testing
    testing.main(suite)
