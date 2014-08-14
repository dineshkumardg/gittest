from abc import ABCMeta, abstractmethod
from gaia.error import GaiaError

class CannotDetermineDocumentTypeFromFilename(GaiaError):
    pass

class Factory: # a Gaia-DOM-Adapter factory
    ' return a suitable Gaia DOM Adapter class for a file name. '
    __metaclass__ = ABCMeta
    _adapters = {}  # override this.

    def __init__(self):
        pass

    @classmethod
    def adapter_class(cls, fname):
        try:
            return cls._adapters[cls._adapter_type(fname)]
        except KeyError, e:
            raise CannotDetermineDocumentTypeFromFilename(file_name=fname, error=e)

    @classmethod
    @abstractmethod
    def _adapter_type(cls, fname):
        ' return a project-specific key (eg a document type) to lookup an adapter.'
        pass
