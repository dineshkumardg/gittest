import doctest

suite = doctest.DocFileSuite('test_generate_feed_report.py')

if __name__ == '__main__':
    doctest.testfile("test_generate_feed_report.py",  extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)


'''
>>> import os
>>> import glob
>>> import shutil
>>> from scripts.reports.feed_file.generate_feed_report import GenerateFeedReport 

>>> cwd = os.path.dirname(__file__)
>>> reports_folder = os.path.join(cwd, 'test_data/actual_csv')
>>> feedfiles_folder = os.path.join(cwd, 'test_data/actual_gz')
>>> expected_csv = os.path.join(cwd, 'test_data/expected_csv/feed_PSM-CHOA_20130726_158.csv')

>>> os.mkdir(reports_folder)

>>> feed = GenerateFeedReport(reports_folder, feedfiles_folder)
>>> feed.clean_up()
>>> feed.check_dir()
>>> feed.copy_local_files()
['PSM-CHOA_20130726_158.xml.gz']

>>> feed.unzip_files()
>>> xml_files = glob.glob(feed.xml_dir + '/*.xml')
>>> for xml_file in xml_files:
...     feed.xml_name = xml_file
...     feed.split_xml()
...     feed.process_xml()
feed file report generated

>>> feed.clean_up()  # doesn't work on windows

>>> output_csv = os.path.join(reports_folder, 'feed_PSM-CHOA_20130726_158.csv')
>>> os.path.isfile(output_csv)
True

>>> output_csv_f = open(output_csv, 'r')
>>> expected_csv_f = open(expected_csv, 'r')
>>> output_csv_f.read() == expected_csv_f.read()
True

>>> output_csv_f.close()
>>> expected_csv_f.close()

>>> shutil.rmtree(reports_folder)

'''
