import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote


class SimpleMessage(messages.Message):
    message = messages.StringField(1)


@endpoints.api(name='test', version='v1')
class TestApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, SimpleMessage)
    def test(self, request):
        return SimpleMessage(message="Hi")


APPLICATION = endpoints.api_server([TestApi])
