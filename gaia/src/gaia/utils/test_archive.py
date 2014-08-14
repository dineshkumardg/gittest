import doctest
suite = doctest.DocFileSuite('test_archive.py')

if __name__ == '__main__':
    doctest.testfile("test_archive.py", extraglobs={'__file__': __file__}, optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)

'''
>>> import os
>>> import sys
>>> from pprint import pprint
>>> from gaia.utils.try_cmd import try_cmd
>>> from gaia.utils.archive import Archive
>>> from testing.gaia_test import GaiaTest

>>> test = GaiaTest()
>>> test.setUp()
>>> test_dir = test.test_dir
>>> config = test.config

>>> dir_to_zip = os.path.join(test_dir, 'dir_to_zip')
>>> zip_dest_dir = os.path.join(test_dir, 'zip_dest')
>>> os.mkdir(dir_to_zip)
>>> os.mkdir(zip_dest_dir)

# Set it up!

>>> if sys.platform.startswith("win"):
...     zip_fpath = r'c:\Program Files\7-zip\7z.exe'
... else:
...     zip_fpath = '/usr/bin/7z'

>>> expected_rel_fpaths = [ os.path.join('dir1.1', 'dir1.1', 'path.txt'),
...                         os.path.join('dir1.1', 'dir1.2', 'path.txt'),
...                         os.path.join('dir2.1', 'path2.txt'),
...                         os.path.join('dir3.1', 'dir3.2', 'path.txt'),
...                         os.path.join('dir4.1', 'dir4.2', 'dir4.3', 'path.txt') ]

>>> for rel_path in expected_rel_fpaths:
...     full_path = os.path.join(dir_to_zip, rel_path)
...     _dirname = os.path.dirname(full_path)
...     if not os.path.exists(_dirname):
...         os.makedirs(_dirname)
...     f = open(full_path, 'wb')
...     f.write('Boom')
...     f.close()

# Test it!

>>> zip_dest_fpath = os.path.join(zip_dest_dir, 'test_zip.7z')
>>> archive = Archive(zip_fpath)
>>> out_fpath = archive.create(dir_to_zip, zip_dest_dir, 'test_zip')
>>> print os.path.relpath(out_fpath, test_dir)  #doctest:+ELLIPSIS
zip_dest...test_zip.7z

>>> os.path.exists(zip_dest_fpath)
True

>>> old_dir = os.getcwd()
>>> os.chdir(zip_dest_dir)

# Confirm we have the right package structure

>>> cmd = [zip_fpath, 'x', zip_dest_fpath]
>>> out = try_cmd(*cmd)

>>> fpaths = []
>>> for root, dirs, files in os.walk(zip_dest_dir):
...     for file in files:
...         fpath = os.path.join(root, file)
...         fpaths.append(os.path.relpath(fpath, zip_dest_dir))
>>> fpaths.sort()
>>> print '\n'.join(fpaths)   # doctest:+ELLIPSIS
dir_to_zip...dir1.1...dir1.1...path.txt
dir_to_zip...dir1.1...dir1.2...path.txt
dir_to_zip...dir2.1...path2.txt
dir_to_zip...dir3.1...dir3.2...path.txt
dir_to_zip...dir4.1...dir4.2...dir4.3...path.txt
test_zip.7z
    
>>> os.chdir(old_dir)

>>> test.tearDown()

'''
