from gaia.error import GaiaError

class ConversionError(GaiaError):
    pass
    
class DialogBConversionError(ConversionError):
    
    def __init__(self, item_name):
        msg = 'Problem converting "%s"' % item_name
        ConversionError.__init__(self, msg)
