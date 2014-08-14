"""
RE: EG-353
"""
import argparse
import os
import logging
import sys
import csv
import psycopg2
import ntpath
from urllib2 import urlopen, URLError


# singleton
class Logger:
    _logger = None

    @classmethod
    def get_logger(cls, name, log_level):
        if cls._logger is None:
            cls._logger = logging.getLogger(name)
            cls._logger.setLevel(log_level)  # FATAL > ERROR > WARNING > INFO > DEBUG
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(logging.Formatter("%(asctime)s: %(levelname)s: %(lineno)s: %(message)s"))  # %(funcName)s, 
            cls._logger.addHandler(handler)
        return cls._logger


class GenerateAuthorReport:
    REQUIRED_COLUMNS = ['PSMID', 'Article Sequence']

    # by default we use development env args - but this requires sanity_meet.sh to have been run!
    def __init__(self, author_csv_fpath=None, delimiter='|', required_columns=REQUIRED_COLUMNS,
                 log_level=logging.INFO,
                 solr='127.0.0.1:8983',
                 host='127.0.0.1', port='5433', db='cho', uid='system_test', pwd='system_test'):
        self._author_csv_fpath_fpath = author_csv_fpath
        self._delimiter = delimiter
        self._required_columns = required_columns

        self._logger = Logger.get_logger(self.__class__.__name__, log_level)

        self._solr = solr

        self._host = host
        self._port = port
        self._db = db
        self._uid = uid
        self._pwd = pwd

        self._logger.info(self._author_csv_fpath_fpath)

        head, tail = ntpath.split(self._author_csv_fpath_fpath)
        self.csv_output_fname = '%s/,%s' % (head, tail)

    def _csv_file_exists(self):
        return os.path.isfile(self._author_csv_fpath_fpath) & self._author_csv_fpath_fpath.endswith('.csv')

    def _first_line_in_csv_file(self):
        csv_file = None
        try:
            csv_file = file(self._author_csv_fpath_fpath, 'r')
            csv_data = csv.reader(csv_file, delimiter=self._delimiter)
            return csv_data.next()
        except Exception:
            return []
        finally:
            if csv_file is not None:
                csv_file.close()

    def _csv_file_has_correct_delim(self):
        if set(self.REQUIRED_COLUMNS).issubset(set(self._first_line_in_csv_file())) is False:
            self._logger.error('Unable to understand csv delimiter')
            return False  # looks like delimiter might be wrong
        else:
            return True

    def _csv_file_has_required_columns(self):
        set_expected_columns = set(self._required_columns)
        set_first_line_in_csv = set(self._first_line_in_csv_file())

        if set_expected_columns.issubset(set_first_line_in_csv) is False:
            self._logger.error('Unable to find mandatory columns in csv file: %s' % self._required_columns)
            return False
        else:
            return True

    def csv_file_good(self):
        return self._csv_file_exists() & self._csv_file_has_correct_delim() & self._csv_file_has_required_columns()

    def _csv_file_required_column_indexes(self):
        header = self._first_line_in_csv_file()
        column_indexes = {}
        for required_column in self._required_columns:
            column_indexes[required_column] = header.index(required_column)

        return column_indexes  # i.e. {'Article Sequence': 2, 'PSMID': 0}

    def _retreive_required_column_data_from_csv_file(self):
        csv_file = None

        try:
            required_column_indexes = self._csv_file_required_column_indexes()

            self._logger.debug(self._author_csv_fpath_fpath)
            csv_file = file(self._author_csv_fpath_fpath, 'r')
            csv_data = csv.reader(csv_file, delimiter=self._delimiter)

            required_column_data = []
            csv_row_index = 1  # start at 1 for csv files, but 0 for py arrays
            for row in csv_data:
                columns_dict = {}
                columns_dict['csv_row_index'] = csv_row_index

                for key, value in required_column_indexes.items():
                    columns_dict[key] = row[value]

                required_column_data.append(columns_dict)
                csv_row_index += 1

            return required_column_data
        finally:
            if csv_file is not None:
                csv_file.close()

    def _distinct_psmids(self, actual_column_data_from_csv_file):
        distinct_psmid = []
        for row in actual_column_data_from_csv_file:
            row_psmid = row['PSMID']
            if row_psmid not in distinct_psmid and row_psmid != '':
                distinct_psmid.append(row_psmid)

        return distinct_psmid

    def _query_solr(self, psmid):
        if len(psmid) == 0:
            self._logger.error('SOLR: unable to find: %s' % psmid)
            return None

        _solr_query = 'doc_PSMID:%s&fl=doc_productContentType&rows=1' % psmid
        url = 'http://%s/solr/select?q=%s&wt=python' % (self._solr, _solr_query)
        self._logger.debug(url)

        try:
            solr_reponse = eval(urlopen(url).read())

            if solr_reponse['response']['numFound'] == 0:
                return None
            else:
                return solr_reponse['response']['docs'][0]['doc_productContentType']
        except URLError as e:
            self._logger.error(e)
            return None

    # the data's not in the GDOM, but instead in solr (and the raw xml & json files in the file system)
    def _retreive_psmid_product_content_type_from_solr(self, column_data_from_csv_file):
        # minimise solr hits
        distinct_psmid = self._distinct_psmids(column_data_from_csv_file)

        psmid_product_content_type_list = []

        for psmid in distinct_psmid:
            psmid_product_content_type_dict = {'psmid': psmid, 'product_content_type':  self._query_solr(psmid)}

            self._logger.debug(psmid_product_content_type_dict)
            psmid_product_content_type_list.append(psmid_product_content_type_dict)

        return psmid_product_content_type_list

    def _retreive_psmid_articleid_assetid_from_postgres(self, psmid_product_content_type_list):
        psmid_product_content_type_articleid_assetid_dict = {}

        connection = None
        try:
            connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (self._host, self._port, self._db, self._uid, self._pwd) )
            cursor = connection.cursor()

            for psmid_product_content_type in psmid_product_content_type_list:
                psmid = psmid_product_content_type['psmid']

                # this must come back in this order (with binary chunks), so that is matches gaia codebase behaviour
                sql = 'SELECT chunk.dom_id as article_sequence, chunk_final_id.final_id as assetid '
                sql += 'FROM public.chunk_final_id, public.chunk, public.document, public.item '
                sql += 'WHERE '
                sql += 'chunk_final_id.chunk_id = chunk.id AND '
                sql += 'chunk.document_id = document.id AND '
                sql += 'document.item_id = item.id AND '
                sql += 'item.is_live = True AND '
                sql += "document.dom_id = '%s' " % psmid
                sql += 'ORDER BY document.dom_id ASC, chunk.dom_id ASC;'

                self._logger.debug(sql)
                cursor.execute(sql)

                articleid = 1
                articleid_assetid_list = {}
                for article_sequence, assetid in cursor:
                    articleid_assetid_list[articleid] = assetid
                    articleid += 1

                if len(articleid_assetid_list) > 0:
                    psmid_product_content_type_articleid_assetid_dict[psmid] = {'product_content_type': psmid_product_content_type['product_content_type'],
                                                                                'articleid_assetid': articleid_assetid_list}

            return psmid_product_content_type_articleid_assetid_dict
        except Exception as e:
            self._logger.error(e)
            return None
        finally:
            if connection is not None:
                connection.close()

    def retreive_data_from_sources(self):
        column_data_from_csv_file = self._retreive_required_column_data_from_csv_file()
        psmid_product_content_type_from_solr = self._retreive_psmid_product_content_type_from_solr(column_data_from_csv_file)
        return self._retreive_psmid_articleid_assetid_from_postgres(psmid_product_content_type_from_solr)

    def insert_data_into_csv(self, psmid_articleid_assetid_product_content_type):
        csv_reader_file = file(self._author_csv_fpath_fpath, 'r')
        csv_reader = csv.reader(csv_reader_file, delimiter=self._delimiter)

        csv_writer_file = file(self.csv_output_fname, 'wb')
        csv_writer = csv.writer(csv_writer_file, delimiter=self._delimiter)

        sequence_except_msg = "csv_row_index=%s ;'Article Sequence' not known by GAIA - %s"
        book_level_except_msg = "csv_row_index=%s; 'Book Level' detected (ALL possible 'chunks' will be inserted underneath this row) - %s"

        # first row contains column headers
        csv_row_index = 1
        headers = csv_reader.next()
        self._write_row_to_csv_file(csv_writer, headers, 'Product Content Type', 'Asset ID')

        try:
            for row in csv_reader:
                csv_row_index += 1

                original_row_psmid = row[0]
                original_row_article_sequence = row[2]

                try:
                    product_content_type = psmid_articleid_assetid_product_content_type[original_row_psmid]['product_content_type']
                    assetid = psmid_articleid_assetid_product_content_type[original_row_psmid]['articleid_assetid'][int(original_row_article_sequence)]
                    self._write_row_to_csv_file(csv_writer, row, product_content_type, assetid)
                except IndexError as e:
                    self._logger.warn(sequence_except_msg % (csv_row_index, original_row_psmid))
                    self._write_row_to_csv_file(csv_writer, row, product_content_type, '')
                except KeyError as e:
                    self._logger.warn(sequence_except_msg % (csv_row_index, original_row_psmid))
                    self._write_row_to_csv_file(csv_writer, row, product_content_type, '')
                except ValueError as e:
                    # assume! its a 'Book Level' issue
                    self._logger.warn(book_level_except_msg % (csv_row_index, original_row_psmid))
                    self._write_row_to_csv_file(csv_writer, row, product_content_type, '')  # we keep the row that says 'Book Level'

                    for article_sequence, assetid in psmid_articleid_assetid_product_content_type[original_row_psmid]['articleid_assetid'].iteritems():
                        new_row = [product_content_type, assetid, original_row_psmid, '', article_sequence]
                        self._logger.info('INSERT: ' + str(new_row))
                        csv_writer.writerow(new_row)

            self._logger.info('SUCCESS: %s' % self.csv_output_fname)
        finally:
            csv_reader_file.close()
            csv_writer_file.close()

    def _write_row_to_csv_file(self, csv_writer, row, product_content_type, assetid):
        row.insert(0, product_content_type)
        row.insert(1, assetid)
        self._logger.debug('UPDATE: ' + str(row))
        csv_writer.writerow(row)

"""
python $HOME/GIT_REPOS/gaia/src/scripts/reports/author/generate_author_report.py --author_csv_file=$HOME/GIT_REPOS/gaia/src/scripts/reports/author/test_data/Consolidated_Author_Extract_Report_small.csv
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Takes an author csv file with assetId | productContentType columns & rows; expects %s columns to exist (in correct position) and delimter to be |' % GenerateAuthorReport.REQUIRED_COLUMNS)
    parser.add_argument('--author_csv_file', help='full path to the original author csv file; use quote marks at start & end if whitespace present')

    args = parser.parse_args()
    if args.author_csv_file == None:
        parser.print_help()
    else:
        # production settings
        generate_author_report = GenerateAuthorReport(args.author_csv_file,
                                                      #log_level=logging.DEBUG,
                                                      solr='10.179.176.181:8983',
                                                      host='10.179.176.181', port='5432', db='cho', uid='gaia', pwd='g818')
        generate_author_report._logger.info('STARTED')

        if generate_author_report.csv_file_good() == True:
            data_retreived_from_sources = generate_author_report.retreive_data_from_sources()
            generate_author_report.insert_data_into_csv(data_retreived_from_sources)

        generate_author_report._logger.info('FINISHED')
