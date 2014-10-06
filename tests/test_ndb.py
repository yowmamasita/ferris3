from ferrisnose import AppEngineTest
from ferris3.ndb import Model, key, get, put, delete, check_kind, paginate
from google.appengine.ext import ndb


class SimpleModel(Model):
    content = ndb.StringProperty()


class OtherModel(Model):
    content = ndb.IntegerProperty()


class NdbTest(AppEngineTest):
    def test_helpers(self):
        entity = SimpleModel()
        entity.put()
        entity2 = OtherModel()
        entity2.put()

        assert key(entity) == entity.key
        assert key(entity.key) == entity.key
        assert key(entity.key.urlsafe()) == entity.key
        self.assertRaises(ValueError, key, 3)

        assert get(entity.key) == entity
        assert get(SimpleModel.query()) == entity
        assert put(entity) == entity

        delete(entity)
        assert SimpleModel.query().count() == 0

        assert check_kind(SimpleModel, entity) == entity
        self.assertRaises(ValueError, check_kind, SimpleModel, entity2)

    def test_pagination(self):
        for n in range(0, 15):
            OtherModel(content=n).put()

        query = OtherModel.query().order(OtherModel.content)

        results = paginate(query, limit=10)

        assert len(results.items) == 10
        assert results.next_page_token
        assert [x.content for x in results.items] == range(0, 10)

        results = paginate(query, page_token=results.next_page_token, limit=10)

        assert len(results.items) == 5
        assert not results.next_page_token
        assert [x.content for x in results.items] == range(10, 15)
