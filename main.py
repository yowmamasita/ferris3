import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import ferris3


class SimpleMessage(messages.Message):
    message = messages.StringField(1)


@endpoints.api(name='test', version='v1')
class TestApi(remote.Service):
    @ferris3.endpoints.auto_api(returns=SimpleMessage)
    def test(self, request):
        return SimpleMessage(message="Hi")


APPLICATION = endpoints.api_server([TestApi])
