from gaia.error import GaiaError

class ProviderError(GaiaError):
    pass

class TransferError(ProviderError):
    pass

class TransferAbort(ProviderError):
    pass
