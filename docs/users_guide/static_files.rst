Static Files
============

By default Ferris doesn't setup any static file handlers and leaves it up to your particular use case. However, you can add a generic static file handler by including this in ``app.yaml``::

    handlers:
    # Static handler
    - url: /(.*)/static/(.*)
      static_files: app/\1/static/\2
      upload: app/.*/static/.*

    # Endpoints handler
    - url: /_ah/spi/.*
      script: main.API_APPLICATION

    # WSGI handler
    - url: /.*
      script: main.WSGI_APPLICATION


By including this line App Engine will expose all files under ``app/[module]/static/[file]`` as ``/[module]/static/[file]``. For example if you have ``app/posts/static/post-icon.png`` you would be able to access it via ``/posts/static/post-icon.png``.
