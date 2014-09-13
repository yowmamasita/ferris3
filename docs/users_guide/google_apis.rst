Google APIs
===========

.. module:: ferris3.google_apis

Ferris' Google API Helper makes it easy to use Google's recommended `best practices <https://developers.google.com/appengine/articles/efficient_use_of_discovery_based_apis>`_ when interacting with Google APIs via the `Google API Client Library <https://developers.google.com/api-client-library/python/>`_.


Building Clients
----------------

.. autofunction:: build

As demonstrated, valid credentials can be obtained with the help of :mod:`ferris3.oauth2` or with any valid credentials from Google's `oauth2client <https://developers.google.com/api-client-library/python/guide/aaa_oauth>`_.


Exponential Backoff
-------------------

Google recommends using `exponential backoff <https://developers.google.com/drive/web/handle-errors>`_ when making API requests. This is especially important when making lots of calls. The helper provides a couple of utilities for this purpose.

.. autofunction:: retry_execute

.. autofunction:: retries


Discovery Document Caching
--------------------------

The API Client uses a discovery document to determine information about an API. The helper ensures that this document is cached so that building a client doesn't incur reloading the discovery document every time. You do not have to do anything to take advantage of this; it happens automatically.

