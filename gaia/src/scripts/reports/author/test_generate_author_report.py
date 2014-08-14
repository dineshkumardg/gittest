import os
import unittest
import filecmp
from test_utils.gaia_test import GaiaTest
from scripts.reports.author.generate_author_report import GenerateAuthorReport
from mock import MagicMock


class TestGenerateAuthorReport(GaiaTest):
    maxDiff = None

    def setUp(self):
        GaiaTest.setUp(self)
        self._test_data_csv_fname = os.path.join(os.path.dirname(__file__), 'test_data/Consolidated_Author_Extract_Report.csv')
        self._test_data_xls_fname = os.path.join(os.path.dirname(__file__), 'test_data/Consolidated_Author_Extract_Report.xls')
        self._test_data_csv_290813_fname = os.path.join(os.path.dirname(__file__), 'test_data/Consolidated_Author_Extract_Report 290813.csv')

        self._test_data_small_csv_fname = os.path.join(os.path.dirname(__file__), 'test_data/Consolidated_Author_Extract_Report_small.csv')
        self._test_data_small_postgres = {'cho_book_1940_0000_001_0000':
                                              {'articleid_assetid':
                                                   {1: 'LRTBRJ999852333',
                                                    2: 'XYHKYZ145618031',
                                                    3: 'FYLQKR304981122',
                                                    4: 'VHNSAV102414365',
                                                    5: 'VSVKNV541634623',
                                                    6: 'SVMBQA690611846',
                                                    7: 'AGEBWE313455247',
                                                    8: 'EWUTET197090103',
                                                    9: 'NDBGYP948852187',
                                                    10: 'BJDHZS530488584',
                                                    11: 'VEPCRH614051849',
                                                    12: 'VFSDKN960983082',
                                                    13: 'TBVVJY225968528',
                                                    14: 'HCPNVI324416661',
                                                    15: 'LLHUMG025787492',
                                                    16: 'SQBGMV467070527'},
                                               'product_content_type': 'Books'},
                                          'cho_book_1970_cosgrove_000_0000':
                                              {'articleid_assetid':
                                                   {1: 'HNRZBF767642820',
                                                    2: 'WMVPRV989596489',
                                                    3: 'SGKSDP699960323',
                                                    4: 'DSUQJC584877520',
                                                    5: 'PARSAH782049285',
                                                    6: 'WHVPWH635125629',
                                                    7: 'NZMDDK986340136',
                                                    8: 'DEGOKK042695545',
                                                    9: 'IGVPGT544765704',
                                                    10: 'XRSIWT718797953',
                                                    11: 'TCKTWE120216395',
                                                    12: 'NHRKTV111230022',
                                                    13: 'ZPXRNH457171781',
                                                    14: 'WGJURZ865936144'},
                                               'product_content_type': 'Books'},
                                          'cho_book_1950_mclachlan_000_0000':
                                              {'articleid_assetid':
                                                   {1: 'ERNTMW370255362',
                                                    2: 'HJJOPE412732288',
                                                    3: 'CMOMHI029372086',
                                                    4: 'VSQOAX195190407',
                                                    5: 'UAYPFA813295704',
                                                    6: 'JGPLIQ630584586',
                                                    7: 'YEGYAR813514451',
                                                    8: 'MWDYJA333319999',
                                                    9: 'CULVBW583302787',
                                                    10: 'CTSWWM999172542',
                                                    11: 'CSMXKW737841842',
                                                    12: 'VABMWR395396369',
                                                    13: 'USNINN647045556',
                                                    14: 'XXNPBB984773523',
                                                    15: 'DCLKGM935087511',
                                                    16: 'YPQPPX363818004',
                                                    17: 'NBHRJN456651762',
                                                    18: 'HPBDOG723331278',
                                                    19: 'RVXOCV952615217',
                                                    20: 'BBJKMZ034550177',
                                                    21: 'ZZRKNE034898928'},
                                               'product_content_type': 'Books'},
                                          'cho_book_1931_0000_001_0000':
                                              {'articleid_assetid':
                                                   {1: 'SXBWCA324506771',
                                                    2: 'MPXEIO935060819',
                                                    3: 'PJIBLV871358750',
                                                    4: 'VGXDRI405381350',
                                                    5: 'QFLMSJ382929248',
                                                    6: 'YSLAVL712663596',
                                                    7: 'HPXGKR535776524',
                                                    8: 'PRDUOG578237927',
                                                    9: 'EIURME812589680',
                                                    10: 'YCTBTB736723261',
                                                    11: 'WYHORO177347095',
                                                    12: 'ENDLER677650555',
                                                    13: 'XCZDDS719012329',
                                                    14: 'JKEOMI241082687',
                                                    15: 'MWEBTT341318081',
                                                    16: 'SDIEVG943330743',
                                                    17: 'TIRCZB777322352',
                                                    18: 'JJKLSI844339819',
                                                    19: 'STIQOK154779078',
                                                    20: 'RVSXUR433828372',
                                                    21: 'FDWPBB550621275',
                                                    22: 'ZPPTYJ535645057',
                                                    23: 'QSWRGF167359736',
                                                    24: 'CKUGFG390257065',
                                                    25: 'JGGLOY396949909',
                                                    26: 'DBEYBS072373318',
                                                    27: 'GOXADA225306144',
                                                    28: 'IIKHDG950149123',
                                                    29: 'WOKOLL476084825',
                                                    30: 'YZQTQI788943891',
                                                    31: 'YEIWCG150650757',
                                                    32: 'RLKODL876564487',
                                                    33: 'TEDPJE683705037',
                                                    34: 'BCSIMX176654242',
                                                    35: 'DGWXMF040714151'},
                                               'product_content_type': 'Books'}}

