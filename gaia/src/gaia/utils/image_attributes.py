
class ImageAttributes:
    TIFF_FORMAT = 'TIFF'
    JPEG_FORMAT = 'JPEG'
    PNG_FORMAT = 'PNG'

    def __init__(self, format, dpi, depth, file_ext, compression_quality=None):
        # Note: dpi is a tuple of (x_dpi, y_dpi), depth is an int, quality is an int
        self.format = format
        self.dpi = dpi  # this is a tuple of (xdpi, ydpi)
        self.depth = depth
        self.file_ext = file_ext
        self.compression_quality = compression_quality
        
    def is_jpeg(self):
        return self.format is self.JPEG_FORMAT
        
    def is_tiff(self):
        return self.format is self.TIFF_FORMAT
        
    def is_png(self):
        return self.format is self.PNG_FORMAT
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return 'Format: %s, DPI: %s, Bit depth: %s, File extension: %s, Compression quality: %s' % (self.format, str(self.dpi), str(self.depth), self.file_ext, str(self.compression_quality))
        
    def __cmp__(self, other):
        if self.format != other.format:
            return -1
        elif self.dpi != other.dpi:
            return -1
        elif self.depth != other.depth:
            return -1
        elif self.file_ext != other.file_ext:
            return -1
        elif self.compression_quality and self.compression_quality != other.compression_quality:
            return -1
        else:
            return 0

class JpegImageAttributes(ImageAttributes):
    ' Attributes for a JPEG Image with a square aspect ratio (x_dpi == y_dpi) '
    FILE_EXT = 'jpg'
    
    def __init__(self, x_dpi, depth, compression_quality=None):
        ImageAttributes.__init__(self, self.JPEG_FORMAT, (x_dpi, x_dpi), depth, self.FILE_EXT, compression_quality)

class TiffImageAttributes(ImageAttributes):
    ' Attributes for a TIFF Image with a square aspect ratio (x_dpi == y_dpi) '
    FILE_EXT = 'tif'
    
    def __init__(self, x_dpi, depth, compression_quality=None):
        ImageAttributes.__init__(self, self.TIFF_FORMAT, (x_dpi, x_dpi), depth, self.FILE_EXT, compression_quality)

class PngImageAttributes(ImageAttributes):
    ' Attributes for a PNG Image with a square aspect ratio (x_dpi == y_dpi) '
    FILE_EXT = 'png'
    
    def __init__(self, x_dpi, depth, compression_quality=None):
        ImageAttributes.__init__(self, self.PNG_FORMAT, (x_dpi, x_dpi), depth, self.FILE_EXT, compression_quality)
