Introduction
============

It's a good idea to read this before diving in to Ferris. This provides some background and answers common questions around why Ferris exists and what sort of problems it solves.


Developing in the Google Cloud
------------------------------

Ferris is intended to make it easier to develop modern applications within Google's Cloud Platform. Recently, there has been a significant shift away from monolithic server-side web application because of advancements in client-side technology. As the "MVC" and UI logic shifts to clients the role of the application server changes into something that no longer fits nicely into traditional MVC. Instead, the web application becomes an `API backend` and is responsible for exposing data and business logic to one or more frontend clients.

Ferris 3 is geared toward creating these API backends that run on Google App Engine and to streamline accessing that backend from various frontends running on various platforms such as HTML5, Android, and iOS. Ferris embraces the platform and extends `Google Cloud Endpoints <https://developers.google.com/appengine/docs/python/endpoints/>`_ with opinionated tools to make it faster and easier to create APIs.


Overall Application Structure
-----------------------------

Ferris constitutes just one part of your overall application structure. You would start with two basic pieces:
    
  1. **A backend created with Ferris**: This will provide APIs that can be consumed by various clients.
  2. **A web frontend created with HTML5 and JavaScript**: The user would interact with this frontend and the frontend would talk to the APIs provided by the ferris application.

As your application grows, you may wish to add additional frontends such as Android, iOS, native Windows, PhoneGap, etc. Ferris makes this easier because your backend is separate and independent of your frontend. Google Cloud Endpoints provices client libraries for most languages and platforms. Ferris does not dictate how you build your frontend- you could even create a frontend using a traditional monolithic MVC framework and use your Ferris-based application as a service.


Convention, Configuration, and Structure
----------------------------------------

Ferris is relatively opinionated about application structure, however, ferris is flexible and there's always a way to configure it to do something differently. Our manta is to optimize for the common case but not at the expense of other cases. It's also part of our philosophy that if you're using another web framework on App Engine you should be able to use parts of Ferris that you find useful (such as model behaviors and search helpers).


Supplemental, not inclusive
---------------------------

Similar to the JavaScript idea of wrapping the DOM instead of extending is, most of Ferris `supplements` another module. For example, Ferris provides many utilities around App Engine's ``ndb`` module. You use ferris' ndb along with app engine's ndb, not instead of it::

    import ferris3
    from google.appengine.ext import ndb


    class Model(ferris3.ndb.Model):
        title = ndb.StringProperty()

        def before_put(self):
            self.title = self.title.lower()


Notice that we still use ``ndb``, we just use ``ferris3.ndb`` along side it. This pattern is oft repeated in ferris. ``ferris3.messages`` supplements ``protorpc.messages``, ``ferris3.endpoints`` supplements ``endpoints``, and so on.


Organization by feature, not function
-------------------------------------

Ferris applications are generally organized by feature which is in contrast to MVC frameworks that organize by structure. For example, a typical MVC application would have a structure like so::

    controllers
        - posts.py
        - pages.py
        - images.py
    models
        - post.py
        - page.py
        - image.py
        - user.py

Whereas in Ferris you would instead organize this application this way::

    posts
        - models.py
        - posts_api.py
    pages
        - models.py
        - pages_api.py
    images
        - models.py
        - images_api.py
    users
        - models.py

We believe this structure improves readability and makes it easier to maintain applications with large amounts of features.


Continue
********

Continue on to :doc:`getting_started` or the :doc:`tutorial`.
