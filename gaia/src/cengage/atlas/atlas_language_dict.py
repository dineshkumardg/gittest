import os
import csv


class AtlasLanguageDict():
    def __init__(self, csv_fname=os.path.join(os.path.dirname(__file__), 'lookup_Atlas_Language_ID.csv'), delimiter='|'):
        self.csv_fname = csv_fname
        self.delimiter = delimiter

    def __getitem__(self, key):
        _dict = csv.DictReader(open(self.csv_fname, 'rb'), delimiter=self.delimiter)

        for k in _dict:
            # TODO speak to Tushar about encopding - re: http://stackoverflow.com/questions/5552555/unicodedecodeerror-invalid-continuation-byte
            if k['ART_LANG'].decode('latin-1') == key:
                return k['Term_id ']
        return None
