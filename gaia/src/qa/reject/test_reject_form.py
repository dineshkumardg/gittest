#!python -m doctest -v test_fix_form.py
# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_reject_form.py')

if __name__ == '__main__':
    doctest.testfile("test_reject_form.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''

>>> from qa.reject.reject_form import RejectForm

>>> # A form validation ---------------------------------------
>>> reject_form = RejectForm({'reason': 'sears', 'current_page': '2'}, initial={'reason': 'james', 'current_page': '1'})
>>> print reject_form.is_valid()
True

>>> print reject_form.data
{'reason': 'sears', 'current_page': '2'}

>>> # B form initilisation ------------------------------------
>>> reject_form = RejectForm({'reason': 'old records', 'current_page': '123'})
>>> print reject_form.data
{'reason': 'old records', 'current_page': '123'}

'''
