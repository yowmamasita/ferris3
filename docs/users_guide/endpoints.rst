Endpoints
=========

Ferris provides some utilities on top of `Google Cloud Endpoints <https://developers.google.com/appengine/docs/python/endpoints/>`__ to make it easier to define an expose endpoints.

.. contents::
    :local:

Terminology
-----------

Before we dive into creating an using APIs let's define some terminology:

 1. **API** is what your application exposes. Your application's API exposes various *endpoints*
 2. **Endpoints** are groups of exposed functionality. It contains the definition of the endpoints' properties including the name, authentication, and access control. Endpoints contain various *services*. When you create a new project you have a single default endpoint but an application can have multiple endpoints. Endpoints are defined using yaml files.
 3. **Services** are Python classes that *expose methods* to the *endpoint* and thus to the overall *API*.
 4. **Method** are the individual functions that can be called by API clients. This is where you write the code to expose and process data.
 5. **Messages** are the language spoken by an API. Messages are classes that define structured data for both data coming from API clients and data sent to API clients.


Defining Endpoints
------------------

When you start a new Ferris project a default endpoint is created for you and made available to clients and your application. However, you can modify this endpoint and add additional endpoints if desired. Endpoints are defined via yaml files stored in the ``app`` directory. The default one is stored at ``app/default-endpoint.yaml``.

Here's an annotated sample:

.. code-block :: yaml
    
    # Friendly name. Displayed in the Google API Explorer.
    canonical_name: Ferris Endpoint
    # API name. Should be lower case and only contain letters, numbers and underscores.
    # Used in the client libraries, e.g. gapi.client.ferris.
    name: ferris
    # API Version. Should be lower case and only contain letters, numbers, and underscores.
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


Once you've defined your endpoint you need to instruct Ferris to load it and make it available. You'll need to modify ``endpoints_config.py`` and add:
    
    endpoints.add('app/my-new-endpoint.yaml')

You can now use this endpoint by name (the name field in the yaml file) when defining services. 


Creating Services
-----------------

Services are defined in the ``app`` directory using the convention ``app/[module]/[module]_service.py``. By following the convention ferris will automatically discover and wire your services.

.. warning::
    If you do not follow the conventions then ferris can not automatically discover your service modules. See :doc:`discovery` for more details.

Once the service file is created, services can be added to an endpoint using :func:`auto_service`::

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

If you need more control, the endpoints loaded by Ferris are turned into normal Google Cloud Endpoints API classes. You may follow the same patterns described in Google's documentation on `implementing a multi-class API <https://developers.google.com/appengine/docs/python/endpoints/create_api#creating_an_api_implemented_with_multiple_classes>`__::

    import ferris3

    endpoint = ferris3.endpoints.default()

    @endpoint.api_class(resource_name='posts')
    class PostsApi(ferris3.Service):
        ...

The default endpoint is available via :func:`default` and you can get a particular endpoint by name via :func:`get`.


Exposing Methods
----------------

A service doesn't do much good without some methods. The :func:`auto_method` decorator helps expose class methods as API methods.

The most basic example::

    import ferris3
    import logging

    @ferris3.auto_service
    class HelloService(ferris3.Service):

        @ferris3.auto_method
        def hello(self, request):
            logging.info("Hello, is it me you're looking for?")


This method simply logs "Hello, is it me you're looking for?" in the application log but does not return any data.


Returning Data
**************

In order to return some data to the client we'll need to define and use a message. We can use the ``returns`` parameter of :func:`auto_method` to do this::

    from protorpc import messages
    import ferris3

    # Define a simple message with one field
    class HelloMessage(messages.Message):
        greeting = messages.StringField(1)


    @ferris3.auto_service
    class HelloService(ferris3.Service):

        # Notice we pass in a "returns" parameter here, informing the endpoint what kind of message this method will return.
        @ferris3.auto_method(returns=HelloMessage)
        def hello(self, request):
            return HelloMessage(greeting="Hello!")


For more details on creating messages see :doc:`messages`.


Defining Parameters
*******************

Sometimes we want a method to take parameters. When using pure Google Cloud Endpoints you'd have to define a `ResourceContainer <https://developers.google.com/appengine/docs/python/endpoints/create_api#using_resourcecontainer_for_path_or_querystring_arguments>`__, but Ferris uses a technique called annotation to automatically handle this for you::

    @ferris3.auto_method(returns=HelloMessage)
    def hello(self, request, name=(str, 'Unknown')):
        return HelloMessage(greeting="Hello, %s!" % name)

Notice this somewhat strange syntax: ``name=(str, 'Unknown')``. Annotations take the form of ``parameter=(type, default)``. By defining the type and default value we can keep our API strongly typed. The default value is optional and if we leave it out the parameter becomes required to call our method. For example::

    @ferris.auto_method(returns=HelloMessage)
    def hello(self, request, name=(str,), age=(int, 18)):
        return HelloMessage(greeting="Hello, %s! You are %s" % (name, int))

``name`` is required but ``age`` is optional. You can observe this by using the API Explorer.



Receiving Data
**************

Often we want to receive structured data from clients. Similar to sending data, we need define a message class for receiving data. We also need to tell the endpoint that we want to receive that message for our method which we can do with an annotation. Putting it all together we get something like this::

    from protorpc import messages
    import ferris3

    # We'll use this new message for the client to send us a list of names.
    class PeopleMessage(messages.Message):
        people = messages.StringField(1, repeated=True)

    # We'll use the same message from before to send data back to the client.
    class HelloMessage(messages.Message):
        greeting = messages.StringField(1)


    @ferris3.auto_service
    class HelloService(ferris3.Service):

        @ferris3.auto_method(returns=HelloMessage)
        def hello(self, request=(PeopleMessage,)):  # Notice the annotation for request
            names = ', '.join(request.people)
            return HelloMessage(greeting="Hello %s!" % names)

If you use the APIs explorer, you'll see you now can provide a request body with a list of names.

Of course, you can combine a request message with parameters::

    @ferris3.auto_method(returns=HelloMessage)
    def hello(self, request=(PeopleMessage,), greeting=(str, 'Hello')):
        names = ', '.join(request.people)
        return HelloMessage(greeting="%s %s!" % (greeting, names))


.. warning::
    When combining request messages with request parameters the field and parameter names must be unique. For example, you can't have a message with the field ``name`` and also a parameter called ``name``. 


API Reference
-------------


.. module:: ferris3.endpoints

.. autofunction:: auto_service
.. autofunction:: auto_method
.. autofunction:: get
.. autofunction:: default
.. autofunction:: add
