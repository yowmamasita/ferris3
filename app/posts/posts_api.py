import endpoints
from protorpc import remote
from google.appengine.ext import ndb
from ferris3 import hvild
from ferris3 import apis

api = apis.default()


class Post(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.TextProperty()


@api.api_class(resource_name='posts')
class PostsApi(remote.Service):

    list = hvild.list(Post)
    paginated_list = hvild.paginated_list(Post, limit=2, name='paginated_list')
    get = hvild.get(Post)
    delete = hvild.delete(Post)
    insert = hvild.insert(Post)
    update = hvild.update(Post)
