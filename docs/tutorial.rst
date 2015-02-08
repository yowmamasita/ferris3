Tutorial
=================

This tutorial will walk you through creating a simple API. If you haven't yet, be sure to read through the :doc:`introduction` and :doc:`getting_started` section. This assumes you have already created a new project- if not, head back to :doc:`getting_started` for instructions.


A Simple “Posts” Service
------------------------

To illustrate how quickly you can get a basic CRUD service up and running we'll create a simple "Posts" service. You could use service like this in a simple blog.

First we will create a ``posts`` folder inside of the ``app`` folder.

.. note::
    For a refresher on how the new folder structure works, take a look at the :doc:`introduction` again. Also recall that python requires all folders you create in your project will need an empty ``__init__.py`` file inside of it.
    (Note: when Google allows us to use Python 3, we’ll no longer have to do this, c'mon, Google!)

Next we'll create the service file. The convention here is to use ``[service_name]_service.py``, or in this case ``posts_service.py``. By following the convention, Ferris' discovery utility will find this file and automatically load it for us. Inside this file we will define all the different methods we’d like our service to contain.

Before we start making methods to interact with Posts, however, we’ll need an actual Post model. We can accomplish this in two ways:

    1. Create a separate ``models.py`` file that contains the models we need.
    2. Define the model inside our service file.

For the purpose of simplicity and because our Posts model is relatively simple, we’re going to go with inline option. While it may seem to fly in the face of traditional MVC conventions, we feel there's no need to make this any more complicated.

At this point you should have a file structure that looks like this::

    /app
        /posts
            /__init__.py
            /posts_service.py


Inside of ``posts_service.py`` we’ll need to import Ferris' Model class and the ndb module using the following lines::

    from google.appengine.ext import ndb
    from ferris3 import Model


.. note::
    Notice that we are importing ndb from the appengine module, not the ferris3 module. There is an ndb package inside the ferris3 module, but it’s not the one we want.

    Ferris’ module names match the modules they supplement. So ``ferris.ndb`` supplements ```google.appengine.ext.ndb``, ``ferris.messages`` supplements ``protorpc.messages``, ``ferris.endpoints`` supplements ```endpoints``, etc.


Now lets add our simple Posts model::

    class Post(Model):
        title = ndb.StringProperty()
        content = ndb.TextProperty()


You'll notice that we're using App Engine's built-in ``ndb`` here- this is a pattern that permeates Ferris as we embrace and extend the underlying platform.

Now that we have a model let's create service to expose an API that allows CRUD operations on our Post model. First we'll need to import a few more things from Ferris. Augment your import statement to include ``auto_service``, ``Service``, and ``hvild``, so it looks something like this::

    from ferris3 import Model, Service, hvild, auto_service

``Service`` will be the base class for our service and ``auto_service`` is a decorator that is used to automatically register and expose our service with Google Cloud Endpoints. Putting that all together our class definition looks like this::

    @auto_service
    class PostsService(Service):


Now we get to ``hvild``. Hvild is one of the more "magical" parts of Ferris and it will allow you to generate CRUD API methods like insert, get, update, delete, etc. quickly and painlessly. Those familiar with Ferris 2 will find it to be very similar to "scaffold". Lets give our posts service some basic functionality with the following lines::

    list = hvild.list(Post)
    get = hvild.get(Post)
    delete = hvild.delete(Post)
    insert = hvild.insert(Post)
    update = hvild.update(Post)


That's it, just set your methods equal to their hvild counterparts and pass in the model that the methods manipulate (in this case ``Post``).


To recap, our ``posts_service.py`` should look like this::

    from google.appengine.ext import ndb
    from ferris3 import Model, Service, hvild, auto_service


    class Post(Model):
        title = ndb.StringProperty()
        content = ndb.TextProperty()


    @auto_service
    class PostsService(Service):
        list = hvild.list(Post)
        get = hvild.get(Post)
        delete = hvild.delete(Post)
        insert = hvild.insert(Post)
        update = hvild.update(Post)


There are is another hvild method which will take just an ounce more effort to use: ``paginated_list``. The only difference is that along with the model you must also pass in a ``limit`` parameter which will be the number of entities that appear on each page of the results. In our case, let's include 3 posts per page by adding these lines::

    paginated_list = hvild.paginated_list(Post, limit=3)


Using the Google APIs Explorer
------------------------------

Now let's test these methods! First we're gonna need some posts in the datastore. We can put them there in one of two ways: We can either use the interactive console (located at ``localhost:8000``) or we can use the insert method in the APIs Explorer that we just had hvild build for us. Either is fine, but we might as well use the Explorer just to get used to navigating through it.


.. note::
    To get to the Explorer, navigate to http://localhost:8080/_ah/api/explorer. Remember, if you're using the launcher your ports may be different.


From here you should see "ferris API" in your list of available endpoints. If it doesn't show up, take a trip over to your terminal or error console to see what the error is and try to resolve it. Hopefully if you're following this guide it shouldn't be anything more than a typo.


.. tip::
    If you get stuck reach out to us via the `mailing list <https://groups.google.com/forum/?fromgroups#!forum/ferris-framework>`_. Ferris has a fantastic community!


After clicking on "Ferris API", you will be taken to a new list showing all of the new services that we've just defined. Navigate to "ferris.posts.insert" to add some test posts.

From here, click inside the "Request body" input field and you will be given the option to choose a new property type add data for. We gave the Post model ``title`` and ``content`` properties, so you should see those along with a ``id`` property. A id will be generated automatically so we do not need to manually define it. Just give your post a title and some content and click the blue "Execute" button. You should receive a ``200 OK`` notice of success along with a copy of the JSON data that describes the post you have just created.

Create a few posts, and then navigate back to the list of services and choose "ferris.posts.paginated_list". Ignore the fields for now and click "Execute". You should see some JSON showing some of the posts you made. If you made 4 or more, it will show only 3 of them, and after the third one it should give you a ``nextPageToken``. This can be entered into the ``pageToken`` field to see the next page.

Feel free to test some of the other services. Some of them will concern just one particular post and will require the ``id`` of an item. Use it to delete, edit, or get a post.


A Little More Complexity
------------------------

So let's say you want to want to get a particular post but you don't know its key and all you remember about it is that its title was "Ferris 3 is Awesome". How would we create a service that allows us to get a post by its title? Unfortunately hvild cannot do this for us so we're going to have to write a few more than just a line or two. But don't fret! Ferris 3 will still make this a cinch!

First let's go ahead and import the entire ``ferris3`` module. It isn't necessary to rename it, but shortening it to ``f3`` will make things just a tiny bit quicker for us in the long run::

    import ferris3 as f3

Now we're going to use some of the methods inside of the f3 module to create a model message for the Post model. Bear with me on this one it's gonna be tough::

    PostMessage = f3.model_message(Post)

Huh, turns out that was totally painless. Creating messages for ndb Models in Ferris 3 is actually this simple. Model and List messages can be made in a snap. It's also possible to reduce the amount of information that your message will contain using the ``exclude`` parameter which we'll demonstrate later. For now let's get back to our "get by title" method.

.. note::
    For more information about protorpc and messages see `Google's documentation <https://cloud.google.com/appengine/docs/python/tools/protorpc/>`_

When building a method we'll use a similar decorator as we did when we built the class::

    @f3.auto_method()


``auto_method`` takes a few optional arguments, namely ``returns`` and ``name``. ``returns`` is the type of message that the service will return and ``name`` is the name that the service will appear under in the API explorer. If you leave out ``returns`` then ferris will just expect you to return nothing. If you leave out ``name`` ferris will just use the name of the function as the method name. In this case, we're going to return an instance of the ``PostMessage`` that we recently defined and we'll call our method ``get_by_title`` even though we could have left that out::

    @f3.auto_method(returns=PostMessage, name="get_by_title")


Now we declare the method. We'll also name it ``get_by_title`` for consistency. The bare minimum parameters we need to give it are ``self`` and ``request``. However, since we want to take in another parameter called ``title`` we'll need to add that as well. All together it should look like this::

    def get_by_title(self, request, title=(str,)):


The syntax on the title parameter may look strange. Cloud endpoints needs to know the type of the parameter and this is our way of letting it know. The ``auto_method`` decorator will take care of the rest. We can also optionally give it a default value by doing ``title=(str, 'a default')``, but in this case we want it to be a required field.

What's next is to use the Ferris 3 toolchain to get the Post we want, convert it into a PostMessage, and finally return it. First we'll show the complete code then break it down line-by-line::

    query = Post.query(Post.title==title)
    post = query.get()
    if not post:
        raise f3.NotFoundException()
    if not post.key.kind() == 'Post':
        raise f3.InvalidRequestException()
    message = f3.messages.serialize(PostMessage, post)
    return message

Let's break this down:

    1. The first thing we do is create a standard ndb query using ``Post.query(Post.title==title)``.
    2. Next we call ``query.get()`` which will fetch the first record from the query. This should be the post we're after.
    3. The two ``if`` statements are sanity checks. First, we make sure we actually got an item back from the query, secondly, we make sure the item is actually a Post. (The kind check isn't strictly necessary here, however, you'll want to make sure you do this for any methods that use the id to get an item directly).
    4. Finally, we'll serialize our Post object into a message using ``messages.serialize`` and return it.


For reference, the final code for the tutorial is::

    from google.appengine.ext import ndb
    from ferris3 import Model, Service, hvild, auto_service
    import ferris3 as f3


    class Post(Model):
        title = ndb.StringProperty()
        content = ndb.TextProperty()


    PostMessage = f3.model_message(Post)


    @auto_service
    class PostsService(Service):
        list = hvild.list(Post)
        paginated_list = hvild.paginated_list(Post, limit=3)
        get = hvild.get(Post)
        delete = hvild.delete(Post)
        insert = hvild.insert(Post)
        update = hvild.update(Post)

        @f3.auto_method(returns=PostMessage, name="get_by_title")
        def get_by_title(self, request, title=(str,)):
            query = Post.query(Post.title==title)
            post = query.get()
            if not post:
                raise f3.NotFoundException()
            if not post.key.kind() == 'Post':
                raise f3.InvalidRequestException()
            message = f3.messages.serialize(PostMessage, post)
            return message


Where to go from here
---------------------

You've created your API backend so now you probably want to create some sort of front-end to talk to it. Most commonly you'll be writing a JavaScript client so head over to `Google's documentation on Javascript API Clients <https://developers.google.com/appengine/docs/python/endpoints/consume_js>`_. There's also guides for `Android <https://developers.google.com/appengine/docs/python/endpoints/consume_android>`_ and `iOS <https://developers.google.com/appengine/docs/python/endpoints/consume_ios>`_!

To dig deeper into what Ferris has to offer check out the :doc:`users_guide/index`.
