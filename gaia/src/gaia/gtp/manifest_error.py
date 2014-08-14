from gaia.error import GaiaError

class ManifestError(GaiaError):
    pass
    
class MissingManifestError(ManifestError):
    
    def __init__(self, group, item_name):
        msg = 'No manifest file for item "%s" in group "%s"' % (item_name, group)
        ManifestError.__init__(self, msg)
