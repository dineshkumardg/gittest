'''
Import data/* csv files into a language table
'''
import csv
import os
import psycopg2
import re
import sys
from optparse import OptionParser


def empty_table(options):
    connection = None
    try:
        connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (options.host, options.port, options.db, options.uid, options.pwd))
        cursor = connection.cursor()

        sql = 'DELETE FROM language;'
        print sql
        cursor.execute(sql)
        connection.commit()
    except Exception, e:
        print e
    finally:
        if connection:
            connection.close()


def import_language_data(options, csv_fname, delim=';'):
    print '\nSTART %s' % csv_fname
    sys.stdout.flush()

    connection = None
    row_count = 0

    mcode = None
    psmid = None
    publication_title = None

    psmid_pattern = re.compile('cho_[a-z]{4}_([0-9-]+|[0-9-]+[a-zA-Z])_(\d{4}|\d{4}[a-z]|[a-zA-Z]+)_\d{3}_\d{4}')

    try:
        connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (options.host, options.port, options.db, options.uid, options.pwd))
        cursor = connection.cursor()

        csv_fpath = os.path.join(os.path.dirname(__file__), 'data/%s' % csv_fname)
        csv_reader = csv.reader(open(csv_fpath, 'r'), skipinitialspace=True, delimiter=delim)

        for csv_row in csv_reader:
            row_count = row_count + 1

            # row_count in .csv == 1996
            if csv_fname == 'Conferences_NOT_COMPLETE_MISSING_ITEMS.csv':
                psmid, article_id, lang = _insert_conference_row(row_count, csv_row, cursor)

            # row_count in .csv == 33074
            if csv_fname == 'edited_books_NOT_COMPLETE_MISSING_ITEMS.csv':
                psmid, article_id, lang = _insert_conference_row(row_count, csv_row, cursor)  # same as conference

            # row_count in .csv == 3382
            if csv_fname == 'Meetings.csv':
                psmid, article_id, lang = _insert_meetings_row(row_count, csv_row, cursor)

            # row_count in .csv == 347
            if csv_fname == 'R&P_NOT_COMPLETE_MISSING_ITEMS.csv':
                psmid, article_id, lang = _insert_report_and_survey_row(row_count, csv_row, cursor)

            # row_count in .csv == 624
            if csv_fname == 'Refugee_Survey_NOT_COMPLETE_MISSING_ITEMS.csv':
                psmid, article_id, lang = _insert_refugee_survey_row(row_count, csv_row, cursor)  # same as conference

            # row_count in .csv == 14762
            if csv_fname == 'Survey_and_Document_Language.csv':
                psmid, article_id, lang = _insert_conference_row(row_count, csv_row, cursor)  # same as conference

            # quick cleanup
            psmid = psmid.strip()
            article_id = article_id.strip()
            article_id = int(article_id)
            lang = lang.strip()

            if re.match(psmid_pattern, psmid):
                # SH, 20140102: don't insert a duplicate - as there are some in the .xls / .csv files!
                cursor.execute('SELECT count(*) FROM language WHERE psmid = %s AND article_id = %s AND lang = %s', (psmid, article_id, lang))
                result = cursor.fetchone()
                number_of_rows = result[0]
                if number_of_rows == 0:
                    cursor.execute('INSERT INTO language (psmid, article_id, lang) VALUES (%s, %s, %s)', (psmid, article_id, lang))
            else:
                print 'ERROR reg. ex. %s' % psmid

            connection.commit()
    except Exception, e:
        print '------------------'
        print e
        print mcode
        print psmid
        print publication_title
    finally:
        if connection:
            connection.close()
        print 'END %s : %s' % (csv_fname, row_count)
        sys.stdout.flush()


def _insert_conference_row(row_count, csv_row, cursor):
    psmid = csv_row[0]

    article_id = csv_row[1]
    lang = csv_row[3]

    return psmid, article_id, lang


def _insert_refugee_survey_row(row_count, csv_row, cursor):
    psmid = csv_row[0]

    article_id = csv_row[2]
    lang = csv_row[4]

    return psmid, article_id, lang


def _insert_meetings_row(row_count, csv_row, cursor):
    psmid = csv_row[0]

    article_id = '1'
    lang = csv_row[3]

    return psmid, article_id, lang


def _insert_report_and_survey_row(row_count, csv_row, cursor):
    psmid = csv_row[0]

    article_id = '1'
    lang = csv_row[2]

    return psmid, article_id, lang

'''
py $HOME/GIT_REPOS/gaia/src/scripts/db/cho/language_import/language_import.py --host=127.0.0.1 --port=5433 --db=cho --uid=system_test --pwd=system_test
'''
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--host')
    parser.add_option('--db')
    parser.add_option('--port')
    parser.add_option('--uid')
    parser.add_option('--pwd')

    options, args = parser.parse_args()

    print options
    empty_table(options)

    import_language_data(options, 'Conferences_NOT_COMPLETE_MISSING_ITEMS.csv')
    import_language_data(options, 'edited_books_NOT_COMPLETE_MISSING_ITEMS.csv')
    import_language_data(options, 'Meetings.csv')
    import_language_data(options, 'R&P_NOT_COMPLETE_MISSING_ITEMS.csv')
    import_language_data(options, 'Refugee_Survey_NOT_COMPLETE_MISSING_ITEMS.csv')
    import_language_data(options, 'Survey_and_Document_Language.csv')
