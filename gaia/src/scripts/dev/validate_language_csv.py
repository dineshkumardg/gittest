import csv
import re
import datetime
import time
import os


class ValidateLanguageCSV:
    def __init__(self):
        self.current_path = os.path.dirname(__file__)
        self.csv_fpath = os.path.dirname(__file__) + '/../../project/cho/data/language_spread_sheet'
        self.csv_report_fpath = os.path.join('%s/,validate_languages_%s.csv' % (self.current_path, datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H_%M_%S')))

    def validate_language_csv(self):
        csv_file = open(self.csv_report_fpath,"w")
        out = csv.writer(csv_file, delimiter=';')
        out.writerow(["File_name", "Line_number", "Line_content", "Report"])

        psmid_reg = "cho_[a-z]{4}_([0-9-]+|[0-9-]+[a-zA-Z])_(\d{4}|\d{4}[a-z]|[a-zA-Z]+)_\d{3}_\d{4}"
        psmid_pattern = re.compile(psmid_reg)
        file_num = 0

        for root, dirs, files in os.walk(self.csv_fpath):
            for each_file in files:
                if each_file.endswith(".csv"):
                    file_path =  os.path.join(root, each_file)
                    print 'processing %s' % file_path

                    f = open(file_path, 'rb') # opens the csv file
                    row_num = 0  # to count the line number
                    col_num = 0  # columes number should be consistent for each file
                    file_num += 1
                    reader = csv.reader(f, delimiter=';')  # creates the reader object

                    for row in reader:# iterates the rows of the file in orders
                        row_num += 1

                        # check colume consistent
                        if col_num == 0:
                            col_num = len(row)
                        elif col_num != len(row):
                            out.writerow([each_file, row_num, row, "column number inconsistent"])

                        # check psmid match regulation expression 
                        if row_num > 1:
                            if re.match(psmid_pattern, row[0]):
                                pass
                            else:
                                out.writerow([each_file, row_num, row, "PSMID invalid"])
                else:
                    print " Please convert the file" + each_file + "into a csv before usiing this validation script"

        if file_num < 5:
            out.writerow(["one or more csv files missing"])

        csv_file.close()

#
# py ~/GIT_REPOS/gaia/src/scripts/dev/validate_language_csv.py
#
if __name__ == "__main__":
    print 'REMEMBER .xlsx files have to be converted in to .CSV file with delimiter ";" before using this validation\n'

    validate_language_CSV = ValidateLanguageCSV()
    validate_language_CSV.validate_language_csv()

    print '\nPlease see report file %s' % validate_language_CSV.csv_report_fpath
    print 'If there are no rows in the report file, then everything is good'
