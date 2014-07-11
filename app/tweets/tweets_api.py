from google.appengine.ext import ndb
from ferris3 import auto_class, hvild, Service


class Tweet(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()
    user = ndb.UserProperty()


@auto_class
class TweetsApi(Service):

    list = hvild.paginated_list(Tweet, limit=50, name='list')
    get = hvild.get(Tweet)
    delete = hvild.delete(Tweet)
    insert = hvild.insert(Tweet)
    update = hvild.update(Tweet)
