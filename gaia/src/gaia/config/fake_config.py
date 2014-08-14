import os
import sys

class FakeConfig():
    VALID_CAT_LIST = ['News', 'Index', 'Business and Finance', 'News in Brief', 'Display Advertising', 'Stock Exchange Tables']
    VALID_IL_TYPES_LIST = ['Photograph', 'Graph', 'Drawing-Painting', 'Cartoons', 'Map']

    # content_providers does not point at real providers (or even real test providers).
    # Replace the contents of content_providers with known values in your tests.
    content_providers = {'provider_one':   {'server': 'IP Address', 'uid': 'User name', 'pwd': 'Password'},
                        }
    
    def __init__(self,
                 img_file_ext='tif',
                 image_attrs=None,
                 dtd_path=None,
                 project_code='0FFO',
                 content_set_name='TLDA',
                 zip_path='/usr/bin/7z',
                 working_dir='/tmp',
                 release_dir=None,
                 valid_cats=None,
                 valid_il_types=None,
                 ):
        
        self._img_file_ext = img_file_ext
        self._image_attrs = image_attrs
        self._dtd_path = dtd_path
        self._project_code = project_code
        self._content_set_name = content_set_name
        self._zip_path = zip_path
        self._working_dir = working_dir
        self._release_dir = release_dir
        self.valid_cats = valid_cats
        self.valid_il_types = valid_il_types
        if sys.platform.startswith("win"):
            self._xmllint_path = r'c:\xmllint\bin\xmllint.exe'
        else:
            self._xmllint_path = '/usr/bin/xmllint'

    def image_attrs(self):
        return self._image_attrs

    def image_file_ext(self):
        return self._img_file_ext
    
    def valid_categories(self):
        if self.valid_cats:
            return self.valid_cats
        else:
            return self.VALID_CAT_LIST

    def valid_illustration_types(self):
        if self.valid_il_types:
            return self.valid_il_types
        else:
            return self.VALID_IL_TYPES_LIST
    
    def dtd_path(self):
        return self._dtd_path
    
    def project_code(self):
        return self._project_code

    def content_set_name(self):
        return self._content_set_name
    
    def zip_path(self):
        return self._zip_path
    
    def working_dir(self):
        return self._working_dir
    
    def release_dir(self):
        return self._release_dir or os.path.join(self.working_dir(), 'export', 'release')
    
    def xmllint_path(self):
        return self._xmllint_path
