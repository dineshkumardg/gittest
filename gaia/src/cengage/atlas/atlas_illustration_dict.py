from cengage.atlas.atlas_language_dict import AtlasLanguageDict
import csv
import os


class AtlasIllustrationDict(AtlasLanguageDict):
    def __init__(self, csv_fname=os.path.join(os.path.dirname(__file__), 'lookup_Atlas_Illustration.csv'), delimiter='|'):
        AtlasLanguageDict.__init__(self, csv_fname, delimiter)

    def __getitem__(self, key):
        _dict = csv.DictReader(open(self.csv_fname, 'rb'), delimiter=self.delimiter)

        for k in _dict:
            if k['meta:term-value'].decode('latin-1').encode("utf-8") == key:  # WARNING: assuming _dict encoded in latin-1
                return  k['meta:term-id']
        return None
