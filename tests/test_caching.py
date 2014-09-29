from ferrisnose import AppEngineTest
from google.appengine.api import memcache
from ferris3.caching import cache, cache_by_args, none_sentinel_string, LocalBackend, MemcacheBackend, DatastoreBackend, MemcacheCompareAndSetBackend, LayeredBackend, DatastoreCacheModel


class CacheTest(AppEngineTest):

    def test_cache(self):
        for backend in [None, 'local', 'datastore', LocalBackend, MemcacheBackend, DatastoreBackend, MemcacheCompareAndSetBackend, LayeredBackend(LocalBackend, MemcacheBackend)]:
            memcache.flush_all()
            LocalBackend.reset()
            map(lambda x: x.key.delete(), DatastoreCacheModel.query())

            mutators = [0, 0, 0]
            print 'testing %s' % backend

            @cache('cache-test-key', backend=backend)
            def test_cached():
                mutators[0] += 1
                return mutators[0]

            if not backend:
                backend = MemcacheBackend
            if backend == 'local':
                backend = LocalBackend
            if backend == 'datastore':
                backend = DatastoreBackend

            assert test_cached() == 1
            assert test_cached() == 1
            assert mutators[0] == 1
            assert backend.get('cache-test-key') == 1
            assert test_cached.uncached() == 2
            assert test_cached.cached() == 1

            test_cached.clear_cache()
            assert test_cached() == 3

            @cache('cache-test-key-none', backend=backend)
            def test_cached_with_none():
                mutators[1] += 1
                return None

            assert test_cached_with_none() is None
            assert test_cached_with_none() is None
            assert mutators[1] == 1
            assert backend.get('cache-test-key-none') == none_sentinel_string
            assert test_cached_with_none.cached() is None

            @cache_by_args('cache-test-args')
            def test_cached_with_args(arg):
                return arg

            assert test_cached_with_args(1) == 1
            assert test_cached_with_args(2) == 2

            @cache_by_args('cache-test-args-method')
            def test_cached_with_args(self, arg):
                return arg

            assert test_cached_with_args(None, 1) == 1
            assert test_cached_with_args(None, 2) == 2

    def test_expiration(self):
        for backend in LocalBackend, DatastoreBackend:
            backend.set('expiry', 1, ttl=-1)
            assert not backend.get('expiry')

    def test_delete(self):
        LocalBackend.delete('non-existant')

    def test_cas(self):
        MemcacheCompareAndSetBackend.set('test', 1, 0)
        MemcacheCompareAndSetBackend.set('test', 2, 0)
        assert MemcacheCompareAndSetBackend.get('test') == 2
