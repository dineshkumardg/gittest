from testing.gaia_django_test import GaiaDjangoTest
django_test = GaiaDjangoTest()
django_test.setUp()


import unittest
from project.cho.egest_adapter.doc.conference_series.test_conference_series import TestConferenceSeries
from project.cho.egest_adapter.cho_namespaces import ChoNamespaces
from project.cho.egest_adapter.doc.conference_series import test_extra_args
from project.cho.egest_adapter.doc.conference_series.parent_conference_series import ParentConferenceSeries
from project.cho.egest_adapter.doc.document_error import DocumentError
from mock import Mock
from project.cho.egest_adapter.entity_reference import EntityReference


# Chatham House Conversion Spec v1.0_Issue-volume record.xlsx
class TestParentConferenceSeries(TestConferenceSeries):
    def test_cho_bcrc_1965_0000_000_0000_INVALID_LEVEL(self):
        '''
        1
        1
            2
                3
        1
                3            <- problem, should raise an DocumentError
        1
            2
            2
                3
                    4
        '''
        try:
            mcode = '4XHZ'
            dom_name = 'cho_bcrc_1965_0000_000_0000'
            publication_title = 'British Commonwealth Relations 7th Conference, New Delhi, India, 1965. Proceedings'
            self._create_mcode_for_psmid(mcode, dom_name, publication_title)

            parent_conference = self._create_document_instances('cho_bcrc_1965_0000_000_0000_INVALID_LEVEL.xml', ParentConferenceSeries, test_extra_args.cho_bcrc_1965)
            parent_conference._language_correction = Mock(return_value=['English'])
            parent_conference.document_instances()[0]
            self.fail('no exception raised')
        except DocumentError, e:
            if e.msg != 'etoc level must be sequential':
                self.fail('no exception raised')
            else:
                pass

    def test_cho_iprx_1933_0001_001_0000(self):
        '''
        1
        1
            2
                3
        1
        '''

        # EXPECTATION / TEST
        mcode = '4XJF'
        dom_name = 'cho_iprx_1933_0001_001_0000'
        publication_title = 'Institute of Pacific Relations 5th Conference, Banff, Alberta, Canada, 1933. Vol. 1: Central Secretariat Papers'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.bcrc_1933_0001)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances.decode('utf-8'))
        self.assertEqual(expected_document_instances.decode('utf-8'), actual_xml_escaped, 'notEqual')

    def test_cho_bcrc_1938_cleeve_001_0000(self):
        '''
        1
            2
            2
                3
                3
                    4
                        5
            2
            2
                3
                    4
        '''

        # EXPECTATION / TEST
        mcode = '4XGV'
        dom_name = 'cho_bcrc_1938_cleeve_001_0000'
        publication_title = 'British Commonwealth Relations 2nd Conference, Sydney, Australia, 1938. Selected bibliography, addendum'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.bcrc_1938_cleeve_001)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')

    def test_cho_bcrc_1933_0001_000_0000(self):
        # Regression test from system tests for where - in meta_editors - there arn't any editors
        # EXPECTATION / TEST
        dom_name = ''
        mcode = '4XFN'
        dom_name = 'cho_bcrc_1933_0001_000_0000'
        publication_title = 'British Commonwealth Relations 1st Conference, Toronto, Ontario, Canada, 1933. Verbatim Papers, vol. 1'
        self._create_mcode_for_psmid(mcode, dom_name, publication_title)

        expected_document_instances, actual_xml_escaped = self.create_parent(dom_name, test_extra_args.bcrc_1933_0001)
        actual_xml_escaped = ChoNamespaces.remove_ns(actual_xml_escaped)
        actual_xml_escaped = EntityReference.prepare_for_lst(actual_xml_escaped)

        # ASSERT
#        self._dump_to_file(dom_name, '_PARENT-actual.xml', actual_xml_escaped)
#        self._dump_to_file(dom_name, '_PARENT-expected.xml', expected_document_instances)
        self.assertEqual(expected_document_instances, actual_xml_escaped, 'notEqual')


suite = unittest.TestSuite([
    unittest.TestLoader().loadTestsFromTestCase(TestParentConferenceSeries),
    ])

django_test.tearDown()

if __name__ == "__main__":
    import testing
    testing.main(suite)
