from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
import types
from collections import namedtuple


def key(s):
    if isinstance(s, ndb.Model):
        return s.key
    if isinstance(s, ndb.Key):
        return s
    if isinstance(s, types.StringTypes):
        return ndb.Key(urlsafe=s)
    return None


def get(item):
    return key(item).get()


def put(item):
    item.put()
    return item


def delete(item):
    key(item).delete()
    return item


def check_kind(kind, item):
    if issubclass(kind, ndb.Model):
        kind = kind._get_kind()

    item_key = key(item)
    if not kind == item_key.kind():
        raise ValueError("Incorrect kind %s, expected %s" % (item_key.kind(), kind))

    return item


PaginationResults = namedtuple('PaginationResults', ['items', 'next_page_token'])


def paginate(query, limit=50, page_token=None):
    if page_token and not isinstance(page_token, Cursor):
        page_token = Cursor(urlsafe=page_token)
    
    # Force all falsy values into None
    if not page_token: 
        page_token = None

    data, next_cursor, more = query.fetch_page(limit, start_cursor=page_token)

    return PaginationResults(items=data, next_page_token=next_cursor.urlsafe() if more else None)
