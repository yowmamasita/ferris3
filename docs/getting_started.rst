Getting Started
===============

Installing pre-requisites
-------------------------

Ferris require installation of a handful of pre-requisites.

 1. Up-to-date installation of Python 2.7.x and pip.
 2. `Google Cloud SDK <https://developers.google.com/cloud/sdk/>`_ or alternatively, the `Google App Engine Python SDK <https://developers.google.com/appengine/downloads>`_.
 3. `PyOpenSSL <https://pypi.python.org/pypi/pyOpenSSL>`_ and `PyCrypto <https://pypi.python.org/pypi/pycrypto>`_.
 4. Optionally, `nose <https://pypi.python.org/pypi/nose>`_ and `ferrisnose <https://pypi.python.org/pypi/FerrisNose>`_.

The easiest way to generate projects is using Yeoman. To take advantage of this you'll need:
 
 1. `NodeJS <http://nodejs.org/>`_
 2. `Yeoman <http://yeoman.io/>`_
 3. `The Ferris 3 Generator <https://bitbucket.org/cloudsherpas/ferris-3-generator>`_

Starting a new project
----------------------


Running with the App Engine development server
----------------------------------------------

Using the development server with a Ferris application is the same as using it with any other App Engine application. Just issue ``dev_appserver.py`` . on unix/linux or use the `launcher <https://developers.google.com/appengine/training/intro/gettingstarted#starting>`_ on Windows/Mac. Once it's started you should be able to open up your app via http://localhost:8080. You should see a rather generic landing page.

.. note::
    If you're using the launcher, the URL for your application and the App Engine console may use a different port. Make note of this as the tutorial and examples all use http://localhost:8080 and http://localhost:8000 for the application and console respectively. 

.. tip::
    If you're running on linux or mac and want to use the command line tools (which are sometimes less frustrating than the launcher) you can use our `app-server <https://bitbucket.org/cloudsherpas/ubuntu-environment-bootstrap/src/master/app-server.sh>`_ script. This script insures that your data is persisted between reboots and sets some useful default flags.

.. note::
    Windows (and sometimes OSX) can be weird and really inconsistent when setting up an environment. If you run into trouble feel free to reach out to us on the mailing list. We recommend Ubuntu (or another flavor of linux) for development as setting up the Google Cloud SDK on linux is extremely easy. You can also use vagrant to run a headless ubuntu VM on Windows or OSX- we even have an example `Vagrantfile <https://bitbucket.org/cloudsherpas/ubuntu-environment-bootstrap/src/master/Vagrantfile>`_ to get you going. 
