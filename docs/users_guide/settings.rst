Settings
========

.. module:: ferris3.settings

The settings module provides a way to specify application-wide settings in a centralized registry.


Configuration
-------------

To configure settings, use ``app/settings.py``. There will already be some defaults configured but you may add your own::

    settings['cats'] = {
        'herdable': False
    }


To read your settings, import ``ferris.settings`` and use :func:`get`::

    from ferris3 import settings

    HERDABLE = settings.get('cats').get('herdable')

.. warning:: Although you can, it's generraly not recommened to import ``app.settings`` directly. Using settings ensures that everything is loaded in the right order.


Functions
---------

.. autofunction:: get

.. autofunction:: all
