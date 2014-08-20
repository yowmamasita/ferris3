Caching
=======

Ferris provides extensive tools for caching data. Taking advantage of the caching can significantly reduce your applications ongoing cost while at the same time decreasing latency and improving responsiveness. The caching utilities can use multiple storage backends to suit different purposes: `App Engine's Memcache API <https://developers.google.com/appengine/docs/python/memcache/>`_, the Cloud Datastore, or local in-process memory.


.. module:: ferris3.caching

Decorators
----------

.. autofunction:: cache

.. autofunction:: cache_by_args


Utility Functions
-----------------

When using the :func:`cache` decorator on a function, the caching module adds three helpful utility methods. Note that these methods are not available for the :func:`cached_by_args` decorator.

.. method:: cachedfunction.clear_cache()

    This will clear any cached data for the function so that the next call will execute the function and refresh the cached data.

    Example::

        @cache('herd-cats')
        def herd_cats():
            count = do_herd_cats()
            return count

        herd_cats.clear_cache()


.. method:: cachedfunction.cached()

    Returns the cached value for the function if it's set, otherwise it returns None.

.. method:: cachedfunction.uncached()

    Skips the caching layer completely and executes the function. This is essentially the same as calling the function without it ever being decoratored.


Backends
--------

Three different backends are provided as well as a special layering backend.


.. autoclass:: LocalBackend

.. autoclass:: MemcacheBackend

.. autoclass:: MemcacheCompareAndSetBackend

.. autoclass:: DatastoreBackend

.. autoclass:: LayeredBackend
