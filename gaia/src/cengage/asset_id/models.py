''' *PRIVATE* Models for the Cengage Asset Id Service 

Note: instead of using these directly you should use the AssetIdService class.
'''
import logging
from django.db import models
# from django.db.backends.dummy.base import IntegrityError
from django.db import IntegrityError

class AssetIdCache(models.Model):
    ''' A cache of Asset Ids.

        add()  - add ids to the cache
        next() - extract the next id from the cache
        size() - check the current size of the cache

        Also supports the Iterator Protocol, so, eg you can get 
        everything from the cache with [id for id in cache]
    '''
    asset_id = models.CharField(max_length=32, primary_key=True)  # TODO confirm this length

    class Meta:
        db_table = 'asset_id_cache'

    def add(self, *asset_ids):
        ' Add new asset ids: the caller should ensure uniqueness (duplicates are ignored) '
        try:
            batch_size = 100    # sqlite has a limit of 999

            #AssetIdCache.objects.bulk_create([AssetIdCache(asset_id=asset_id) for asset_id in asset_ids], batch_size=999)   # in Django 1.5
            while asset_ids:
                AssetIdCache.objects.bulk_create([AssetIdCache(asset_id=asset_id) for asset_id in asset_ids[:batch_size]])
                asset_ids = asset_ids[batch_size:]

        except IntegrityError, e:
            logging.warning('tried to add a duplicate Asset Id "%s": ignoring (should never happen!)' % asset_id)

    def next(self):
        ''' get the next available id frm the cache or raise StopIteration if cache is empty.

            Note that this has the side effect of removing that id from the cache.
            Note: we use StopIteration to (partly) support the standard Iteration Protocol (it's "half a duck").
        '''
        try:
            next_in_cache = AssetIdCache.objects.all()[0]
            asset_id = next_in_cache.asset_id

            next_in_cache.delete() # remove this from the cache

            return asset_id

        except IndexError, e:   # the cache is empty (TODO: add logging)
            raise StopIteration()

    def __iter__(self):
        return self

    def size(self):
        return AssetIdCache.objects.count()
