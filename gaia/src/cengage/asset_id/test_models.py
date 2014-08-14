from testing.cengage_django_test import CengageDjangoTest
_test = CengageDjangoTest()
_test.setUp()

import unittest
from django.test import TestCase
from cengage.asset_id.models import AssetIdCache


class AssetIdCacheTestCase(TestCase):
    def test_add_one(self):
        # Ddesign Note: asset ids are mnore normally fixed-length character strings ,
        # but this code is agnostic to the details of the id (it's an opaque character string).
        cache = AssetIdCache()

        num_ids = 7
        for next_id in range(0, num_ids):
            cache.add(str(next_id)) 

        self.assertEqual(num_ids, AssetIdCache.objects.count())
        
    def test_add_many(self):
        cache = AssetIdCache()

        num_ids = 4
        next_ids = [str(next_id) for next_id in range(0, num_ids)]

        cache.add(*next_ids)

        self.assertEqual(num_ids, AssetIdCache.objects.count())
        
    def test_add_duplicates_ignored(self):
        asset_id = 'XXSXKW685871004'

        self.assertEqual(0, AssetIdCache.objects.count())

        AssetIdCache().add(asset_id)
        AssetIdCache().add(asset_id)
        AssetIdCache().add(asset_id)

        self.assertEqual(1, AssetIdCache.objects.count())

    def test_next_EMPTY(self):
        cache = AssetIdCache()

        try:
            cache.next()
            self.fail('failed to raise StopIteration on empty cache')
        except StopIteration, e:
            pass

    def test_next(self):
        cache = AssetIdCache()

        num_ids = 4
        next_ids = [str(next_id) for next_id in range(0, num_ids)]

        cache.add(*next_ids)
        self.assertEqual(num_ids, AssetIdCache.objects.count())

        # TEST:
        ids = []

        for i in range(0, num_ids):
            ids.append(cache.next()) # note: _explicit_ call of next()
            num_expected_in_cache = num_ids - i - 1
            self.assertEqual(num_expected_in_cache, AssetIdCache.objects.count()) # check that the cache is being emptied

        self.assertEqual(0, AssetIdCache.objects.count())    # cache should be empty at the end.

    def test_iterator(self):
        cache = AssetIdCache()

        num_ids = 4
        next_ids = [str(next_id) for next_id in range(0, num_ids)]

        cache.add(*next_ids)
        self.assertEqual(num_ids, AssetIdCache.objects.count())
        
        # TEST:
        ids = [ _id for _id in cache]    # Note: _implicitly_ calls next() via the iterator protocol

        self.assertEqual(num_ids, len(ids))
        self.assertEqual(0, AssetIdCache.objects.count()) # check that the cache was emptied as we got each value

    def test_size(self):
        cache = AssetIdCache()

        self.assertEqual(0, cache.size())

        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901a')
        self.assertEqual(1, cache.size())

        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901b')
        self.assertEqual(2, cache.size())

        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901c')
        self.assertEqual(3, cache.size())

        cache.next()
        self.assertEqual(2, cache.size())

        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901d')
        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901e')
        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901f')
        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901g')
        cache.add('ABCDEFGHIJKLMNOPQRSTUVWXYZ78901h')
        cache.add('TOJUCO403007670') # Note: this is a real asset id (15 chars length)
        self.assertEqual(8, cache.size())

        cache.next()
        cache.next()
        cache.next()
        self.assertEqual(5, cache.size())

        cache.next()
        cache.next()
        cache.next()
        cache.next()
        cache.next()
        self.assertEqual(0, cache.size())


suite = unittest.TestLoader().loadTestsFromTestCase(AssetIdCacheTestCase)
_test.tearDown()

if __name__ == '__main__':
    import testing
    testing.main(suite)
