OAuth2
======

Ferris provides utilities for interacting with Google's implementation of `OAuth2 Service Account Flow <https://developers.google.com/accounts/docs/OAuth2ServiceAccount>`_. This makes it easy to obtain service account credentials and access Google APIs.

This documentation assumes you have an understanding of OAuth2. If you'd like to read more on the subject of OAuth2 and how Google uses it please read `Google's documentation <https://developers.google.com/accounts/docs/OAuth2>`_.

.. module:: ferris3.oauth2


Configuration
-------------

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
