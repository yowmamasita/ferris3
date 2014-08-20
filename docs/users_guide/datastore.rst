Datastore
=========

.. module:: ferris3.ndb

Ferris provides several supplemental utilities on top of the `NDB Datastore API <https://developers.google.com/appengine/docs/python/ndb/>`_. These utilities are intended to complement the items in the ``google.appengine.ext.ndb`` package. Items that share the same name are intended to be drop-in replacements.


The Model Class
---------------

Ferris includes a model class that inherits from ``ndb.Model`` and adds some additional functionality. Use of the Ferris model is completely optional and most ferris functionality works with standard ``ndb.Model`` objects.

.. autoclass:: Model

You define these models in the exact same was as you do with ndb::

    import ferris3
    from google.appengine.ext import ndb

    class Post(ferris3.ndb.Model):
        title = ndb.StringProperty()
        author = ndb.StringProperty()


Callbacks
---------

.. _model_callbacks:

The Model class also provides aliases for the callback methods. You can override these methods in your Model and they will automatically be called after their respective action.

.. automethod:: Model.before_put(self)
.. automethod:: Model.after_put(self, key)
.. automethod:: Model.before_get(cls, key)
.. automethod:: Model.after_get(cls, key, item)
.. automethod:: Model.before_delete(cls, key)
.. automethod:: Model.after_delete(cls, key)

These methods are useful for replicating database triggers, enforcing application logic, validation, search indexing, and more.


Behaviors
---------

Taking callbacks a bit further we get *Behaviors*. Behaviors are ways of packaging up related callbacks into a re-usable components. For example, you may write a behavior that notifies the creator of an item when their item is deleted. You can then attach this behavior to multiple models to easily add this functionality to multiple parts of your application. Such a behavior might look like this::
    
    class NotifyOnDelete(ferris3.ndb.Behavior):
        def before_delete(self, key):
            item = key.get()
            send_delete_notification(item.author, item.title)

This behavior can be attached to any model that has an ``author`` and ``title`` field::

    class Post(ferris3.ndb.Model):
        class Meta:
            behaviors = (NotifyOnDelete,)

        title = ndb.StringProperty()
        author = ndb.StringProperty()

Behaviors can be combined and each behavior's callbacks are triggered along with the model's. So for example if you wanted to use ``NotifyOnDelete`` as well as a new behavior like ``FixTitle``::

    class Post(ferris3.ndb.Model):
        class Meta:
            behaviors = (NotifyOnDelete, FixTitle)


By combining behaviors you can create models with deep logic out of small, discrete building blocks.


.. autoclass:: Behavior

.. automethod:: Behavior.before_put
.. automethod:: Behavior.after_put
.. automethod:: Behavior.before_get
.. automethod:: Behavior.after_get
.. automethod:: Behavior.before_delete
.. automethod:: Behavior.after_delete
