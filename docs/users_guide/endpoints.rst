Endpoints
=========

Ferris provides some utilities on top of Google Cloud Endpoints to make it easier to define an expose endpoints.

An endpint is comprised of various parts:

 1. **Endpoint** is the top-level container. It contains the definition of the API's properties including the name, authentication, and access control. An application can have multiple endpoints.
 2. **API Classes**


.. module:: ferris3.endpoints


Defining Endpoint APIs
----------------------

When you start a new ferris project a default endpoint is created for you and made available to clients and your application. However, you're not limited to just one endpoint. Endpoints can be defined via yaml files stored in the ``app`` directory. Here's an annotated sample:


.. code-block :: yaml
    
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


Once you've defined your endpoint you need to instruct ferris to load it and make it available. You'll need to modify ``main.py`` and add:
    
    endpoints.add('app/my-new-api.yaml')


Creating API Classes
--------------------

The easiest way to associate a API class with an endpoint is via :func:`auto_class`::

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

If you need more control, the endpoints loaded by Ferris are turned in to normal Google Cloud Endpoints API classes. This means you can follow the same patterns described in Google's documentation on `implementing a multi-class API <https://developers.google.com/appengine/docs/python/endpoints/create_api#creating_an_api_implemented_with_multiple_classes>`_::

    import ferris3
    import endpoints

    endpoint = ferris3.endpoints.default()

    @endpoint.api_class(resource_name='posts')
    class PostsApi(ferris3.Service):
        ...

The default endpoint is available via :func:`default` and you can get a particular endpoint by name via :func:`get`.


Exposing API Methods
--------------------

TODO
