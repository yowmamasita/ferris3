Hvild
=====

.. module:: ferris3.hvild

Hvild is a collection of generic or "cookie-cutter" methods that help you implement CRUD functionality for your services quickly.

The basic concept is that instead of repeating this everywhere you need to implement ``insert`` functionality::

    @ferris3.auto_method(returns=PostMessage)
    def insert(cls, request=(PostMessage,)):
        entity = ferris3.messages.deserialize(Post, request)
        entity.put()
        msg = ferris3.messages.serialize(PostMessage, entity)
        return msg

You would just re-use the generic version::

    insert = ferris3.hvild.insert(Post)

You can implement a complete CRUD API in just a few lines::

    @ferris3.auto_service
    class PostsService(ferris3.Service):
        list = ferris3.hvild.paginated_list(Post, name="list")
        get = ferris3.hvild.get(Post)
        insert = ferris3.hvild.insert(Post)
        update = ferris3.hvild.update(Post)
        delete = ferris3.hvild.delete(Post)


Generic method arguments
------------------------

All of the generic methods require at least the ``Model`` parameter. The methods will then use :func:`~protopigeon.model_message` and :func:`~protopigeon.list_message` where needed to fill in the gaps.

You can of course provide your own messages if desired. For example, if we wanted to create a list of posts that only contained the title::

    PostTitleOnlyMessage = ferris3.model_message(Post, only=('title',))

    ...

    title_only_list = ferris3.hvild.list(Post, Message=PostTitleOnlyMessage, name="title_only_list")


Additionally, all of the methods accept the ``name`` parameter to allow you to control what the API method name is when exposed to Google Cloud Endpoints. This is very important in the case of multiple uses of the generic method, for example::

    full_list = ferris3.hvild.list(Post, Message=PostTitleOnlyMessage, name="full_list")
    title_only_list = ferris3.hvild.list(Post, Message=PostTitleOnlyMessage, name="title_only_list")

Without specifying ``name``, these two functions would have the name API method name and would cause an error.


Generic methods
---------------

.. autofunction:: list
.. autofunction:: paginated_list
.. autofunction:: searchable_list
.. autofunction:: get
.. autofunction:: insert
.. autofunction:: update
.. autofunction:: delete


Under the hood
--------------

These generic methods are intended to reduce redundancy and code reptition and not to serve all use cases. None of these methods are intended to be difficult to understand or re-implement. We encourage you to read the source code and create your own versions of the generic methods to suit your application's need.
