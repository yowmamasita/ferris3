import protopigeon
from protorpc import messages
from google.appengine.ext import ndb


def serialize(MessageType, entity):
    return protopigeon.to_message(entity, MessageType)


def deserialize(Model, message):
    return protopigeon.to_entity(message, Model)


def serialize_list(ListMessageType, entities):
    MessageType = ListMessageType.items.message_type
    message = ListMessageType()
    message.items = [serialize(MessageType, x) for x in entities]
    return message
