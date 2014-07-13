from google.appengine.ext import ndb
from ferris3 import Model


class TimeEntry(Model):
    user = ndb.UserProperty(indexed=False)  # Explicitly unindexed due to ancestor.
    date = ndb.DateProperty(indexed=False)  # Explicitly unindexed due to ancestor.
    order = ndb.IntegerProperty(indexed=True)

    project = ndb.StringProperty(indexed=False)
    notes = ndb.StringProperty(indexed=False)
    hours = ndb.FloatProperty(indexed=False)
    billable = ndb.BooleanProperty(indexed=False)

    @staticmethod
    def make_stream_key(user, date):
        return ndb.Key('TimeStream', '%s:%s' % (user.email(), date))

    @classmethod
    def list_stream(cls, user, date):
        return cls.query(ancestor=cls.make_stream_key(user, date)).order(cls.order)

    @classmethod
    def save_stream(cls, user, date, items):
        stream_key = TimeEntry.make_stream_key(user, date)
        t_items = []

        for item in items:
            if not item.key.parent() == stream_key:
                raise ValueError("Not in the correct stream")
            item.date = date
            item.user = user
            t_items.append(item)

        ndb.put_multi(t_items)
