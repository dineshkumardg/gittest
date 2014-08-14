from testing.gaia_django_test import GaiaDjangoTest
import os
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.review_foreign_press.test_review_foreign_press import TestReviewForeignPress
from project.cho.egest_adapter.doc.review_foreign_press import test_extra_args
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from gaia.xml.cached_xml_dict import CachedXmlDict
from lxml import etree
from StringIO import StringIO
from project.cho.egest_adapter.doc.review_foreign_press.article_review_foreign_press import ArticleReviewForeignPress
from qa.models import Language
from project.cho.egest_adapter.entity_reference import EntityReference


class TestArticleReviewForeignPress(TestReviewForeignPress):
    def test_cho_rfpx_1940C_0000_049_0000(self):  # http://jira.cengage.com/browse/CHOA-1013
        mcode = '4XCZ'
        dom_name = 'cho_rfpx_1940C_0000_049_0000'  # Special Publication: Journal
        publication_title = 'Review of the Foreign Press. Series C: U.S.S.R. Baltic States and the Far East'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        source_fname = os.path.join(os.path.dirname(__file__), '../../../test_samples/cho_rfpx_1940C_0000_049_0000.xml')
        test_extra_args.cho_rfpx_1940C_0000_042['illustrations'] = self._extra_args_binary_chunks(source_fname)

        expected_document_instances, actual_xml_escaped = self.create_article(dom_name, test_extra_args.cho_rfpx_1940C_0000_042, creation_date='20130416')
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)

        # ASSERT
        self._dump_to_file(dom_name, '_ARTICLE-actual.xml', actual_xml_escaped)
        self._dump_to_file(dom_name, '_ARTICLE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped)

    def test_cho_rfpx_1940C_0000_042_0000(self):  # http://jira.cengage.com/browse/CHOA-1013
        mcode = '4XCZ'
        dom_name = 'cho_rfpx_1940C_0000_042_0000'  # Special Publication: Journal
        publication_title = 'Review of the Foreign Press. Series C: U.S.S.R. Baltic States and the Far East'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        source_fname = os.path.join(os.path.dirname(__file__), '../../../test_samples/cho_rfpx_1940C_0000_042_0000.xml')
        test_extra_args.cho_rfpx_1940C_0000_042['illustrations'] = self._extra_args_binary_chunks(source_fname)

        expected_document_instances, actual_xml_escaped = self.create_article(dom_name, test_extra_args.cho_rfpx_1940C_0000_042, creation_date='20130416')
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)

        # ASSERT
        #self._dump_to_file(dom_name, '_ARTICLE-actual.xml', actual_xml_escaped)
        #self._dump_to_file(dom_name, '_ARTICLE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped)

    def test_cho_rfpx_1939B_0000_001_0000(self):
        mcode = '5XHZ'
        dom_name = 'cho_rfpx_1939B_0000_001_0000'  # Special Publication: Journal
        publication_title = 'Review of the Foreign Press. Series B: European Neutrals and the Near East'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_article(dom_name, test_extra_args.cho_rfpx_1939B_0000, creation_date='20130416')
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
        #self._dump_to_file(dom_name, '_ARTICLE-actual.xml', actual_xml_escaped)
        #self._dump_to_file(dom_name, '_ARTICLE-expected.xml', expected_document_instances)
        self.assertEqual(ChoNamespaces.remove_ns(expected_document_instances), actual_xml_escaped, 'notEqual')

    def test__meta_descriptive_indexing(self):
        # EXPECTATION
        expected_meta_descriptive_indexing = """<meta:descriptive-indexing xmlns:meta="http://www.gale.com/goldschema/metadata">
  <meta:indexing-term>
    <meta:term>
      <meta:term-type>DOC_INFO_TYPE</meta:term-type>
      <meta:term-source>Atlas</meta:term-source>
      <meta:term-id>21819391</meta:term-id>
      <meta:term-value>Journal</meta:term-value>
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
        <PSMID>1</PSMID>
        <productContentType>Special Publications</productContentType>
    </metadataInfo>
    <citation>
        <journal>
        </journal>
    </citation>
    <page>
        <article id='1' type='front_matter'>
            <articleInfo>
                <language ocr="English">English</language>
            </articleInfo>
        </article>
    </page>
</chapter>
"""
        language = Language(psmid='1', article_id='1', lang='English')
        language.save()

        source_xml_dict = CachedXmlDict(etree.parse(StringIO(source_xml)))
        extra_args = None
        document_instance = 1
        article_review_foreign_press = ArticleReviewForeignPress(self.config, source_xml_dict, extra_args)
        actual_meta_descriptive_indexing = article_review_foreign_press._meta_descriptive_indexing(document_instance)

        # ASSERT
        pretty_printed_actual = etree.tostring(actual_meta_descriptive_indexing, pretty_print=True)
        self.assertEqual(expected_meta_descriptive_indexing, pretty_printed_actual, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestArticleReviewForeignPress),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
