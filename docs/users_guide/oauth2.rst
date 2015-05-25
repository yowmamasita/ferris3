OAuth2
======

.. module:: ferris3.oauth2

Ferris provides utilities for interacting with Google's implementation of `OAuth2 Service Account Flow <https://developers.google.com/accounts/docs/OAuth2ServiceAccount>`_ as well as obtaining the access token from the active endpoints request. This makes it easy to obtain account credentials and access Google APIs.

This documentation assumes you have an understanding of OAuth2. If you'd like to read more on the subject of OAuth2 and how Google uses it please read `Google's documentation <https://developers.google.com/accounts/docs/OAuth2>`_.


Endpoints Credentials
---------------------

If your endpoint requires authentication then you can obtain the user's authorization token. You can use this to access Google APIs as long as the token was authorized for the appropriate scope. Do not that endpoints does not provide the refresh token so these access tokens are short-lived (at most 1 hour) so it is not advisable to store these credentials.

.. autofunction:: get_endpoints_credentials

Example of using this to get the user's information::

    from ferris3 import auto_service, auto_method, Service, oauth2, google_apis

    @auto_service
    class AuthInfoService(Service):

        @auto_method(returns=UserInfoMessage)
        def info(self, request):
            creds = oauth2.get_endpoints_credentials()
            client = google_apis.build('oauth2', 'v2', creds)

            r = client.userinfo().get().execute()
            logging.info(r)


Service Account Configuration
-----------------------------

In order to use Ferris' OAuth2 features, you must first configure client settings in ``app/settings.py``. The Google Developer Console provides service account credentials with a JSON file. You can load these directly::

    import json
    with open('app/service_account.json') as f:
        settings['oauth2_service_account'] = json.load(f)

Or you can manually configure it::

    settings['oauth2_service_account'] = {
        'client_id': None, # ...apps.googleusercontent.com
        'client_email': None,  # ..@developer.gserviceaccount.com
        'private_key' None,  # The private key in PEM format
    }


Using Service Accounts
----------------------

.. autofunction:: build_service_account_credentials

Example::

    credentials = build_service_account_credentials(
        scope=["https://www.googleapis.com/drive/file"],
        user="user@domain.com")

    credentials.authorize(http)


.. warning:: Service account credentials will not work properly on local development environments that are missing the PyCrypto or PyOpenSSL modules. If you get errors concerning SignedJwtCredentials check your Python installation.

.. note:: Ferris ensures that the access token is stored in the datastore/memcache to reduce calls to Google's authorization service and avoid quota issues.
