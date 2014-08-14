import os
from gaia.log.log import Log
from gaia.error import GaiaError

class ImageManifestError(GaiaError):
    pass

class ImageManifest:
    ' Creates an XML image manifest for assets belonging to a particular item. '
    
    def __init__(self, item, content_set_name):
        self.item = item
        self.fname = '%s_image_manifest_%s.xml' % (content_set_name, item.dom_name)
        self._log = Log.get_logger(self)

    def create(self):
        self._log.enter()
        
        fnames = [asset.fname for asset in self.item.assets if asset.ftype != 'xml']
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<records>\n'

        for fname in sorted(fnames):
            fbase, _ext = os.path.splitext(fname)
            xml += '<record href="%s" ECOID="%s" />\n' % (fname, fbase)

        xml += '</records>'

        self._log.exit()
        return xml

class AssetImageManifest:   # TEMPORARY SOLUTION: NEEDS THINKING ABOUT....(too tired now!.... :( )
    ' Creates an XML image manifest for assets '
    
    def __init__(self, assets, content_set_name, package_name):
        self.assets = assets
        self.fname = '%s_image_manifest_%s.xml' % (content_set_name, package_name)
        self._log = Log.get_logger(self)

    def create(self):
        self._log.enter()
        
        fnames = [asset.fname for asset in self.assets]
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<records>\n'

        for fname in sorted(fnames):
            fbase, _ext = os.path.splitext(fname)
            xml += '<record href="%s" ECOID="%s" />\n' % (fname, fbase)

        xml += '</records>'

        self._log.exit()
        return xml
