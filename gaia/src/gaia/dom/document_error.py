import os
from gaia.error import GaiaError

class DocumentError(GaiaError):
    pass
   
class InvalidXmlSchema(DocumentError):
   
    def __init__(self, xsd_fpath, e):
        DocumentError.__init__(self, xsd=xsd_fpath, error=e)

class InvalidXml(DocumentError):
    ''' Note: we don't supply full paths here so that the reports are sanitised.
    '''

    def __init__(self, fpath, schema_fpath, line, err_msg):
        xml_fname = os.path.basename(fpath)
        xsd_fname = os.path.basename(schema_fpath)
        DocumentError.__init__(self, file=xml_fname, schema=xsd_fname, line=line, error=err_msg)
