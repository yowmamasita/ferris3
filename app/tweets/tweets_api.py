import endpoints
from protorpc import remote
from google.appengine.ext import ndb
from ferris3 import hvild


class Tweet(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    user = ndb.UserProperty()


@endpoints.api(name='tweets', version='v1')
class TweetApi(remote.Service):

    list = hvild.paginated_list(Tweet, limit=50, name='list')
    get = hvild.get(Tweet)
    delete = hvild.delete(Tweet)
    insert = hvild.insert(Tweet)
    update = hvild.update(Tweet)
