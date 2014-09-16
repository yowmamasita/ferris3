Webapp2 Handlers
================

Although Ferris is designed for Google Cloud Endpoints, it provides some tooling for `webapp2 handlers <https://webapp-improved.appspot.com/>`__.


Defining Handlers
-----------------

Similar to endpoint services, handler are defined in the ``app`` directory using the convention ``app/[module]/[module]_handler.py``. By following the convention ferris will automatically discover and wire your handlers.

.. warning::
    If you do not follow the conventions then ferris can not automatically discover your handlers. See :doc:`discovery` for more details.


Inside of your handler file you can define webapp2 handlers as usual::

    import webapp2

    class HelloHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write("Hello, world!")

    webapp2_routes = [
        webapp2.Route('/hello', HelloHandler)
    ]


Notice the ``webapp2_routes`` at the bottom of the file. This is critically important as it tells ferris which routes to use for your handlers.


Using templates
---------------

You can use the built-in :doc:`template <templates>` module to render templates using `jinja2 <http://jinja.pocoo.org/>`__::

    from ferris3 import template

    class HelloHandler(webapp2.RequestHandler):
        def get(self):
            result = template.render("app/hello/hello.html")
            self.response.content_type = 'text/html'
            self.response.write(result)

