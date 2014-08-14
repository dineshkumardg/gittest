'''
Import data/* csv files into a m_code table
'''
import csv
import os
import psycopg2
from optparse import OptionParser


def empty_table(options):
    connection = None
    try:
        connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (options.host, options.port, options.db, options.uid, options.pwd) )
        cursor = connection.cursor()

        sql = 'DELETE FROM m_codes;'
        print sql
        cursor.execute(sql)
        connection.commit()
    except Exception, e:
        print e
    finally:
        if connection:
            connection.close()


def import_mcode_data(options, csv_fname):
    print '\nSTART %s' % csv_fname

    connection = None
    row_count = 0

    mcode = None
    psmid = None
    publication_title = None

    try:
        connection = psycopg2.connect("host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (options.host, options.port, options.db, options.uid, options.pwd) )
        cursor = connection.cursor()

        csv_books_fname = os.path.join(os.path.dirname(__file__), 'data/%s' % csv_fname)
        csv_reader = csv.reader(open(csv_books_fname, 'r'), delimiter=',')

        for row in csv_reader:
            row_count = row_count + 1
            mcode = _clean_data(row[0])
            psmid = _clean_data(row[1])
            publication_title = _clean_data(row[2])

#             print row_count
#             print mcode
#             print psmid
#             print publication_title

            if mcode is None or len(mcode) == 0:
                print 'MISSING: mcode: %s: %s' % (csv_fname, row_count) 
            if psmid is None or len(psmid) == 0:
                print 'MISSING: psmid: %s: %s' % (csv_fname, row_count)
            if publication_title is None or len(publication_title) == 0:
                print 'MISSING: publication_title: %s: %s' % (csv_fname, row_count)

            sql = 'INSERT INTO m_codes (mcode, psmid, publication_title) VALUES (%s, %s, %s)'
            cursor.execute(sql, (mcode, psmid,  publication_title))
            connection.commit()
    except Exception, e:
        print e
        print mcode
        print psmid
        print publication_title
    finally:
        if connection:
            connection.close()
        print 'END %s : %s' % (csv_fname, row_count)


def _clean_data(original_data):
    ascii = unicode(original_data, 'latin-1').encode('ascii','ignore')  # get rid of unicode chars
    ascii = ascii.lstrip()
    ascii = ascii.rstrip()
    return ascii

'''
py ~/GIT_REPOS/gaia/src/scripts/db/cho/mcode_import/mcode_import.py --host=127.0.0.1 --port=5433 --db=cho --uid=system_test --pwd=system_test
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
    import_mcode_data(options, 'books.csv')
    import_mcode_data(options, 'byil.csv')
    import_mcode_data(options, 'conference_series.csv')
    import_mcode_data(options, 'journals.csv')
    import_mcode_data(options, 'refugee_survey.csv')
    import_mcode_data(options, 'review_of_foreign_press.csv')
    import_mcode_data(options, 's_and_d.csv')
