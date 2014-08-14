import os
from gaia.log.log import Log

class DeliveryManifest:
    ' A class responsible for creating a Callisto delivery manifest. '
    
    def __init__(self, package_name, package_dir, content_set_name):
        self.fname = '%s_delivery_manifest_%s.txt' % (content_set_name, package_name)
        self.package_dir = package_dir
        self.content_set_name = content_set_name
        self._log = Log.get_logger(self)

    def create(self):
        self._log.enter()
        manifest = ''
        listing = os.listdir(self.package_dir)
        dirs = [entry for entry in listing if os.path.isdir(os.path.join(self.package_dir, entry))]
        dir_names = [os.path.basename(_dir) for _dir in dirs]
        dir_names.sort()

        for _dir in dirs:
            manifest += '%s, %s\n' % (_dir, self.content_set_name)

        self._log.exit()
        return manifest
