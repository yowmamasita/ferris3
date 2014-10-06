from ferrisnose import AppEngineTest
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import search as search_api
from ferris3 import search
import ferris3
import datetime
import mock


class SearchTestModel(ferris3.ndb.Model):
    string = ndb.StringProperty()
    string2 = ndb.StringProperty()
    repeated_string = ndb.StringProperty(repeated=True)
    datetime = ndb.DateTimeProperty()  # auto_now_add=True is broken due to it calling now() locally instead of utcnow()
    person = ndb.UserProperty(auto_current_user=True)
    date = ndb.DateProperty(auto_now_add=True)
    time = ndb.TimeProperty()
    ref = ndb.KeyProperty()
    geopt = ndb.GeoPtProperty()
    repeated_number = ndb.IntegerProperty(repeated=True)
    blobkey = ndb.BlobKeyProperty()


class SearchTest(AppEngineTest):

    def _create_test_data(self):
        instance = SearchTestModel(
            string='123',
            repeated_string=['1', '2', '3'],
            datetime=datetime.datetime.utcnow(),
            person=users.User(email='a@example.com'),
            date=datetime.date.today(),
            time=datetime.time(4),
            ref=ndb.Key('Test', '123'),
            geopt=ndb.GeoPt(1, 2),
            repeated_number=[1, 2, 3])
        instance.put()
        return instance

    def test_searchable(self):
        search_index = search_api.Index(name='searchable:SearchTestModel')
        ins = self._create_test_data()
        b = search.Searchable(SearchTestModel)

        # Test auto-indexing
        b.after_put(ins)
        assert len(search_index.get_range().results) == 1

        # Test auto-removal
        b.before_delete(ins.key)
        assert len(search_index.get_range().results) == 0

        # Test multi-indexing
        SearchTestModel.Meta.search_index = ('searchable:SearchTestModel', 'global')
        b.after_put(ins)
        assert len(search_index.get_range().results) == 1
        assert len(search_api.Index(name='global').get_range().results) == 1

    def test_indexer(self):
        instance = self._create_test_data()

        indexed_fields = search.default_entity_indexer(instance, instance._properties.keys())

        assert len(indexed_fields) == 10  # -1 for the key, +1 for the datetime (creates two fields), +3 for the repeated string

    def test_index_and_unindex(self):
        instance = self._create_test_data()
        search_index = search_api.Index(name='test_index')

        search.index_entity(instance, index='test_index')

        # test indexing with custom converters
        converters = {
            ndb.StringProperty: mock.Mock(side_effect=lambda n, v: search_api.TextField(name=n, value=v))
        }
        search.index_entity(instance, index='test_index', extra_converters=converters)

        assert converters[ndb.StringProperty].called

        # test indexing with callback
        callback_mock = mock.Mock()
        search.index_entity(instance, index='text_index', callback=callback_mock)
        assert callback_mock.called

        # test error handler
        with mock.patch('ferris3.search.search_api.Index.put', side_effect=ValueError()):
            self.assertRaises(ValueError, search.index_entity, instance, index='test_index')

        # Test responses and translation
        response = search_index.get_range()
        assert len(response.results) == 1

        entities = search.to_entities(response)
        assert len(entities) == 1

        # Test unindexing
        search.unindex_entity(instance, index='test_index')

        response = search_index.get_range()
        assert len(response.results) == 0

    def test_search(self):
        instance = self._create_test_data()
        search.index_entity(instance, index='test_index')

        result = search.search('test_index', '')

        assert not result.error
        assert len(result.items) == 1

        results, error, next_page_token = search.to_entities(result)
        assert len(results) == 1

        # with sorting
        result = search.search('test_index', '', sort='string')

        assert not result.error
        assert len(result.items) == 1

        result = search.search('test_index', '', sort='-string')

        assert not result.error
        assert len(result.items) == 1

        result = search.search('test_index', '', sort=search_api.SortExpression('string'))

        assert not result.error
        assert len(result.items) == 1

        # test error handling
        with mock.patch('ferris3.search.search_api.Index.search', side_effect=search_api.Error(":(")):
            result = search.search('test_index', '', sort='-string')
            assert result.error

    def test_join_query(self):
        assert search.join_query(['blue', 'shoe']) == 'blue AND shoe'
        assert search.join_query(['blue', 'shoe'], parenthesis=True) == '(blue) AND (shoe)'
