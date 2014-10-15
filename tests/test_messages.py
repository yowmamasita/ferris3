from ferrisnose import AppEngineTest
import ferris3
from google.appengine.ext import ndb
import mock


class SimpleModel(ndb.Model):
    content = ndb.StringProperty()

SimpleModelMessage = ferris3.messages.model_message(SimpleModel)
SimpleModelMessageCollection = ferris3.messages.list_message(SimpleModelMessage)


class MessagesTest(AppEngineTest):
    def test_serialization(self):
        entity = SimpleModel(content="Hello!")
        message = ferris3.messages.serialize(SimpleModelMessage, entity)
        assert entity.content == message.content
        back = ferris3.messages.deserialize(SimpleModel, message)
        assert entity.content == message.content == back.content

    def test_list_serialization(self):
        entities = [
            SimpleModel(content='1'),
            SimpleModel(content='2'),
            SimpleModel(content='3')
        ]

        message = ferris3.messages.serialize_list(SimpleModelMessageCollection, entities)

        assert len(message.items) == 3
        assert [x.content for x in message.items] == [x.content for x in entities]

        results = ferris3.ndb.PaginationResults(items=entities, next_page_token='meep')
        message = ferris3.messages.serialize_list(SimpleModelMessageCollection, results)

        assert len(message.items) == 3
        assert message.nextPageToken == 'meep'
