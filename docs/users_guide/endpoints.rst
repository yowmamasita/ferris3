Endpoints
=========

Ferris provides some utilities on top of Google Cloud Endpoints to make it easier to define an expose endpoints.

Before we dive into creating an using APIs let's define some terminology:

 1. **API** is what your application exposes. Your application's API exposes various *endpoints*
 2. **Endpoints** are groups of exposed functionality. It contains the definition of the endpoints's properties including the name, authentication, and access control. Endpoints contain various *services*. When you create a new project you have a single default endpoint but an application can have multiple endpoints. Endpoints are defined using yaml files.
 3. **Services** are python classes that *expose methods* to the *endpoint* and thus to the overall *API*.
 4. **Method** are the individual functions that can be called by API clients. This is where you write the code to expose and process data.
 5. **Messages** are the language spoken by an API. Messages are classes that define structured data for both data coming from API clients and data send to API clients.

.. module:: ferris3.endpoints


Defining Endpoints
------------------

When you start a new ferris project a default endpoint is created for you and made available to clients and your application. However, you can modify this endpoint and add additional endpoints if desired. Endpoints are defined via yaml files stored in the ``app`` directory and the default one is stored at ``app/default-endpoint.yaml``.

Here's an annotated sample:

.. code-block :: yaml
    
    # Friendly name. Shows up in the Google API Explorer.
    canonical_name: Ferris Endpoint
    # API name. Should be lower case and only contain letters, numbers and underscore.
    # Used in the client librarys, ala gapi.client.ferris.
    name: ferris
    # API Version. Lower case and letters, numbers, and underscore.
    version: v1
    # Friendly description.
    description: Ferris-based Endpoint
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
    
    endpoints.add('app/my-new-endpoint.yaml')

You can now use this endpoint by name (the name field in the yaml file) when defining services. 


Creating Services
-----------------

Services can be added to an endpoint using :func:`auto_service`::

    import ferris3

    # Exposed as ferris.posts
    @ferris3.auto_service
    class PostsService(ferris3.Service):
        ...

    # Exposed as ferris.photos
    @ferris3.auto_service(name='photos')
    class ImagesService(ferris3.Service):
        ...

    # Exposed as mobile_only.photos
    @ferris3.auto_service(name='photos', endpoint='mobile_only')
    class ImagesApi(ferris3.Service):
        ...

If you need more control, the endpoints loaded by Ferris are turned in to normal Google Cloud Endpoints API classes. This means you can follow the same patterns described in Google's documentation on `implementing a multi-class API <https://developers.google.com/appengine/docs/python/endpoints/create_api#creating_an_api_implemented_with_multiple_classes>`_::

    import ferris3

    endpoint = ferris3.endpoints.default()

    @endpoint.api_class(resource_name='posts')
    class PostsApi(ferris3.Service):
        ...

The default endpoint is available via :func:`default` and you can get a particular endpoint by name via :func:`get`.


Exposing API Methods
--------------------

TODO
