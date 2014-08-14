from gaia.error import GaiaError


class DocumentError(GaiaError):
    pass


class SourceDataMissing(DocumentError):
    msg = 'element, attribute, or value is required, but is missing!'

    def __init__(self, missing, **kwargs):
        DocumentError.__init__(self, msg=self.msg, missing=missing, **kwargs)


class AtlasLanguageMissing(DocumentError):
    pass


class AtlasIllustrationMissing(DocumentError):
    pass


class PubSegMissing(DocumentError):
    pass


class McodeMissing(DocumentError):
    pass

class McodeDuplicate(DocumentError):
    pass


class LanguageMissing(DocumentError):
    # this is used with respect to the .csv LanguageCorrection class
    pass


class GiftValidationError(DocumentError):
    msg = 'gift document-instance(s) do not validate against XSD'
    def __init__(self, missing, **kwargs):
        DocumentError.__init__(self, msg=self.msg, missing=missing, **kwargs)


class InvalidXmlError(DocumentError):
    msg = 'gift document-instance(s) -- badly formed'
    def __init__(self, error, **kwargs):
        DocumentError.__init__(self, msg=self.msg, error=error, **kwargs)
