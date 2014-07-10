from google.appengine.ext import ndb
import types


def key(s):
    if isinstance(s, ndb.Key):
        return s
    return ndb.Key(urlsafe=s)


def get(ndbkey):
    if isinstance(ndbkey, types.StringTypes):
        ndbkey = key(ndbkey)
    return ndbkey.get()


def put(item):
    item.put()
    return item


def delete(item_or_key):
    if isinstance(item_or_key, types.StringTypes):
        item_or_key = key(item_or_key)
    if isinstance(item_or_key, ndb.Model):
        item_or_key = item.key
    item_or_key.delete()
    return item_or_key
