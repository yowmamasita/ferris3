import ferris3 as f3
from .models import TimeEntry
import datetime


TimeEntryMessage = f3.model_message(TimeEntry)
TimeEntryListMessage = f3.list_message(TimeEntryMessage)


@f3.auto_class
class TimestreamApi(Service):

    @f3.auto_method(returns=TimeEntryListMessage)
    def list(self, request, year=(int,), month=(int,), day=(int,)):
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        return self._list(date)

    def _list(self, date):
        query = TimeEntry.list_stream(f3.get_current_user(), date)

        return f3.ApiChain(query) \
            .messages.serialize_list(TimeEntryListMessage) \
            .value()

    @f3.auto_method(returns=TimeEntryListMessage, http_method='POST')
    def update(self, request=(TimeEntryListMessage,), year=(int,), month=(int,), day=(int,)):
        user = f3.get_current_user()
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        stream_key = TimeEntry.make_stream_key(user, date)

        items = [
            f3.deserialize(item, TimeEntry(parent=stream_key))
            for item
            in request.items]

        TimeEntry.save_stream(user, date, items)

        return self._list(date)
