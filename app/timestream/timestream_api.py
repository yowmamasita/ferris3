from ferris3 import auto_class, auto_method, Service, ApiChain, VoidMessage
import protopigeon
from .models import TimeEntry
import datetime
import endpoints


TimeEntryMessage = protopigeon.model_message(TimeEntry)
TimeEntryListMessage = protopigeon.list_message(TimeEntryMessage)


@auto_class
class TimestreamApi(Service):

    @auto_method(returns=TimeEntryListMessage)
    def list(self, request, year=(int,), month=(int,), day=(int,)):
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        return self._list(date)

    def _list(self, date):
        query = TimeEntry.list_stream(endpoints.get_current_user(), date)

        return ApiChain(query) \
            .messages.serialize_list(TimeEntryListMessage) \
            .value()

    @auto_method(returns=TimeEntryListMessage, http_method='POST')
    def update(self, request=(TimeEntryListMessage,), year=(int,), month=(int,), day=(int,)):
        user = endpoints.get_current_user()
        date = datetime.date(year=int(year), month=int(month), day=int(day))
        stream_key = TimeEntry.make_stream_key(user, date)

        items = [
            protopigeon.to_entity(item, TimeEntry(parent=stream_key))
            for item
            in request.items]

        TimeEntry.save_stream(user, date, items)

        return self._list(date)
