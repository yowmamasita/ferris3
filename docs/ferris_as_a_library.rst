Ferris as a Library
===================

While Ferris provides a recommended directory structure and minimal integration with Google's webapp2 framework, Ferris can be used as library within any other framework that runs on Google App Engine.


Installation
------------

It's recommended that you setup vendoring via a tool like `Darth Vendor <https://github.com/jonparrott/Darth-Vendor>`_. You can then easily install ferris3 and all dependencies with ``pip``::

    pip install --target lib --pre Ferris


Usage
-----

You can now use the Ferris utilities by importing ``ferris3`` as usual. A full example of using `Ferris with Flask <https://github.com/jonparrott/flask-ferris-example>`_ is available on github.

