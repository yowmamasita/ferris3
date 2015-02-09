Search
======

.. module:: ferris3.search

Ferris provides some higher-level utilities on top of `App Engine's Search API <https://developers.google.com/appengine/docs/python/search/>`__. Notably ferris offers automatic translation of models into search documents via :func:`index_entity` and the :class:`Searchable` behavior as well as a highler-level query interface via :func:`search`.


Indexing models
---------------

You can easily add any entity to the full-text search index via :func:`index_entity`.

.. autofunction:: index_entity

.. note:: This function can not automatically index Computed, Key, or Blob properties. Use the search_callback to implement indexing for these fields.

Likewise, you can remove an entity via :func:`unindex_entity`. Note that this method only requires the key of the entity.

.. autofunction:: unindex_entity


Automatic index management
--------------------------

The :class:`Searchable` behavior will automatically add entities to the search index when saved and remove them when deleted::

    from ferris import Model
    from ferris.behaviors import searchable

    class Post(Model):
        class Meta:
            behaviors = (searchable.Searchable,)

        title = ndb.StringProperty()
        context = ndb.TextProperty()

.. autoclass:: Searchable

This behavior can be configured using the Meta class::

    class Meta:
        behaviors = (searchable.Searchable,)
        search_index = ('global', 'searchable:Post')
        search_exclude = ('thumbnail', 'likes')

.. attribute:: SearchableMeta.search_index

    Which search index to add the entity's data to. By default this is ``searchable:[Model]``. You can set it to a list or tuple to add the entity data to muliple indexes

.. attribute:: SearchableMeta.search_fields

    A list or tuple of field names to use when indexing. If not specified, all fields will be used.

.. attribute:: SearchableMeta.search_exclude

    A list or tuple of field names to exclude when indexing.

.. attribute:: SearchableMeta.search_callback

    A callback passed to :func:`~ferris.core.search.index_entity`. This can be used to index additional fields::

        from google.appengine.ext import ndb, search
        from ferris.behaviors.searchable import Searchable

        class Post(Model):
            class Meta:
                behaviors = (Searchable,)

                @static_method
                def search_callback(instance, fields):
                    category = instance.category.get()
                    fields.append(
                        search.TextField(
                            name="category",
                            value=category.title
                        )
                    )

            title = ndb.StringProperty()
            category = ndb.KeyProperty(Category)


Performing searches
-------------------

Ferris provides a slighly more pythonic wrapper for searching.

.. autofunction:: search


Transforming results into entities
----------------------------------

Search results alone are rarely what you want. Typically, we want to get the actual datastore entity we indexed. This is straightforward with :func:`to_entities`.

.. autofunction:: to_entities


For example::

    # Search all pages for "policies"
    results, error, next_page_token = search.search('searchable:Page', 'policies', limit=20)

    entities = search.to_entities(results)


Using search with endpoints
---------------------------

A search method can be added to an endpoint service easily using the building blocks above::

    import ferris3
    from google.appengine.ext import ndb

    class Page(ferris3.Model):
        class Meta:
            behaviors = (ferris3.search.Searchable,)

        title = ndb.StringProperty()
        content = ndb.TextProperty()

    PageMessage = ferris3.model_message(Page)
    PageListMessage = ferris3.list_message(PageMessage)

    @ferris3.auto_service
    class PagesService(ferris3.Service):

        @ferris3.auto_method(returns=PageListMessage)
        def search(self, request, query=(str,), page_token=(str,None)):
            
            # Get the index to search, because this is a searchable model it'll be 'searchable:Page'
            index = ferris3.search.index_for(Page)
            
            # Perform the query
            results, error, next_page_token = ferris3.search.search(index, query, limit=20, page_token=page_token)

            # Check for errors
            if error:
                raise ferris3.BadRequestException("Search error: %s" % error)

            # Translate to entities
            entities = ferris3.search.to_entities(results)

            # Translate to list message
            msg = ferris3.messages.serialize_list(PageListMessage, entities)

            return msg

The :mod:`~ferris3.hvild` module has a generic implementation of this called :func:`~ferris3.hvild.searchable_list`.
