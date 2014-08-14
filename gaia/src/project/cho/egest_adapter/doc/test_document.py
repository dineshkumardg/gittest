from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


from project.cho.egest_adapter.doc.test_document_helper import TestDocumentHelper
from lxml import etree
from project.cho.egest_adapter.doc.document import Document
import unittest
from project.cho.egest_adapter.doc.document_error import DocumentError
import os
from gaia.xml.xml_dict import XmlDict
from cStringIO import StringIO


class TestDocument(TestDocumentHelper):
    def test__page_article_illustration_pgrefs(self):
        # EXPECTATAION
        expected_page_article_illustration_pgrefs = [
            {'index_article': 1, 'index_illustration': 1, 'illustration_pgref': u'1', 'caption': u'HELP!', 'index_page': 1, 'type': u'line_drawing'},
            {'index_article': 1, 'index_illustration': 2, 'illustration_pgref': u'1', 'caption': None, 'index_page': 1, 'type': u'line_drawing'},
            {'index_article': 1, 'index_illustration': 3, 'illustration_pgref': u'2', 'caption': u'Illustration 2', 'index_page': 1, 'type': u'line_drawing'}
             ]

        # TEST
        source_xml_dict, extra_args = self._document(extra_args={})

        source_fname = os.path.join(os.path.dirname(__file__), '../../test_samples/cho_iprx_1933_0001_001_0000.xml')  # TODO figure out a way to use StringIO instead?
        extra_args['illustrations'] = self._extra_args_binary_chunks(source_fname)

        document = Document(self.config, source_xml_dict, extra_args)
        actual_page_article_illustration_pgrefs = document._page_article_illustration_pgrefs()

        # ASSERT
        self.assertEqual(expected_page_article_illustration_pgrefs, actual_page_article_illustration_pgrefs, 'notEqual')

    def test__meta_document_titles_rules_htc_escaped_from_source(self):  # demonstrates lxml behaviour at runtime
        expected = 'Start End'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)

        xml = """<chapter>
<title>Start&#x2010;End</title>
<title>Start&#x2012;End</title>
<title>Start&#x2013;End</title>
<title>Start&#x2014;End</title>
<title>Start&#x2015;End</title>
<title>Start&#x02BC;End</title>
</chapter>
"""
        tree = etree.parse(StringIO(xml))
        xml_dict = XmlDict(tree)

        actual = document._meta_document_titles_rules(xml_dict['/chapter/title[1]'])
        self.assertEqual(expected, actual)

        actual = document._meta_document_titles_rules(xml_dict['/chapter/title[2]'])
        self.assertEqual(expected, actual)

        actual = document._meta_document_titles_rules(xml_dict['/chapter/title[3]'])
        self.assertEqual(expected, actual)

        actual = document._meta_document_titles_rules(xml_dict['/chapter/title[4]'])
        self.assertEqual(expected, actual)

        actual = document._meta_document_titles_rules(xml_dict['/chapter/title[5]'])
        self.assertEqual(expected, actual)

    def test__meta_document_titles_rules_htc_escaped(self):
        expectation = 'Ghana The Politicians Return'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)

        # problem is that lxml has already convereted the entity into decimal, not hexidecimal - however we strip out both!
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2010; The &#8208; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2012; The &#8210; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2013; The &#8211; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2014; The &#8212; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2015; The &#8213; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2018; The &#8216; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x02BB; The &#699; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x275B; The &#10075; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2018; The &#8216; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x02BC; The &#699; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x275C; The &#10076; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201A; The &#8218; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201B; The &#8219; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x02BD; The &#701; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201C; The &#8220; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201F; The &#8223; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x275D; The &#10077; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x301D; The &#12317; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201D; The &#8221; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2033; The &#8243; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x275E; The &#10078; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x301E; The &#12318; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201E; The &#8222; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x301F; The &#12319; Politicians Return'))
        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x201F; The &#8223; Politicians Return'))

        self.assertEqual(expectation, document._meta_document_titles_rules('Ghana &#x2013; The &#8211; Politicians Return'))

    def test__meta_document_titles_rules_an(self):
        # defect spotted by QAI http://jira.cengage.com/browse/CHOA-401
        expectation = 'A The American Christian View of the Future of World Order'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('An A The American Christian View of the Future of World Order')

        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_a(self):
        expectation = 'An Christian View of the Future of World Order'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('A An Christian View of the Future of World Order')

        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_the(self):
        expectation = 'An A Christian View of the Future of World Order'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('The An A Christian View of the Future of World Order')

        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_the_with_double_quote(self):  # http://jira.cengage.com/browse/CHOA-645
        expectation = 'Dominions and Foreign Affairs'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('&quot;The Dominions and Foreign Affairs&quot;')  # not via xml_dict
        self.assertEqual(expectation, actual)

        # simulate via xml_dict - see test_xml_dict.py
        actual = document._meta_document_titles_rules('"The Dominions and Foreign Affairs"')
        self.assertEqual(expectation, actual)

        # have lots of (xml_dict) double quotes
        actual = document._meta_document_titles_rules('"Th"e "Dominions" and Fo"reign """Affairs"')
        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_the_with_single_quote(self):
        expectation = 'Dominions and Foreign Affairs'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('&apos;The Dominions and Foreign Affairs&apos;')  # not via xml_dict
        self.assertEqual(expectation, actual)

        # simulate via xml_dict - see test_xml_dict.py
        actual = document._meta_document_titles_rules("'The Dominions and Foreign Affairs'")
        self.assertEqual(expectation, actual)

        # go mad and have lots (xml_dict) of single quotes
        actual = document._meta_document_titles_rules("'The' Dominions' a'nd Foreign' Aff'airs'")
        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_trailing_comma(self):
        expectation = 'Goodbye trailing commas'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('Goodbye trailing commas,,,,')

        self.assertEqual(expectation, actual)

    def test__meta_document_titles_rules_full_stops(self):
        expectation = 'Goodbye trailing full stops'

        source_xml_dict, extra_args = self._document()
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document._meta_document_titles_rules('Goodbye trailing full stops...')

        self.assertEqual(expectation, actual)
        self.assertEqual(expectation, actual)

    def test_single_isbn(self):
        expectation = '''<meta:bibliographic-ids xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:id type="PSM">
    <meta:value>blah</meta:value>
  </meta:id>
  <meta:id type="isbn">
    <meta:value>0 19 285056 3</meta:value>
  </meta:id>
  <meta:id type="issn">
    <meta:value>1234-5678</meta:value>
  </meta:id>
</meta:bibliographic-ids>
'''

        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
        <isbn length="10">0 19 285056 3</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        source_xml_dict, extra_args = self._document(xml=source)
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document.meta_bibliographic_ids_psmid_isbn_issn()

        self.assertEqual(expectation, etree.tostring(actual, pretty_print=True))

    def test_two_isbn(self):
        expectation = '''<meta:bibliographic-ids xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:id type="PSM">
    <meta:value>blah</meta:value>
  </meta:id>
  <meta:id type="isbn">
    <meta:value>0 19 285056 3</meta:value>
  </meta:id>
  <meta:id type="isbn">
    <meta:value>0 19 215196 7 12 3</meta:value>
  </meta:id>
  <meta:id type="issn">
    <meta:value>1234-5678</meta:value>
  </meta:id>
</meta:bibliographic-ids>
'''

        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
            <isbn length="10">0 19 285056 3</isbn>
            <isbn length="13">0 19 215196 7 12 3</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        source_xml_dict, extra_args = self._document(xml=source)
        document = Document(self.config, source_xml_dict, extra_args)
        actual = document.meta_bibliographic_ids_psmid_isbn_issn()

        self.assertEqual(expectation, etree.tostring(actual, pretty_print=True))

    def test_two_same_length_isbn(self):
        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
            <isbn length="10">0 19 285056 3</isbn>
            <isbn length="10">0 19 215196 7</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        source_xml_dict, extra_args = self._document(xml=source)
        document = Document(self.config, source_xml_dict, extra_args)

        self.assertRaises(DocumentError, document.meta_bibliographic_ids_psmid_isbn_issn)

    def test__related_doc_display_link(self):
        # EXPECTATION
        expected_related_doc_display_link = "Document"
        
        # TEST
        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
            <isbn length="10">0 19 285056 3</isbn>
            <isbn length="10">0 19 215196 7</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        source_xml_dict, extra_args = self._document(xml=source)
        document = Document(self.config, source_xml_dict, extra_args)
        actual_related_doc_display_link = document._related_doc_display_link("Document")

        self.assertEqual(expected_related_doc_display_link, actual_related_doc_display_link)

    def test__vault_link_related_docs_missing(self):  # there are no extra_args['related_documents']
        # EXPECTATION
        expected_vault_link_related_docs = None

        # TEST
        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
        <isbn length="10">0 19 285056 3</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        extra_args = {
            'asset_id': {
                },
            }
        page_article_illustration_pgref = []

        source_xml_dict, extra_args = self._document(xml=source, extra_args=extra_args)
        document = Document(self.config, source_xml_dict, extra_args)
        actual_vault_link_related_docs = document._vault_link_related_docs(page_article_illustration_pgref)

        # ASSERT
        self.assertEqual(expected_vault_link_related_docs, actual_vault_link_related_docs)  # code should work with no relatedDocuments present

    def test__vault_link_related_docs(self):  # we should be able to produce two relatedDocument vault links
        # EXPECTATION
        expected_vault_link_related_docs = '''<vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
  <vault-link:link-type>external</vault-link:link-type>
  <vault-link:link-category term-id="19009864" term-source="Atlas">Related document</vault-link:link-category>
  <vault-link:action>point</vault-link:action>
  <vault-link:where>
    <vault-link:path>//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="asset_id_1"]</vault-link:path>
  </vault-link:where>
  <vault-link:select>
    <vault-link:document-nodes>
      <vault-link:target>ancestor::gift-doc:document</vault-link:target>
    </vault-link:document-nodes>
  </vault-link:select>
  <vault-link:display-point>//gift-doc:document/gift-doc:body/essay:div/essay:div/essay:complex-meta/meta:page-id-number="0123"</vault-link:display-point>
  <vault-link:display-link>value_1</vault-link:display-link>
</vault-link:vault-link>
<vault-link:vault-link xmlns:vault-link="http://www.gale.com/goldschema/vault-linking">
  <vault-link:link-type>external</vault-link:link-type>
  <vault-link:link-category term-id="19009864" term-source="Atlas">Related document</vault-link:link-category>
  <vault-link:action>point</vault-link:action>
  <vault-link:where>
    <vault-link:path>//gift-doc:document-metadata/meta:document-ids/meta:id[@type="Gale asset"]/meta:value[.="asset_id_2"]</vault-link:path>
  </vault-link:where>
  <vault-link:select>
    <vault-link:document-nodes>
      <vault-link:target>ancestor::gift-doc:document</vault-link:target>
    </vault-link:document-nodes>
  </vault-link:select>
  <vault-link:display-point>//gift-doc:document/gift-doc:body/essay:div/essay:div/essay:complex-meta/meta:page-id-number="0456"</vault-link:display-point>
  <vault-link:display-link>value_2</vault-link:display-link>
</vault-link:vault-link>
'''

        # TEST
        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
        <isbn length="10">0 19 285056 3</isbn>
        <issn>12345678</issn>
    </metadataInfo>
    <page id='1'>
        <article id='1'>
            <text>
                <textclip>
                    <relatedDocument type="footnote" docref="doc_ref_1" pgref="123" articleref="1">value_1</relatedDocument>
                    <relatedDocument type="footnote" docref="doc_ref_2" pgref="456" articleref="2">value_2</relatedDocument>
                </textclip>
            </text>
        </article>
    </page>
