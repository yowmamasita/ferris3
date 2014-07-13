from __future__ import absolute_import
import protopigeon
from .endpoints import auto_method
from .api_chain import ApiChain
from endpoints import NotFoundException
from protorpc import message_types
from ferris3.utils.messages import list_message

#
# Method implementations.
# Bare-bones, can be re-used in other methods and such.
#


def list_impl(ListMessage, query):
    return ApiChain(query) \
        .messages.serialize_list(ListMessage) \
        .value()


def paginated_list_impl(ListMessage, query, limit, page_token):
    return ApiChain(query) \
        .ndb.paginate(limit=limit, page_token=page_token) \
        .messages.serialize_list(ListMessage) \
        .value()


def get_impl(Model, Message, item_key):
    return ApiChain(item_key) \
        .ndb.get() \
        .raise_if(None, NotFoundException()) \
        .ndb.check_kind(Model) \
        .messages.serialize(Message) \
        .value()


def delete_impl(Model, item_key):
    return ApiChain(item_key) \
        .ndb.key() \
        .ndb.check_kind(Model) \
        .ndb.delete() \
        .value()


def update_impl(Model, Message, item_key, request):
    item = ApiChain(item_key) \
        .ndb.get() \
        .raise_if(None, NotFoundException()) \
        .ndb.check_kind(Model) \
        .value()

    return ApiChain(request) \
        .messages.deserialize(item) \
        .ndb.put() \
        .messages.serialize(Message) \
        .value()


def insert_impl(Model, Message, request):
    return ApiChain(request) \
        .messages.deserialize(Model) \
        .ndb.put() \
        .messages.serialize(Message) \
        .value()

#
# Full method wrappers.
# Can be used as endpoint methods directly.
#


def list(Model, Message=None, ListMessage=None, query=None, name='list'):
    if not Message:
        Message = protopigeon.model_message(Model)

    if not ListMessage:
        ListMessage = list_message(Message)

    if not query:
        query = Model.query()

    if callable(query):
        query = query()

    @auto_method(returns=ListMessage, name=name)
    def inner(self, request):
        return list_impl(ListMessage, query)

    return inner


def paginated_list(Model, Message=None, ListMessage=None, query=None, limit=50, name='list'):
    if not Message:
        Message = protopigeon.model_message(Model)

    if not ListMessage:
        ListMessage = list_message(Message)

    if not query:
        query = Model.query()

    if callable(query):
        query = query()

    @auto_method(returns=ListMessage, name=name)
    def inner(self, request, page_token=(str, '')):
        return paginated_list_impl(ListMessage, query, limit, page_token)

    return inner


def get(Model, Message=None, name='get'):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name=name)
    def inner(self, request, item_key=(str,)):
        return get_impl(Model, Message, item_key)

    return inner


def delete(Model, name='delete'):

    @auto_method(name=name, http_method='DELETE')
    def inner(self, request, item_key=(str,)):
        delete_impl(Model, item_key)
        return None

    return inner


def insert(Model, Message=None, name='insert'):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name=name, http_method='POST')
    def inner(self, request=(Message,)):
        return insert_impl(Model, Message, request)

    return inner


def update(Model, Message=None, name='update'):
    if not Message:
        Message = protopigeon.model_message(Model)

    @auto_method(returns=Message, name=name, http_method='POST')
    def inner(self, request=(Message,), item_key=(str,)):
        return update_impl(Model, Message, item_key, request)

    return inner
