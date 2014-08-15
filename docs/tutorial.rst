Tutorial
=================

This tutorial will walk you through creating a simple API. If you haven't yet, be sure to read through the :doc:`introduction` and :doc:`getting_started` section. This assumes you've already created a new project.


A Simple “Posts” Service
------------------------

Let’s start with something easy to illustrate just how magical Ferris 3 actually is: a Posts Service.

First we will create a “posts” folder inside of the “app” folder.

.. note::
    For a refresher on how the new folder structure works, take a look at the :doc:`introduction` again. Also recall that python requires any and every folder you create in your project will need an empty __init__.py file inside of it.
    (Note: when Google allows us to use Python 3, we’ll no longer have to do this, c'mon, Google!)

Now we'll create the service file. The convention here is to use “[Service Name]_servcice.py”, or in this case "posts_service.py". Inside this file we will define all the different methods we’d like our Service to contain.

Before we start making methods to interact with Posts, however, we’ll need an actual Post model. We can accomplish this in two ways:

    1. Create a separate models.py file that contains the models we need.
    2. Define the model inside our service file.

For simplicity’s sake, and because our Posts model is relatively trivial, we’re going to go with inline option. While it may seem to fly in the face of traditional MVC conventions, we feel there's no need to make this any more complicated.

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

And voila, we have a model to perform some basic methods with. To get started on the service itself, we’ll first need to import a few more commands from Ferris 3. Augment your import statement to include “auto_service”, “Service”, and “hvild”, so it looks something like this::

    from ferris3 import Model, Service, hvild, auto_service

"auto_service" is a method decorator that we will always use when defining our API service. “Service” is what our class will extnd. Our class definition will look like this::

    @auto_class
    class PostsApi(Service):

Now we get to “hvild”. hvild is where Ferris 3 truly shines, as it will allow you to generate API methods like insert, get, update, delete, etc. quickly and painlessly. Those familiar with Ferris 2 will find it to be very similar to "scaffold". Lets give our posts service some basic functionality with the following lines::

    list = hvild.list(Post)
    get = hvild.get(Post)
    delete = hvild.delete(Post)
    insert = hvild.insert(Post)
    update = hvild.update(Post)

That’s it, just set your methods equal to their hvild counterparts and pass in the model that the methods manipulate (in this case “Post”).


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


There are two more hvild methods which will take just an ounce more effort to use, and those are paginated_list and search. The only difference is that along with the model, you must also pass in a “limit” parameter which will be the number of instances that appear on each page of the results. In our case, let’s include 3 posts per page by adding these lines::

    paginated_list = hvild.list(Post, limit=3)
    search = hvild.search(Post, limit=3)


Using the Google APIs Explorer
------------------------------

Now let’s test these methods! First we’re gonna need some posts in the datastore. We can put them there in one of two ways: We can either use the interactive console (located at localhost:8000) just like we might have with Ferris 2, or we can use the insert method in the APIs Explorer that we just had hvild build for us. Either is fine, but we might as well use the Explorer just to get used to navigating through it.


.. note::

    To get to the Explorer, navigate to
    localhost:8080/_ah/api/explorer

From here, if you’ve done everything right, you should see “ferris API” in your list of Endpoints (and nothing else probably). If it doesn’t show up, take a trip over to your terminal to see what the error is and fix it. Assuming you’ve followed this guide, it shouldn’t be anything more than a typo.

After clicking on “ferris API”, you will be taken to a new list, this one of all the wonderful new services that we’ve just defined. Navigate to “ferris.posts.insert” to add some test posts.

From here, click inside the “Request body” input field and you will be given the option to choose a new property type add data for. We gave the Post model title and content properties, so you should see those along with a “key” property. A key will be generated automatically, so no need to manually define it. Just give your post a title and some content and click the pretty blue “Execute” button. You should receive a “200 Ok” notice of success, along with a copy of the JSON data that describes the post you have just created.

Create a few posts, and then navigate back to the list of services and choose “ferris.posts.paginated_lists”. Ignore the fields for now and click “Execute”. You should see some JSON code showing some of the posts you made. If you made 4 or more, it will show only 3 of them, and after the third one it should give you a “next_page_token”. This can be entered into the “page_token” field to see the next page.

Feel free to test some of the other services. Most of them will concern just one particular post, and will require the “urlsafe” item from a post’s key. Use it to delete, edit, or get a post.

But what if we want to reference a post without using its key? A key is (usually) a long string of random characters. Maybe we want to get a post with a specific title, how would we go about something like that?


A Little More Complexity
------------------------

So let’s say you want to want to get a particular post, but you don’t know its key and all you remember about it is that its title was “Ferris 3 is Awesome”. How would we create a service that allows us to get a post by its title? Unfortunately hvild cannot do this for us, so we’re going to have to write a few more than just a line or two, but don’t fret! Ferris 3 will still make this a cinch!

First let’s go ahead and import the entire ferris3 module. It isn’t necessary to rename it, but shortening it to f3 will make things just a tiny bit quicker for us in the long run::

    import ferris3 as f3

Now we’re going to use some of the methods inside of the f3 module to create a model message for the Post model. Bear with me on this one it’s gonna be tough::

    PostMessage = f3.model_message(Post)

Huh, turns out that was totally painless. Creating messages in Ferris 3 is actually this simple. Model and List messages can be made in a snap. It’s also possible to reduce the amount of information that your message will contain using the “exclude” parameter, which I’ll show later. For now let’s get back to our “get by title” service.

When building a method we use a similar decorator as we did when we built the class::

    @f3.auto_method()

Note that since we imported f3, but not “auto_method” specifically, we had to address it through f3. We could’ve imported it specifically like we did with auto_service and then we wouldn’t have had to do so, or conversely we could’ve chosen not to import auto_class either and then could’ve used “f3.auto_class”. Until Ferris 3 conventions have been more rigidly defined, how you go about this is up to you.

“auto_method” take a few arguments, namely “returns” and “name”. “returns” is the type of message that the service will return, and “name” is the name that the service will appear under in the API explorer. We’re going to return an instance of the “PostMessage” that we recently defined, and we’ll call our service “get_by_title”::

    @f3.auto_method(returns=PostMessage, name="get_by_title")

Now we declare the method. We’ll also name it “get_by_title” for simplicity’s sake. The parameters we need to give it are “self”, “request”, and then the field that we will entering into the service, in this case “title”, equal to it’s type, in this case string. All together it should look like this::

    def get_by_title(self, request, title=(str,)):

Now all we need to do is use the Ferris 3 toolchain to get the Post we want, convert it into a PostMessage, and return it. I’ll show you how this is done and then break it down line by line for you::

    return f3.ToolChain(Post.query(Post.title==title)) \
             .ndb.get() \
             .raise_if(None, f3.NotFoundException()) \
             .ndb.check_kind(Post) \
             .messages.serialize(PostMessage) \
             .value()

