import endpoints
from protorpc import messages
from ferris3 import auto_class, auto_method, Service


import os
from oauth2client.client import AccessTokenCredentials
from apiclient.discovery import build
import httplib2


def build_client(api, version):
    token = os.environ['HTTP_AUTHORIZATION'].split(' ').pop()
    credentials = AccessTokenCredentials(token, 'appengine:ferris')
    http = httplib2.Http()
    credentials.authorize(http)
    client = build(api, version, http=http)
    return client


class UserInfoMessage(messages.Message):
    name = messages.StringField(1)
    given_name = messages.StringField(2)
    family_name = messages.StringField(3)
    picture = messages.StringField(4)
    link = messages.StringField(5)
    hd = messages.StringField(6)
    verified_email = messages.BooleanField(7)
    gender = messages.StringField(8)
    email = messages.StringField(9)
    locale = messages.StringField(10)


@auto_class
class AuthInfoApi(Service):

    @auto_method(returns=UserInfoMessage)
    def info(self, request):
        client = build_client('oauth2', 'v2')

        m = UserInfoMessage()
        r = client.userinfo().get().execute()

        for field in UserInfoMessage.all_fields():
            field_name = field.name
            setattr(m, field_name, r.get(field_name))

        return m
