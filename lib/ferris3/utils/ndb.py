from google.appengine.ext import ndb
import types


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