</chapter>'''
        extra_args =  {
            'asset_id': {
                },
            'illustrations': None,
            'related_documents': [({'/chapter/page[1]/article/text/textclip[1]/relatedDocument[1]/@docref': u'doc_ref_1',
                                 '/chapter/page[1]/article/text/textclip[1]/relatedDocument[1]/@pgref': u'123',
                                 '/chapter/page[1]/article/text/textclip[1]/relatedDocument[1]/@type': u'footnote',
                                 '_dom_id': 1,
                                 '_dom_name': u'value_1',
                                 '_source': {'chunk': 1, 'page': '2'},
                                 '_target': {'chunk': '2',
                                             'document': u'cho_diax_1962_0000_000_0000',
                                             'page': '3'}},
                                u'asset_id_1'),
                               ({'/chapter/page[1]/article/text/textclip[1]/relatedDocument[2]/@docref': u'doc_ref_2',
                                 '/chapter/page[1]/article/text/textclip[1]/relatedDocument[2]/@pgref': u'456',
                                 '/chapter/page[1]/article/text/textclip[1]/relatedDocument[2]/@type': u'footnote',
                                 '_dom_id': 2,
                                 '_dom_name': u'value_2',
                                 '_source': {'chunk': 6, 'page': '5'},
                                 '_target': {'chunk': '4',
                                             'document': u'cho_diax_1962_0000_000_0000',
                                             'page': '6'}},
                                u'asset_id_2')]
                }

        page_article_illustration_pgref = []

        source_xml_dict, extra_args = self._document(xml=source, extra_args=extra_args)
        document = Document(self.config, source_xml_dict, extra_args)

        page_article_illustration_pgref = {'textclip_index': 1, 'page_index': 1, 'article_id': 1, 'article_index': 1, 'pgref_value': 1}

        vault_link_related_docs = document._vault_link_related_docs(page_article_illustration_pgref)  # returns a list

        actual_vault_link_related_docs = ''
        for vault_link in vault_link_related_docs:
            actual_vault_link_related_docs += etree.tostring(vault_link, pretty_print=True)

        # ASSERT
        self.assertEqual(expected_vault_link_related_docs, actual_vault_link_related_docs)

    def test__validate_isbns(self):
        source = '''<chapter>
    <metadataInfo>
        <PSMID>blah</PSMID>
        <issn>12345678</issn>
    </metadataInfo>
    <page>p1</page>
</chapter>'''
        source_xml_dict, extra_args = self._document(xml=source)
        document = Document(self.config, source_xml_dict, extra_args)

        isbns =  [u'1-4051-2648-5', u'1-4051-2647-7', u'978-1-4051-2648-9', u'978-1-4051-2647-2']
        isbn_lengths = [10, 10, 13, 13]
        self.assertRaises(DocumentError, document._validate_isbns, isbns, isbn_lengths)

        isbns = [u'978 1 86203 188 3', u'978 1 86203 192 0', u'978 1 86203 193 7', u'978 1 86203 194 4']
        isbn_lengths = [13, 13, 13, 13]
        self.assertRaises(DocumentError, document._validate_isbns, isbns, isbn_lengths)

        isbns = [u'978 1 86203 176 0', u'1 86203 176 2']
        isbn_lengths = [13, 10]
        document._validate_isbns(isbns, isbn_lengths)


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestDocument),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
