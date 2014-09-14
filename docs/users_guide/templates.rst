Templates
=========

.. module:: ferris3.template

Templates are useful for rendering html for use in :doc:`mail` or :doc:`handlers`. Ferris provides a thin wrapper around `jinja2 <http://jinja.pocoo.org/>`__.


Rendering templates
-------------------

Templates can be easily rendered by using :func:`render`::

    from ferris3 import template

    context = {"greeting": "Hello!"}
    result = template.render("app/email/welcome.html", context)

Notice that the template path is relative to the root of the application. 


The environment
---------------

The jinja2 environment is available via :func:`environment`::

    temp_template = template.environment().from_string("<h1>{{greeting}}</h1>")
    result = temp_template.render({"greenting": "hello"})


You can also add globals, filters, extensions, etc.::

    template.environment().globals['user'] = endpoints.get_current_user()
    template.environment().filters['format_date'] = lambda x: x.strftime("%d-%m-%Y")
    template.environment().add_extension("jinja2.ext.autoescape")


Typically you'd do this in some auto-loaded file such as ``appengine_config.py``, ``main.py``, or ``app/settings.py``.
