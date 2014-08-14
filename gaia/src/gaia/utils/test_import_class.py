# Note: use "<BLANKLINE>" to expect an empty line in the output.
import doctest
suite = doctest.DocFileSuite('test_import_class.py')

if __name__ == '__main__':
    doctest.testfile("test_import_class.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> from gaia.utils.import_class import import_class
>>> x = import_class('gaia.error.GaiaError')
>>> print x
<class 'gaia.error.GaiaError'>

>>> # Note: you'll also get this error if there's code within the class that's
>>> # being imported (eg a bad import)
>>> x = import_class('not.importable.GaiaError')
Traceback (most recent call last):
  File "c:\Python27\lib\doctest.py", line 1254, in __run
    compileflags, 1) in test.globs
  File "<doctest test_import_class.py[3]>", line 1, in <module>
    x = import_class('not.importable.GaiaError')
  File "c:\GIT_REPOS\gaia\src\gaia\utils\import_class.py", line 14, in import_class
    raise GaiaCodingError('cannot import class for name (badly configured or bug in class code?)', class_name=class_name)
GaiaCodingError: GaiaCodingError: cannot import class for name (badly configured or bug in class code?) (class_name="not.importable.GaiaError")

'''
