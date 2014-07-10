import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote
import ferris3
from google.appengine.ext import ndb
from ferris3 import hvild
import protopigeon


class SimpleMessage(messages.Message):
    message = messages.StringField(1)


class Post(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()


@endpoints.api(name='test', version='v1')
class TestApi(remote.Service):
    @ferris3.endpoints.auto_method(returns=SimpleMessage)
    def test(self, request):
        return SimpleMessage(message="Hi")

    get = hvild.get(Post)

APPLICATION = endpoints.api_server([TestApi])
