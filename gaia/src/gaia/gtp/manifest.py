import os
import re
from gaia.gtp.manifest_error import ManifestError


class Manifest():
    ''' Represents the contents of a manifest file 
        following Gaia Transfer Protocol standards.
    '''

    fname = 'manifest.md5'

    def __init__(self, manifest_fpath):
        self._checksum = {}
        exp = re.compile('(^[0-9a-fA-F]{32}) [ \*](.+$)')

        try:
            if os.path.getsize(manifest_fpath) == 0:
                raise ManifestError('Manifest file is empty')

            with open(manifest_fpath) as f:
                for line in f:
                    if line.strip() == '' or line.startswith('#'):
                        continue # Blank lines or comment lines are ignored

                    match = exp.match(line)
                    if not match:
                        raise ManifestError('Line in manifest file is badly formatted: "%s"' % line)

                    checksum = match.group(1)

                    fname = match.group(2).strip()  # whitespace
                    # Gaia Transfer Protocol been published to htc to allow an * before the filename, but code downstream doesn't like this
                    fname = fname.strip('*')

                    if fname.startswith('_'):
                        continue   # ignore any status files (which can get in the manifest by accident)

                    if fname == 'Thumbs.db':
                        continue

                    self._checksum[fname] = checksum

        except (OSError, IOError), e:
            raise ManifestError('Error opening manifest file: "%s"' % e)

    def checksums(self):
        ' return a dictionary of checksums for fnames'
        return self._checksum
