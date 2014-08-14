from gaia.log.log import Log
from gaia.error import GaiaError
from cengage.asset_id.models import AssetIdCache
from cengage.asset_id.asset_id_provider import _AssetIdProvider, AssetIdFetchFailed

class AssetIdCacheEmptyError(GaiaError): pass

# TODO: rename this to the servie (backed by a cache)
class AssetIdService:
    ''' An Asset Id Service Manager for EMEA.

        This implementation serves ids from the US central provider
        when they are available, and also maintains a temporary
        cache in case the US systems are un-available.

        CACHE POLICY:
        The cache-management policy is as follows:

        Each get() will try to fetch an id from the US.
        If this fails, the cache will be hit (and decrease by 1)

        If the cache reaches below the low_watermark, each subsequent
        get() request will try to pull in enough new ids to re-fill
        the cache to the high_watermark. If these requests fail, another
        attempt will be made on each subsequent get().

        Note that the cache *can* run to empty (eg if the service is
        continually down), in which case AssetIdCacheEmptyError is raised.
        (Please tune low and high watermarks appropriately!)

        You can force fill the cache with refresh() if required to ensure
        a higher capacity (but better to tune watermarks appropriately)
    '''

    #def __init__(self, low_watermark=10, high_watermark=30, provider_args={}):  # TMP TUSH FOR TESTING
    def __init__(self, low_watermark=3000, high_watermark=4000, provider_args={}):
        self._log = Log.get_logger(self)
        self.low_watermark = low_watermark
        self.high_watermark = high_watermark
        self.cache = AssetIdCache()
        self.service = _AssetIdProvider(**provider_args) #single_url=None, bulk_url=None, uid=None, pwd=None, timeout_seconds=60, num_retries=3):
        
    def get(self):
        self._log.enter()
        if self.cache.size() < self.low_watermark:
            self.refresh()                          # try to re-fill the cache as we're getting low/desperate!

        try:
            asset_id = self.service.fetch()           # normal service
            self._log.info('got asset_id from service (normal)', asset_id=asset_id)
        except  AssetIdFetchFailed, e:
            try:
                asset_id = self.cache.next()        # try to serve from the cache instead
                self._log.info('got asset_id from cache (service fetch failed)', asset_id=asset_id)
            except StopIteration, e:
                self._log.exit('NO ASSET IDS left, raising error.')
                raise AssetIdCacheEmptyError()  # we're empty, so give up!

        self._log.exit()
        return asset_id

    def refresh(self):
        num_required = self.high_watermark - self.cache.size()
        self.cache.add(*self.service.fetch(num_required)) 

'''
>>> import os
>>> import sys
>>> import logging
>>> from testing.gaia_django_test import GaiaDjangoTest
>>> test = GaiaDjangoTest()
>>> test.setUp()

>>> from cengage.asset_id.asset_id_service import AssetIdService 
>>> service = AssetIdService(low_watermark=3, high_watermark=7) # avoid getting lots of ids with extremely low watermark settings!)  # WARNING: Uses live service!

>>> asset_id =  service.get()
>>> cached_ids = [_id for _id in service.cache]
>>> print "Got asset_id=", asset_id, ", cached_ids=", str(cached_ids)
TODO: shoud get one id and 7 in the cache...

>>> test.tearDown()

'''
