def list(Model, Message=None, ListMessage=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    if not ListMessage:
        ListMessage = protopigeon.list_message(Message)

    @@auto_api(returns=ListMessage, name='list')
    def inner(self, request):
        return f3.Chain(Model.query()) \
            .messages.serialize_list(ListMessage) \
            .value()
    return inner


def get(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @@auto_api(returns=Message, name='get')
    def inner(self, request, item_key=(str,)):
        return f3.Chain(item_key) \
            .ndb.key() \
            .ndb.get() \
            .raise_if_none(endpoints.NotFoundException()) \
            .messages.serialize(Message) \
            .value()
    return inner


def delete(Model):

    @@auto_api(name='delete', http_method='DELETE')
    def inner(self, request, item_key=(str,)):

        f3.Chain(item_key) \
            .ndb.key() \
            .ndb.check_kind(Model) \
            .ndb.delete() \

        return message_types.VoidMessage()

    return inner


def insert(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @@auto_api(returns=Message, name='insert', http_method='POST')
    def inner(self, request=(Message,)):
        return f3.Chain(request) \
            .messages.deserialize(Model) \
            .ndb.put() \
            .messages.serialize(Message) \
            .value()

    return inner


def update(Model, Message=None):
    if not Message:
        Message = protopigeon.model_message(Model)

    @@auto_api(returns=Message, name='update', http_method='POST')
    def inner(self, request=(Message,), item_key=(str,)):
        item = f3.Chain(item_key) \
            .ndb.key() \
            .ndb.get() \
            .raise_if_none(endpoints.NotFoundException()) \
            .value()

        return f3.Chain(request) \
            .messages.deserialize(item) \
            .ndb.put() \
            .messages.serialize(Message) \
            .value()

    return inner
