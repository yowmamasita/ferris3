Common Patterns
===============

This section contains some approaches to common problems. If you have a recommedation, please feel free to reach out to us.


Adding extra information to messages
------------------------------------

Sometimes you want additional information to go along with your model data, here's a quick example::

    import ferris3 as f3
    import endpoints
    import protopigeon
    from protorpc import messages
    from google.appengine.ext import ndb


    # This is our example model.
    # it has two basic properties plus one method that provides
    # some extra information. 
    class Page(ndb.Model):
        title = ndb.StringProperty()
        content = ndb.TextProperty()

        def get_permissions():
            if endpoints.get_current_user().email() == 'admin@example.com':
                return ["read", "update", "delete"]
            else:
                return ["read"]


    # We'll create a standard message for our Model. This will have
    # the title and content fields.
    PageMessage = f3.messages.model_message(Page)


    # We'll use this message to hold the permissions.
    class WithPermissions(messages.Message):
        permissions = messages.StringField(1, repeated=True)


    # We'll use protopigeon to combine the two messages together.
    # This message will have title, content, and permissions fields.
    PageMessageWithPermissions = protopigeon.compose(PageMessage, WithPermissions)


    @f3.auto_service
    class PagesService(f3.Service):

        @f3.auto_method(returns=PageMessageWithPermissions)
        def get(self, request, id=(str,)):
            page = f3.ndb.get(id)
            if not page:
                raise f3.NotFoundException()

            # We serialize as usual using the combined message.
            # The serialization will handle the title and content fields.
            message = f3.messages.serialize(PageMessageWithPermissions, page)

            # Finally, we'll manually populate the permissions field.
            message.permissions = page.get_permissions()

            return message


Using custom properties with protopigeon
----------------------------------------

Sometimes it's desired to use a custom property or to override the built-in behavior for serializing properties. Here's an example::

    import ferris3
    import endpoints
    import protopigeon
    from protorpc import messages
    from google.appengine.ext import ndb
     
    
    # This is our custom property class.
    # We want ferris / protopigeon to automatically
    # serialize this in messages
    class ExampleProperty(ndb.StringProperty):
        def _to_base_type(self, value):
            return "---" + str(value) + "---"
     
        def _from_base_type(self, value):
            return value.strip('-')
    

    # A simple class that uses our custom property
    class ExampleModel(ndb.Model):
        normal = ndb.StringProperty()
        custom = ExampleProperty()
     
    
    # This converter will tell ferris / protopigeon how to
    # handle our custom property.
    class ExamplePropertyConverter(protopigeon.converters.Converter):
        @staticmethod
        def to_field(Model, property, count):
            return messages.StringField(count, repeated=property._repeated, required=property._required)
     
    
    # This tells protopigeon about our converter.
    protopigeon.converters.converters["ExampleProperty"] = ExamplePropertyConverter
     
    
    # Everything else happens automatically.
    @ferris3.auto_service
    class CustomService(ferris3.Service):
        list = ferris3.hvild.list(ExampleModel)
        insert = ferris3.hvild.insert(ExampleModel)
