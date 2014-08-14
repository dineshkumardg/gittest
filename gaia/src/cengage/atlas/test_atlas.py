# coding: utf-8

import doctest

suite = doctest.DocFileSuite('test_atlas.py')

if __name__ == '__main__':
    doctest.testfile("test_atlas.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS)

'''
>>> from cengage.atlas.atlas_language_dict import AtlasLanguageDict
>>> from cengage.atlas.atlas_illustration_dict import AtlasIllustrationDict

>>> atlas_language = AtlasLanguageDict()
>>> print atlas_language['Abkhaz']
21632973

>>> print atlas_language[u'English']
13858590

>>> print atlas_language['English']
13858590

>>> ########################################################################################

>>> atlas_illustration = AtlasIllustrationDict()
>>> print atlas_illustration['Chart']
14170008

>>> print atlas_illustration[u'Chart']
14170008

'''
