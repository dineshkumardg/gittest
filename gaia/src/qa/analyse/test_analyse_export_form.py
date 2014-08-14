#!python -m doctest -v test_fix_form.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_analyse_export_form.py')

if __name__ == '__main__':
    doctest.testfile("test_analyse_export_form.py", extraglobs={'__file__': __file__},)# optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''

>>> from qa.analyse.analyse_expert_form import AnalyseExpertForm

>>> # ---------------------------------------------------------------------
>>> # C: split_query tests
>>> query = 'id:*'
>>> print AnalyseExpertForm.split_query(query)
('id:*', {})

>>> query = 'id:*&fl=id,title&rows=999'
>>> print AnalyseExpertForm.split_query(query)
('id:*', {'rows': ['999'], 'fl': ['id,title']})

>>> query = 'doc_@contentType:* &fl=doc_language&rows=3'
>>> print AnalyseExpertForm.split_query(query)
('doc_@contentType:* ', {'rows': ['3'], 'fl': ['doc_language']})

>>> query = 'title:james doc_@contentType:* &fl=doc_language&facet=true&whatever=something&rows=1223'
>>> print AnalyseExpertForm.split_query(query)
('title:james doc_@contentType:* ', {'facet': ['true'], 'rows': ['1223'], 'fl': ['doc_language'], 'whatever': ['something']})

>>> query = 'doc_@contentType:* &rows=2&fl=doc_language'
>>> print AnalyseExpertForm.split_query(query)
('doc_@contentType:* ', {'rows': ['2'], 'fl': ['doc_language']})

>>> # A form validation ---------------------------------------
>>> # data is empty, but bound: https://docs.djangoproject.com/en/dev/ref/forms/api/#ref-forms-api-bound-unbound
>>> form = AnalyseExpertForm({'expert_query': ''})
>>> print form.is_valid()
True

>>> # B search_query_syntax ---------------------------------------
>>> form = AnalyseExpertForm({'expert_query': 'id:*'})
>>> print form.is_valid()
True

>>> form = AnalyseExpertForm({'expert_query': 'id:*&fl=id'})
>>> print form.is_valid()
True

>>> form = AnalyseExpertForm({'expert_query': "doc_language:'English' fl=doc_language"})
>>> print form.is_valid()
True

>>> form = AnalyseExpertForm({'expert_query': "doc_language:'English' &fl=doc_language"})
>>> print form.is_valid()
True

>>> form = AnalyseExpertForm({'expert_query': "doc_language:'Eng\nlish' &fl=doc_language"})
>>> print form.is_valid()
True

>>> form = AnalyseExpertForm({'expert_query': 'doc_@contentType:*  &fl=doc_language&rows=12'})
>>> print form.is_valid()
True

>>> # this would have actually caused: SearchError: Cannot Analyse due to a SEARCH SERVER PROBLEM
>>> form = AnalyseExpertForm({'expert_query': 'doc_@contentType:*  &rows=1 &fl=doc_language'})
>>> print form.is_valid()
True

'''
