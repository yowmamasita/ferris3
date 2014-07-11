from __future__ import absolute_import
import protopigeon
from .endpoints import auto_method
from .api_chain import ApiChain
from endpoints import NotFoundException
from protorpc import message_types


def list(Model, Message=None, ListMessage=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    if not ListMessage:
        ListMessage = protopigeon.list_message(Message)

    @auto_method(returns=ListMessage, name='list')
    def inner(self, request):
        return ApiChain(Model.query()) \
            .messages.serialize_list(ListMessage) \
            .value()
    return inner


def get(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name='get')
    def inner(self, request, item_key=(str,)):
        return ApiChain(item_key) \
            .ndb.get() \
            .raise_if(None, NotFoundException()) \
            .messages.serialize(Message) \
            .value()
    return inner


def delete(Model):

    @auto_method(name='delete', http_method='DELETE')
    def inner(self, request, item_key=(str,)):

        ApiChain(item_key) \
            .ndb.key() \
            .ndb.check_kind(Model) \
            .ndb.delete()

        return message_types.VoidMessage()

    return inner


def insert(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name='insert', http_method='POST')
    def inner(self, request=(Message,)):
        return ApiChain(request) \
            .messages.deserialize(Model) \
            .ndb.put() \
            .messages.serialize(Message) \
            .value()

    return inner


def update(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name='update', http_method='POST')
    def inner(self, request=(Message,), item_key=(str,)):
        item = ApiChain(item_key) \
            .ndb.key() \
            .ndb.get() \
            .raise_if(None, NotFoundException()) \
            .value()

        return ApiChain(request) \
            .messages.deserialize(item) \
            .ndb.put() \
            .messages.serialize(Message) \
            .value()

    return inner
