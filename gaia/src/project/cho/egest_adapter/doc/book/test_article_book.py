from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from lxml import etree
from StringIO import StringIO
from project.cho.egest_adapter.doc.book.test_book import TestBook
from project.cho.egest_adapter.doc.book import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.book.article_book import ArticleBook
from gaia.xml.cached_xml_dict import CachedXmlDict
from qa.models import Language
from project.cho.egest_adapter.entity_reference import EntityReference


class TestArticleBook(TestBook):
    def test_cho_book_1929_heald_000_0000(self):
        mcode = 'XXXX'
        dom_name = 'cho_book_1929_heald_000_0000'
        publication_title = 'A Directory of Societies and Organizations in Great Britain Concerned with the Study of International Affairs'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        for i in range(1, 77):
            language = Language(psmid=dom_name, article_id=i, lang='English')
            language.save()

        expected_document_instances, actual_xml_escaped = self.create_article(dom_name, test_extra_args.cho_book_1929)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#         self._dump_to_file(dom_name, '_ARTICLE-actual.xml', actual_xml_escaped)
#         self._dump_to_file(dom_name, '_ARTICLE-expected.xml', expected_document_instances.decode('utf-8'))
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped.encode('utf-8'), 'notEqual')

    def test__meta_descriptive_indexing(self):
        # EXPECTATION
        expected_meta_descriptive_indexing = """<meta:descriptive-indexing xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>DOC_INFO_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>14186620</meta:term-id>
      <meta:term-value>Monograph</meta:term-value>
    </meta:term>
  </meta:indexing-term>
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>DOC_INFO_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>21817803</meta:term-id>
      <meta:term-value>Front matter</meta:term-value>
    </meta:term>
  </meta:indexing-term>
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>CONT_REC_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>17234672</meta:term-id>
      <meta:term-value>Text</meta:term-value>
    </meta:term>
  </meta:indexing-term>
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>CONT_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>21901547</meta:term-id>
      <meta:term-value>DVI-Periodical</meta:term-value>
    </meta:term>
  </meta:indexing-term>
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>FUNC_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>21787856</meta:term-id>
      <meta:term-value>Issue-volume article record</meta:term-value>
    </meta:term>
  </meta:indexing-term>
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>ART_LANG</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>13858590</meta:term-id>
      <meta:term-value>English</meta:term-value>
    </meta:term>
  </meta:indexing-term>
</meta:descriptive-indexing>
"""

        # TEST
        source_xml = """<chapter>
    <metadataInfo>
        <PSMID>cho_book_1953_0003_000_0000</PSMID>
        <productContentType>Books</productContentType>
    </metadataInfo>
    <page>
        <article id='1' type='front_matter'>
            <articleInfo>
                <language ocr="English">English</language>
            </articleInfo>
        </article>
    </page>
</chapter>
"""
        language = Language(psmid='cho_book_1953_0003_000_0000', article_id='1', lang='English')
        language.save()
        language = Language(psmid='cho_book_1953_0003_000_0000', article_id='2', lang='English')
        language.save()
        language = Language(psmid='cho_book_1953_0003_000_0000', article_id='3', lang='English')
        language.save()

        source_xml_dict = CachedXmlDict(etree.parse(StringIO(source_xml)))
        extra_args = None
        document_instance = 1
        article_book = ArticleBook(self.config, source_xml_dict, extra_args)
        actual_meta_descriptive_indexing = article_book._meta_descriptive_indexing(document_instance)

        # ASSERT
        pretty_printed_actual = etree.tostring(actual_meta_descriptive_indexing, pretty_print=True)
        self.assertEqual(expected_meta_descriptive_indexing, pretty_printed_actual, 'notEqual')

suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestArticleBook),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
