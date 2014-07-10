import protopigeon
from google.appengine.ext import ndb


def serialize(MessageType, entity):
    if not isinstance(entity, ndb.Model):
        raise ValueError("%s is not an ndb model" % entity)
    return protopigeon.to_message(entity, MessageType)
