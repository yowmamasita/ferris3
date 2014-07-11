from google.appengine.ext import ndb
from ferris3 import hvild, auto_class, Service


class Post(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()


@auto_class
class PostsApi(Service):

    list = hvild.list(Post)
    paginated_list = hvild.paginated_list(Post, limit=2, name='paginated_list')
    get = hvild.get(Post)
    delete = hvild.delete(Post)
    insert = hvild.insert(Post)
    update = hvild.update(Post)
