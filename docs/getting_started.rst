Getting Started
===============

This section walks you through setting up your environment and creating an empty Ferris project. For an introduction to what Ferris is and how it can help, see :doc:`introduction`.


Installing pre-requisites
-------------------------

Ferris requires installation of a handful of prerequisites.

 1. Up-to-date installation of Python 2.7.x and pip.
 2. `Google Cloud SDK <https://developers.google.com/cloud/sdk/>`_ or alternatively, the `Google App Engine Python SDK <https://developers.google.com/appengine/downloads>`_.
 3. `PyOpenSSL <https://pypi.python.org/pypi/pyOpenSSL>`_ and `PyCrypto <https://pypi.python.org/pypi/pycrypto>`_.
 4. Optionally, `nose <https://pypi.python.org/pypi/nose>`_ and `ferrisnose <https://pypi.python.org/pypi/FerrisNose>`_.

If you want to take advantage of the easiest way of using Ferris you'll need:
 
 1. `NodeJS <http://nodejs.org/>`_
 2. `Yeoman <http://yeoman.io/>`_
 3. `The Ferris 3 Generator <https://bitbucket.org/cloudsherpas/ferris-3-generator>`_

If you already have node, run::

    npm install -g yo generator-ferris

.. tip::
    Sometimes setting up an environment can be weird and difficult. We feel your pain. If you run into trouble feel free to reach out to us on the `mailing list <https://groups.google.com/forum/?fromgroups#!forum/ferris-framework>`_. We generally recommend Ubuntu for development as setting up the Google Cloud SDK on Linux is extremely easy. We've even written a `script to setup a complete environment <https://bitbucket.org/cloudsherpas/ubuntu-environment-bootstrap>`_ on Ubuntu. You can also use vagrant to run a headless Ubuntu VM on Windows or OSX; we even have an example `Vagrantfile <https://bitbucket.org/cloudsherpas/ubuntu-environment-bootstrap/src/master/Vagrantfile>`_ to get you going. 


Starting a new project
----------------------

As mentioned above, the easiest method of starting a new project is using yeoman. From the terminal::

    mkdir my-ferris-project
    cd my-ferris-project
    yo ferris

Yeoman will ask you a few questions (the defaults are usually fine) and generate a project for you.

Alternatively, if you do not wish to use Yeoman you can clone the `Ferris Boilerplate <TODO>`_ repository.


The App Engine Development Server
---------------------------------

Ferris uses the same App Engine development server as any other application. See Google's `documentation on using the development server <https://developers.google.com/appengine/docs/python/tools/devserver#Python_Running_the_development_web_server>`_.

.. note::
    If you're using the launcher, the URL for your application and the App Engine console may use a different port. Make note of this as the tutorial and examples all use http://localhost:8080 and http://localhost:8000 for the application and sdk console respectively. 

.. warning::
    When using ``dev_appserver.py`` with default configuration it stores all data in the ``/tmp`` directory which is deleted upon reboot. We have created an `app-server <https://bitbucket.org/cloudsherpas/ubuntu-environment-bootstrap/src/master/app-server.sh>`_ script that stores the data alongside the application.


The APIs Explorer
-----------------

By navigating to ``http://localhost:8080/_ah/api/explorer`` locally or ``https://your-app-id.appspot.com/_ah/api/explorer`` live you'll be able to browse and interact with the APIs explosed by your Ferris application. See Google's `documentation on testing APIs <https://developers.google.com/appengine/docs/python/endpoints/test_deploy>`_.


.. note::
    As mentioned above, your port may be different if using the App Engine Launcher.


Deploying
---------

Ferris applications are deployed just like any other App Engine application. See Google's `documentation on deploying applications <https://developers.google.com/appengine/docs/python/gettingstartedpython27/uploading>`_.


Continue
********

Continue on to the :doc:`tutorial` or dive into the :doc:`users_guide/index`.
