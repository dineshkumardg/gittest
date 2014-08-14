#!python -m doctest -v test_delivery_manifest.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.

import doctest

suite = doctest.DocFileSuite('test_doc_factory.py')

if __name__ == '__main__':
    doctest.testfile("test_doc_factory.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)


'''
>>> from cStringIO import StringIO
>>> from lxml import etree
>>> from gaia.xml.xml_dict import XmlDict
>>> from project.cho.egest_adapter.doc.doc_factory import DocFactory

# Test which builders are recognised

# Meetings ###############################################
>>> xml = """<chapter>
...     <metadataInfo>
...         <productContentType>Meetings</productContentType>
...     </metadataInfo>
...     <citation>
...         <meeting>
...             <etc/>
...         </meeting>
...     </citation>
... </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Meetings

# Conference Series ###############################################
>>> xml = """<chapter>
...     <metadataInfo>
...         <productContentType>Conference Series</productContentType>
...     </metadataInfo>
...     <citation>
...         <conference>
...             <etc/>
...         </conference>
...     </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Conference Series

# Pamphlets and Reports ###############################################
>>> xml = """<chapter>
...     <metadataInfo>
...         <productContentType>Pamphlets and Reports</productContentType>
...     </metadataInfo>
...     <citation>
...         <book>
...             <etc/>
...          </book>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Pamphlets and Reports

# Books ###############################################
>>> xml = """<chapter>
...      <metadataInfo>
...          <productContentType>Books</productContentType>
...      </metadataInfo>
...      <citation>
...          <book>
...              <etc/>
...          </book>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Books

# Special Publications/book (Refugee Survey) ###############################################
>>> xml = """<chapter>
...      <metadataInfo>
...          <productContentType>Special Publications</productContentType>
...      </metadataInfo>
...      <citation>
...          <book>
...              <etc/>
...          </book>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Special Publications/book

# Special Publications/journal (Weekly Review of Foreign Press) ###########################
>>> xml = """<chapter>
...      <metadataInfo>
...          <productContentType>Special Publications</productContentType>
...      </metadataInfo>
...      <citation>
...          <journal>
...              <etc/>
...          </journal>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Special Publications/journal

# Journals ###########################
>>> xml = """<chapter>
...      <metadataInfo>
...          <productContentType>Journals</productContentType>
...      </metadataInfo>
...      <citation>
...          <journal>
...              <etc/>
...          </journal>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Journals

# Survey and Documents Series ###########################
>>> xml = """<chapter>
...      <metadataInfo>
...          <productContentType>Survey and Documents Series</productContentType>
...      </metadataInfo>
...      <citation>
...          <book>
...              <etc/>
...          </book>
...      </citation>
...  </chapter>"""
>>> source_xml_dict = XmlDict(etree.parse(StringIO(xml)))
>>> print DocFactory._choose_builder(source_xml_dict)
Survey and Documents Series

'''
