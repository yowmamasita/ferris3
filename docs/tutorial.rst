Ferris 3 Tutorial
=================

.. note::
    This tutorial is meant to be a quick guide on how to get a Ferris 3 project up and running and making some example api calls. It assumes you are familiar with Ferris 2 and explains Ferris 3 with this in mind.



A Simple “Posts” Service
------------------------

Let’s start with something easy to illustrate just how magical Ferris 3 actually is: a Posts API. This will also give us a chance to get accustomed to the new folder organization in Ferris.

Ferris 3 implements something called “fractal hierarchy”. Unlike Ferris 2, where all controllers and models were housed inside overarching “controllers” and “models” folders, respectively, in this new paradigm controllers, models, services, and anything else relating to a specific module are all housed inside a folder named after that module.

For instance, since we are building a Posts API, we will create a “posts” folder inside of the “app” folder. Now since Jon still hasn’t automated this yet, you still have to go through the gratuitous process of creating an empty __init__.py file right inside your posts folder. Feel free to scowl and send angry messages to Jon about this. (editor’s note: when google allows us to use python 3, we’ll no longer have to do this).

With that out of the way, create another file inside of the posts folder called “posts_api.py”. The convention here is to use “[Module Name]_api.py”. Inside this file we will define all the different methods we’d like our API to contain.

Before we start making methods to interact with Posts, we’ll need a Post model. We can accomplish this in two ways:

    1. Create a separate models.py file that contains the models we need.
    2. Define the model inside our posts_api.py file

For simplicity’s sake and because our Posts model is relatively trivial, we’re going to go with option 2 (note how strongly different this is from the Ferris 2 recommendations). We’ll need to import the Model class and the ndb module using the following lines:

from google.appengine.ext import ndb
from ferris3 import Model

An important thing to note here is that we are importing ndb from the appengine module, not the ferris3 module. There is an ndb package inside the ferris3 module, but it’s not the one we want.*

*Basically, ferris’ module names match the modules they supplement. So ferris.ndb supplements google.appengine.ext, ferris.messages supplements protorpc.message, and ferris.endpoints supplements endpoints.




Now lets add our simple Posts model::

    class Post(Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()

And voila, we have a Model to perform some basic methods with. To get started on the service itself, we’ll first need to import a few more commands from Ferris 3. Augment your import statement to include “auto_class”, “Service”, and “hvild”, so it looks something like this::

    from ferris3 import Model, Service, hvild, auto_class

“auto_class” is a method decorator that we will always use when defining our API service. “Service”e is what our class will extnd. Our class definition will look like this::

    @auto_class
    class PostsApi(Service):

Now we get to “hvild”. hvild is some Jon magic that will make your life incredibly easy when it comes to coding up a quick, simple API service. It functions very similarly to the scaffold module from Ferris 2. We can very quickly give the posts service some basic functionality with the following lines::

    list = hvild.list(Post)
    get = hvild.get(Post)
    delete = hvild.delete(Post)
    insert = hvild.insert(Post)
    update = hvild.update(Post)

That’s it, just set your methods equal to their hvild counterparts and pass in the model that the methods manipulate (in this case “Post”).
There is one more hvild method which will take just one ounce more effort to use, and that is paginated_list. The only difference is that along with the model, you must also pass in a “limit” parameter which will be the number of instances that appear on each page of the paginated list. In our case, let’s include 3 posts per page by adding this next line::

    paginated_list = hvild.list(Post, limit=3)

Now let’s test these methods! First we’re gonna need some posts in the datastore, and we can put them there in one of two ways. We can either use the interactive console (located at localhost:8000) just like we might have with Ferris 2, or we can use the insert method that we just had hvild build for us in the APIs Explorer. Either is fine, but we might as well use the Explorer just to get used to navigating through it.



.. reminder::

    To get to the Explorer, navigate to
    localhost:8080/_ah/api/explorer

From here, if you’ve done everything right, you should see “ferris API” in your list of APIs (and nothing else!). If it doesn’t show up, take a trip over to your terminal to see what the error is and fix it. Assuming you’ve followed this guide, it shouldn’t be anything more than a typo at this point.

After clicking on “ferris API”, you will be taken to a new list, this one of all the wonderful new services that we’ve just defined. Navigate to “ferris.posts.insert” to add some test posts.

From here, click inside the “Request body” input field and you will be given the option to choose a new property type add data for. We gave the Post model title and content properties, so you should see those along with a “key” property. A key will be generated automatically, so no need to manually define it. Just give your post a title and some content and click the pretty blue “Execute” button. You should receive a “200 Ok” notice of success, along with a copy of the JSON data that describes the post you have just created.

Create a few posts, and then navigate back to the list of services and choose “ferris.posts.paginated_lists”. Ignore the fields for now and click “Execute”. You should see some JSON code showing some of the posts you made. If you made 4 or more, it will show only 3 of them, and after the third one it should give you a “next_page_token”. This can be entered into the “page_token” field to see the next page.

Feel free to test some of the other services. Most of them will concern just one particular post, and will require the “urlsafe” item from a post’s key. Use it to delete, edit, or get a post.

But what if we want to reference a post without using its key? A key is (usually) a long string of random characters. Maybe we want to get a post with a specific title, or search for all posts with a reference to “Ferris 3” in their content. How would we go about something like that?


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

Note that since we imported f3, but not “auto_method” specifically, we had to address it through f3. We could’ve imported it specifically like we did with “auto_class” and then we wouldn’t have had to do so, or conversely we could’ve chosen not to import auto_class either and then could’ve used “f3.auto_class”. Until Ferris 3 conventions have been more rigidly defined, how you go about this is up to you.

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

