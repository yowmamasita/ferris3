Testing
=======

.. module:: ferrisnose

Ferris provides utilities to test your application using the `nose <https://nose.readthedocs.org/en/latest/>`_ test runner.


Installing the nose plugin
--------------------------

`FerrisNose <https://pypi.python.org/pypi/FerrisNose>`_ is a nose plugin that allows you to run isolated Google App Engine tests. Install it via pip::

    pip install ferrisnose


.. note:: You may have to run this with ``sudo`` on Linux.

Running tests
-------------

To run tests just use nose::

    nosetests --with-ferris tests

.. warning::
    Be sure to specify a path or nose will try to discover all tests. We only need the test cases in /app/tests.

.. note::
    You may need to tell the plugin where to find your appengine directory. You can specify using ``--gae-sdk-path``::
    
        nosetests --with-ferris --gae-sdk-path /home/user/google_appengine tests

.. tip::
    
    Some libraries, especially ``ndb``, do a lot of debug logging. If these logs are getting in the way of figuring out why your tests are failing, specify ``--logging-level INFO``.

Testing recommendations
-----------------------

It's recommend to focus on testing the business logic of your application and not so much the glue that binds things together. Therefore, it's typical in a cloud endpoints application to test your models and any service layers around the models and not to spent too much effort testing your API services as they are mostly just glue. However, it is important to test more complicated translations between models and messages.

Mocking API calls
-----------------

Google has an `excellent guide on mocking API calls <https://developers.google.com/api-client-library/python/guide/mocks>`_.

Writing tests for models
------------------------

Models and other parts of the application that don't involve HTTP/WSGI (such as services) can be tested using :class:`AppEngineTest`.

.. autoclass:: AppEngineTest

Here is a simple example::

    from app.cats.models import Cat
    from ferrisnose import AppEngineTest

    class CatTest(AppEngineTest):
        def test_herding(self):
            Cat(name="Pickles").put()
            Cat(name="Mr. Sparkles").put()

            assert Cat.query().count() == 2


Writing tests for web request handlers
--------------------------------------

:class:`AppEngineWebTest` exposes a `webtest <http://webtest.pythonpaste.org/en/latest/>`_ instance so you can simulate a full web application. This is useful you testing any web request handlers you have in your applications.

.. autoclass:: AppEngineWebTest

You can easily add routes to ``testapp`` use :meth:`add_route` and :meth:`add_routes`.

.. automethod:: AppEngineWebTest.add_route
.. automethod:: AppEngineWebTest.add_routes

Here's an example of writing a test case::

    from app.cats import cats_handler
    from ferrisnose import AppEngineWebTest

    class CatsTest(AppEngineWebTest):
        def test_herding_method(self):
            self.add_routes(cats_handler.webapp2_routes)

            r = self.testapp.get('/cats')

            assert "Pickles" in r


Writing tests for cloud endpoints services
------------------------------------------

:class:`EndpointsTest` makes it easier to test endpoints services. It handles setting up the proper environment as well as configuring a ``webtest`` instance.

.. autoclass:: EndpointsTest

To add services to be tested use :meth:`add_service`.

.. automethod:: EndpointsTest.add_service

To login a user so that ``endpoints.get_current_user`` returns that user, use :meth:`login`.

.. automethod:: EndpointsTest.login

To invoke a service's method, use :meth:`invoke`. Note that you must use ``ClassName.method_name``.

.. automethod :: EndpointsTest.invoke

A complete example::

    from ferrisnose import EndpointsTest
    from app.guestbook import guestbook_service


    class TestGuestbook(EndpointsTest):

        def test_api(self):
            self.login("test@example.com")
            self.add_service(guestbook_service.GuestbookService)

            resp = self.invoke('GuestbookService.insert', {
                "content": "hello!"
            })

            assert resp['content'] == 'hello!'
            assert resp['author']['email'] == 'test@example.com'

            resp = self.invoke('GuestbookService.list')

            assert len(resp['items']) == 1
            assert resp['items'][0]['content'] == 'hello!'
