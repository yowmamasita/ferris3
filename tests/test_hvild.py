from ferrisnose import AppEngineTest
import ferris3
from ferris3 import hvild
from google.appengine.ext import ndb
import mock


class SimpleModel(ferris3.ndb.Model):
    class Meta:
        behaviors = (ferris3.search.Searchable,)

    content = ndb.IntegerProperty()


def invoke(method, **kwargs):
    service = mock.Mock()
    request = method.remote.request_type()
    for k, v in kwargs.iteritems():
        setattr(request, k, v)
    return method(service, request)


class HvildTest(AppEngineTest):
    def test_lists(self):
        for n in range(0, 15):
            SimpleModel(content=n).put()

        service_list = hvild.list(SimpleModel)
        result = invoke(service_list)
        assert len(result.items) == 15

        service_list_query = hvild.list(SimpleModel, query=lambda: SimpleModel.query())
        result = invoke(service_list_query)
        assert len(result.items) == 15

        service_paginated_list = hvild.paginated_list(SimpleModel, limit=10)
        result = invoke(service_paginated_list)
        assert len(result.items) == 10

        service_paginated_list_query = hvild.paginated_list(SimpleModel, limit=10, query=lambda: SimpleModel.query())
        result = invoke(service_paginated_list_query)
        assert len(result.items) == 10

        service_searchable_list = hvild.searchable_list(SimpleModel, limit=10)
        result = invoke(service_searchable_list)
        assert len(result.items) == 10

        # Test error handling with search
        self.assertRaises(
            ferris3.BadRequestException,
            invoke,
            service_searchable_list,
            query='(badquery')

    def test_insert(self):
        service_insert = hvild.insert(SimpleModel)

        result = invoke(service_insert, content=42)

        assert result.key.urlsafe
        assert result.content == 42
        assert SimpleModel.query().get().content == 42

    def test_get(self):
        key = SimpleModel(content=42).put()
        service_get = hvild.get(SimpleModel)

        result = invoke(service_get, item_key=key.urlsafe())

        assert result.key.urlsafe == key.urlsafe()
        assert result.content == 42

    def test_delete(self):
        key = SimpleModel(content=42).put()
        service_delete = hvild.delete(SimpleModel)

        invoke(service_delete, item_key=key.urlsafe())

        assert SimpleModel.query().count() == 0

    def test_update(self):
        key = SimpleModel(content=42).put()
        service_update = hvild.update(SimpleModel)

        result = invoke(service_update, item_key=key.urlsafe(), content=13)

        assert result.key.urlsafe == key.urlsafe()
        assert result.content == 13
        assert SimpleModel.query().get().content == 13