#     def test__csv_file_does_not_exist(self):
#         generate_author_report = GenerateAuthorReport('a_non_existant_file')
#         self.assertFalse(generate_author_report._csv_file_exists())
# 
#     def test__csv_file_has_wrong_extension(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_xls_fname)
#         self.assertFalse(generate_author_report._csv_file_exists())
# 
#     def test__csv_file_exists(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         self.assertTrue(generate_author_report._csv_file_exists())
# 
#     def test__csv_file_contains_wrong_delim(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         generate_author_report._first_line_in_csv_file = MagicMock(return_value=['PSMID;column2'])
#         self.assertFalse(generate_author_report._csv_file_has_correct_delim())
# 
#     def test__csv_file_contains_recognised_delim(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         self.assertTrue(generate_author_report._csv_file_has_correct_delim())
# 
#     def test__csv_file_has_required_columns(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         self.assertTrue(generate_author_report._csv_file_has_required_columns())
# 
#     def test__csv_file_does_not_required_columns(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         generate_author_report._first_line_in_csv_file = MagicMock(return_value=['column1', 'column2'])
#         self.assertFalse(generate_author_report._csv_file_has_required_columns())
# 
#     def test_csv_file_good(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname)
#         self.assertTrue(generate_author_report.csv_file_good())
# 
#         generate_author_report = GenerateAuthorReport(self._test_data_xls_fname)
#         self.assertFalse(generate_author_report.csv_file_good())
# 
#     def test__retreive_required_column_data_from_csv_file(self):
#         # Expectation(s)
#         expected_csv_row_count = 80
#         expected_csv_row_index = 50
#         expected_csv_row_psmid = 'cho_book_1940_0000_001_0000'
#         expected_csv_row_article_sequence = '22'
# 
#         # Test(s)
#         generate_author_report = GenerateAuthorReport(self._test_data_small_csv_fname)
#         actual_column_data = generate_author_report._retreive_required_column_data_from_csv_file()
#         actual_csv_row_index = actual_column_data[49]['csv_row_index']
#         actual_csv_row_psmid = actual_column_data[49]['PSMID']
#         actual_csv_row_article_sequence = actual_column_data[49]['Article Sequence']
# 
#         # Assert(s)
#         self.assertEquals(expected_csv_row_count, len(actual_column_data))
#         self.assertEquals(expected_csv_row_index, actual_csv_row_index)
#         self.assertEquals(expected_csv_row_psmid, actual_csv_row_psmid)
#         self.assertEquals(expected_csv_row_article_sequence, actual_csv_row_article_sequence)
# 
#     # use production or else assetid's will always be different!
#     def test__retreive_product_content_type_from_solr_PRODUCTION(self):
#         expected_psmid_product_content_type_from_solr = [{'product_content_type': None, 'psmid': 'PSMID'},
#                                                          {'product_content_type': 'Books', 'psmid': 'cho_book_1931_0000_001_0000'},
#                                                          {'product_content_type': 'Books', 'psmid': 'cho_book_1940_0000_001_0000'},
#                                                          {'product_content_type': 'Books', 'psmid': 'cho_book_1950_mclachlan_000_0000'},
#                                                          {'product_content_type': 'Books', 'psmid': 'cho_book_1970_cosgrove_000_0000'}]
# 
#         generate_author_report = GenerateAuthorReport(self._test_data_small_csv_fname,
#                                                       solr='10.179.176.181:8983')
#         column_data_from_csv_file = generate_author_report._retreive_required_column_data_from_csv_file()
#         actual_psmid_product_content_type_from_solr = generate_author_report._retreive_psmid_product_content_type_from_solr(column_data_from_csv_file)
# 
#         self.assertListEqual(expected_psmid_product_content_type_from_solr, actual_psmid_product_content_type_from_solr)
# 
#     def test__retreive_psmid_articleid_assetid_from_postgres(self):
#         expected_psmid_articleid_assetid_from_postgres = self._test_data_small_postgres['cho_book_1931_0000_001_0000']['articleid_assetid']
# 
#         generate_author_report = GenerateAuthorReport(self._test_data_small_csv_fname,
#                                                       host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
#         column_data_from_csv_file = generate_author_report._retreive_required_column_data_from_csv_file()
#         psmid_product_content_type_from_solr = [{'product_content_type': None, 'psmid': 'PSMID'},
#                                                 {'product_content_type': 'Books', 'psmid': 'cho_book_1931_0000_001_0000'},
#                                                 {'product_content_type': 'Books', 'psmid': 'cho_book_1940_0000_001_0000'},
#                                                 {'product_content_type': 'Books', 'psmid': 'cho_book_1950_mclachlan_000_0000'},
#                                                 {'product_content_type': 'Books', 'psmid': 'cho_book_1970_cosgrove_000_0000'}]
# 
#         actual_psmid_articleid_assetid_from_postgres = generate_author_report._retreive_psmid_articleid_assetid_from_postgres(psmid_product_content_type_from_solr)
# 
#         self.assertItemsEqual(expected_psmid_articleid_assetid_from_postgres, actual_psmid_articleid_assetid_from_postgres['cho_book_1931_0000_001_0000']['articleid_assetid'])
# 
#     def test_retreive_data_from_sources(self):
#         expected_psmid_articleid_assetid_from_postgres = self._test_data_small_postgres
# 
#         generate_author_report = GenerateAuthorReport(self._test_data_small_csv_fname,
#                                                       solr='10.179.176.181:8983',
#                                                       host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
#         actual_data_retreived_from_sources = generate_author_report.retreive_data_from_sources()
# 
#         self.assertItemsEqual(expected_psmid_articleid_assetid_from_postgres, actual_data_retreived_from_sources)
# 
    def test_insert_data_csv_small(self):
        expected_output_fname = '%s.expected' % self._test_data_small_csv_fname
 
        generate_author_report = GenerateAuthorReport(self._test_data_small_csv_fname,
                                                      solr='10.179.176.181:8983',
                                                      host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
        data_retreived_from_sources = generate_author_report.retreive_data_from_sources()
        generate_author_report.insert_data_into_csv(data_retreived_from_sources)
 
        self.assertTrue(filecmp.cmp(expected_output_fname, generate_author_report.csv_output_fname))
#
#     def test_insert_data_csv(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_fname,
#                                                       solr='10.179.176.181:8983',
#                                                       host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
#         data_retreived_from_sources = generate_author_report.retreive_data_from_sources()
#         generate_author_report.insert_data_into_csv(data_retreived_from_sources)
# 
#     def test_insert_data_csv_290813_fname(self):
#         generate_author_report = GenerateAuthorReport(self._test_data_csv_290813_fname,
#                                                       solr='10.179.176.181:8983',
#                                                       host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
#         data_retreived_from_sources = generate_author_report.retreive_data_from_sources()
#         generate_author_report.insert_data_into_csv(data_retreived_from_sources)


suite = unittest.TestSuite([unittest.TestLoader().loadTestsFromTestCase(TestGenerateAuthorReport),])
