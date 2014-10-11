Discovery
=========

.. module:: ferris3.discovery

Ferris uses conventions to automatically discover :doc:`endpoint services <endpoints>` and :doc:`webapp2 handlers <handlers>`.


Conventions for endpoints
-------------------------

Endpoint services must be defined in ``app/[module]/[module]_service.py``. All services within the file will be discovered and wired. There are no restrictions on what the service class is named, however, all services must inherit from ``ferris3.Service`` or ``protorpc.remote.Service``.

For example, all of the following would work:

    * ``app/posts/posts_service.py`` containing ``PostService``
    * ``app/directory/directory_service.py`` containing ``UsersService`` and ``GroupsService``
    * ``app/directory/combined_service.py`` containing ``Users`` and ``Groups`` because class name doesn't matter, so long as they are a subclass of ``Service``.

However, these would not work:

    * ``app/posts/posts.py`` containing ``PostService``, because the file does not end in ``service``.
    * ``app/posts_service.py`` containing ``PostsService``, because it's not in a subdirectory under ``app``.


Conventions for handlers
------------------------

Webapp2 handlers must be defined in ``app/[module]/[module]_handler.py``. Unlike with endpoints, the classes are not discovered, rather, the routes are. Every handler file must contain a global ``webapp2_routes`` variable defining the list of routes available. For example::

    webapp2_routes = [
        webapp2.Route('/hello', HelloHandler)
    ]


Using discovery
---------------

The generator and the boilerplate repository both contain a working ``main.py`` for the application, however, if you find yourself wanting to modify or create one manually this information could be helpful.

Before calling discovery you should make sure all endpoint configuration files are loaded. Typically this is done by importing a ``endpoints_config.py`` within ``appengine_config.py``. The ``endpoints_config.py`` should be something like::

    # Load the default endpoint or any other endpoints used by the application here
    # It's important to do this before discovery because if the endpoint isn't available
    # the classes will throw and error when trying to register.
    endpoints.add('app/default-api.yaml', default=True)

To discover all endpoint services in the application use :func:`discover_api_services`::

    import endpoints as cloud_endpoints
    from ferris3.discovery import discover_api_services

    API_CLASSES = discover_api_services()
    API_APPLICATION = cloud_endpoints.api_server(API_CLASSES)

You can then expose this in ``app.yaml`` using::

    handlers:
    # Endpoints handler
    - url: /_ah/spi/.*
      script: main.API_APPLICATION

Using discovery with handlers is very similar using :func:`discover_webapp2_routes`::

    from ferris3.discovery import discover_webapp2_routes
    import webapp2

    WSGI_ROUTES = discover_webapp2_routes()
    WSGI_APPLICATION = webapp2.WSGIApplication(WSGI_ROUTES)

Exposing in ``app.yaml`` is again similar::

    handlers:
    # WSGI handler
    - url: /.*
      script: main.WSGI_APPLICATION
