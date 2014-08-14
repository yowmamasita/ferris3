Endpoints
=========

Ferris provides some utilities on top of Google Cloud Endpoints to make it easier to define an expose endpoints.


.. module:: ferris3.endpoints_apis


Defining APIs
-------------

When you start a new ferris project a default API is created for you and made available to clients and your application. However, you're not limited to just one API. APIs can be defined via yaml files stored in the ``app`` directory. Here's an annotated sample::

    
    # Friendly name. Shows up in the Google API Explorer.
    canonical_name: Ferris API
    # API name. Should be lower case and only contain letters, numbers and underscore.
    # Used in the client librarys, ala gapi.client.ferris.
    name: ferris
    # API Version. Lower case and letters, numbers, and underscore.
    version: v1
    # Friendly description.
    description: Ferris-based API
    # Authentication level. Can be "optional" or "required".
    auth_level: required
    # Scopes required when authentication is used. Any valid scope from Google is allowed. USERINFO is a special scope alias.
    scopes:
    - USERINFO
    # Allowed client IDs. These are the client IDs that your front-ends use when accessing the API.
    allowed_client_ids:
    - API_EXPLORER_CLIENT_ID
    - 462711127220-1mr3uha1ukgicv4s0ebvo26bulkpb4k1.apps.googleusercontent.com


Once you've defined your API you need to instruct ferris to load it and make it available. You'll need to modify ``main.py`` and add:
    
    endpoints_apis.add('app/my-new-api.yaml')


Using APIs
----------

The easiest way to associate a service class with an API is via :func:`auto_class`::

    import ferris3

    @ferris3.auto_class
    class PostsApi(ferris3.Service):
        ...

    @ferris3.auto_class(name='photos')
    class ImagesApi(ferris3.Service):
        ...

    @ferris3.auto_class(name='photos', api='mobile_only')
    class ImagesApi(ferris3.Service):
        ...

If you need more control, the APIs loaded by Ferris are turned in to normal Google Cloud Endpoints API classes. This means you can follow the same patterns described in Google's documentation on `implementing a multi-class api <https://developers.google.com/appengine/docs/python/endpoints/create_api#creating_an_api_implemented_with_multiple_classes>`::

    import ferris3
    import endpoints

    api = ferris3.endpoints_apis.default()

    @api.api_class(resource_name='posts')
    class PostsApi(ferris3.Service):
        ...

The default api is available via :func:`default` and you can get a particular api by name via :func:`get`.
