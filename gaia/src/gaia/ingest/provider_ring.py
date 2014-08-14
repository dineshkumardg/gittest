from gaia.provider.provider import Provider 
from gaia.utils.ftp import Ftp

class ProviderRing:
    '  A circular buffer of (Provider, TransferAgent) pairs: calling next() will cycle around forever. '

    def __init__(self, config, _transfer_agent_class=Ftp, _provider_class=Provider):
        self._index = 0
        self._providers = []

        for name in config.content_providers.keys():
            transfer_agent = _transfer_agent_class(**config.content_providers[name])
            provider = _provider_class(name, transfer_agent, config)
            
            self._providers.append((provider, transfer_agent))

    def next(self):
        self._index += 1
        if self._index >= len(self._providers):
            self._index = 0
        
        #self._logger.debug('<<< next_provider (returning provider #%d)' % (self._index))
        return self._providers[self._index]
