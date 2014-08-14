import hashlib
import mimetypes
from gaia.error import GaiaSystemError
from gaia.utils.gaia_file import GaiaFile
from gaia.asset.asset_error import AssetError
import platform
from gaia.log.log import Log
from gaia.utils.imagemagick_error_codes import IMAGEMAGICK_SYSTEM_ERROR_CODES, IMAGEMAGICK_IMAGE_ERROR_CODES
from gaia.utils.try_cmd import try_cmd, CommandError

class Asset(GaiaFile):
    ''' An Asset is a file with some extra features.
    
        checksum() - returns a checksum for this file
        mime_type() - returns a mime type for this file
        validate() - checks the file's extension type matches the magic number (basic confirmation that this file is "good")
    '''

    def __init__(self, *args, **kwargs):
        GaiaFile.__init__(self, *args, **kwargs)
        self._log = Log.get_logger(self)

    def __cmp__(self, other):
        try:
            return cmp(self.fpath, other.fpath)
        except AttributeError:  # this mainly deals with the case of other == None
            return cmp(self.fpath, other)

    def __hash__(self):
        return hash(self.fpath)

    def checksum(self):
        with open(self.name, 'rb') as f:
            m = hashlib.md5()
            m.update(f.read())
            checksum = m.hexdigest()

        return checksum
    
    def mime_type(self):
        # WARNING: on Windows, .xsd comes out as None (vs application/xml)
        mime_type = mimetypes.guess_type(self.name)[0] # ignore the encoding.

        # WARNING: not sure why these come out like this, but we are changing the types!! Could be a Windows thing
        if mime_type == 'image/pjpeg':
            self._log.warning("mime correction: 'image/pjpeg' changed to 'image/jpeg'")
            return 'image/jpeg'
        elif mime_type == 'audio/x-mpg':
            self._log.warning("mime correction: 'audio/x-mpg' changed to 'audio/mpeg'")
            return 'audio/mpeg'
        elif mime_type == 'text/xml':
            self._log.warning("mime correction: 'text/xml' changed to 'application/xml'")
            return 'application/xml'
        else:
            return mime_type

    def validate(self, identify_fpath='/usr/bin/identify'):
        if self.mime_type() != self._file_type():
            raise AssetError('Incorrect mime-type for asset "%s": mime_type_guess="%s", file_type(magic)="%s"' % (self.fname, self.mime_type(), self._file_type()))

        if self.fpath.endswith('.mp3') == False and self.fpath.endswith('.xml') == False:
            colourspace = self._get_colourspace(identify_fpath, self.fpath)
            if colourspace.replace('\n',"") == 'CMYK':
            #if colourspace == 'CMYK':
                raise AssetError('Incorrect colourspace:%s; %s' % (colourspace, self.fpath))

    def _get_colourspace(self, identify_fpath, image_fpath):
        # convert ~/Desktop/a.jpg -colorspace RGB|CMYK ~/Desktop/RGB.jpeg
        cmd = [identify_fpath, '-format', '%[colorspace]', image_fpath]

        try:
            output = try_cmd(*cmd)
        except CommandError, e:
            retcode = e.retcode

            if retcode in IMAGEMAGICK_SYSTEM_ERROR_CODES:
                raise GaiaSystemError('Error providing image info for %s (%s)' %(self.image_fpath, IMAGEMAGICK_SYSTEM_ERROR_CODES[retcode]))
            elif retcode in IMAGEMAGICK_IMAGE_ERROR_CODES:
                raise AssetError('Problem with image at %s (%s)' % (self.image_fpath, IMAGEMAGICK_SYSTEM_ERROR_CODES[retcode]), e.stderr)
            else:
                raise AssetError('Problem with image at %s (%s)' % (image_fpath, e.stderr))

            if retcode == 0 and output.rstrip() == '':
                output = 'Failed to get more information about problems with image (err=%s)' % (str(e))
                raise AssetError('Image "%s" has error (%s)' % (image_fpath, output))

        return output

    def _file_type(self):
        ' return the mime type of a file based on its CONTENTS (magic number), ie like unix file command '
        # requires python-magic from https://github.com/ahupp/python-magic/downloads
        import magic    # this is here to allow tests to run on windows :(
        mime = magic.Magic(mime=True)

        files_mime = mime.from_file(self.name)
        system = platform.system()

        # Sometimes we see the OS not being able to correctly tell us the mime type of  .xml  or .jpg files
        # So we have to manually correct things!
        # see: 
        #    https://bugzilla.redhat.com/show_bug.cgi?id=849621
        #    https://bugzilla.redhat.com/show_bug.cgi?id=873997
        #
        # file -i test_files/minix_filesystem.jpg
        # test_files/minix_filesystem.jpg: application/octet-stream; charset=binary
        #
        # FYI: 
        # file -k test_files/minix_filesystem.jpg
        # test_files/minix_filesystem.jpg: Minix filesystem, V2, 50968 zones\012- JPEG image data, JFIF standard 1.02, comment: "Created by AccuSoft Corp."
        if system == 'Linux':
            distname = platform.linux_distribution()[0]

            if distname == 'Red Hat Enterprise Linux Server' or distname == 'CentOS' or distname == 'Ubuntu' or distname == 'debian' or distname == 'Fedora':
                if files_mime == 'text/x-tex':
                    self._log_file_command()
                    self._log.warning("mime correction: 'text/x-tex' changed to 'application/xml'")
                    files_mime = 'application/xml'
                elif files_mime == 'application/octet-stream':
                    self._log_file_command()
                    self._log.warning("mime correction: 'application/octet-stream' changed to 'image/jpeg'")
                    files_mime = 'image/jpeg'

        return files_mime

    def _log_file_command(self):
        # There isn't a way to log file -k without and'ing MAGIC_CONTINUE to flag in magic lib constructor!
        import magic
        magic_file = magic.Magic(mime=False)

        file_command = magic_file.from_file(self.name)
        self._log.warning("'file' command: '%s'" % file_command) 
