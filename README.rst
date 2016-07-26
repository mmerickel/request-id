request-id
==========

Attach a unique identifier to every request in your WSGI application.

``request-id`` is implemented as a WSGI middleware.

The package will do 3 things:

1. Generate a unique ``request_id`` identifier which will be stored in the
   WSGI ``environ`` and set as the ``X-Request-ID`` response header.

2. Rename the processing thread with the ``request_id`` such that any log
   messages output by the logger have the ``request_id`` attached.

3. Log the request to the Python stdlib logging library, which can be used
   to generate a simple access log.

Installation
------------

You may install the ``request-id`` package using pip::

  $ pip install request-id

Configure with PasteDeploy
--------------------------

Update your application INI to run in a pipeline with the ``request-id``
filter::

  [app:myapp]
  use = egg:myapp

  [filter:request-id]
  use = egg:request-id
  format = {status} {REQUEST_METHOD:<6} {REQUEST_PATH:<60} {REQUEST_ID}

  [pipeline:main]
  request-id
  myapp

  [loggers]
  keys = translogger

  [handlers]
  keys = translogger

  [formatters]
  keys = minimal

  [logger_translogger]
  level = INFO
  handlers = translogger
  qualname = request_id
  propagate = 0

  [handler_translogger]
  class = StreamHandler
  args = (sys.stderr,)
  level = NOTSET
  formatter = minimal

  [formatter_minimal]
  format = %(message)s

Configure in code
-----------------

Create a ``RequestIdMiddleware`` object and compose it with your WSGI
application:

.. code-block:: python

  from request_id import RequestIdMiddleware
  from wsgiref.simple_server import make_server

  def app(environ, start_response):
      start_response('200 OK', [('Content-Type', 'text/plain')])
      yield 'Hello World\n'

  app = RequestIdMiddleware(
      app,
      format='{status} {REQUEST_METHOD:<6} {REQUEST_PATH:<60} {REQUEST_ID}',
  )

  if __name__ == '__main__':
      server = make_server('0.0.0.0', 8080, app)
      server.serve_forever()

Access the request_id
---------------------

The ``request_id`` is stored in the request ``environ`` dictionary and may
be accessed from anywhere this is available using
``request_id.get_request_id(request)`` where ``request`` is an instance of
``webob.request.Request``.

Settings
--------

``logger_name``
  The name of the Python stdlib logger to which the log output will be
  delivered. Default: ``request_id``

``logging_level``
  The name of the Python stdlib logging level on which request information
  will be output. Default: ``INFO``

``format``
  A formatting string using `PEP-3101`_ string format syntax. Possible
  options are:

  - ``REQUEST_ID``
  - ``REMOTE_ADDR``
  - ``REMOTE_USER``
  - ``REQUEST_METHOD``
  - ``REQUEST_URI``
  - ``REQUEST_PATH``
  - ``HTTP_HOST``
  - ``HTTP_VERSION``
  - ``HTTP_REFERER``
  - ``HTTP_USER_AGENT``
  - ``time``
  - ``duration``
  - ``bytes``
  - ``status``

  Default: ``'{REMOTE_ADDR} {HTTP_HOST} {REMOTE_USER} [{time}] "{REQUEST_METHOD} {REQUEST_URI} {HTTP_VERSION}" {status} {bytes} {duration} "{HTTP_REFERER}" "{HTTP_USER_AGENT}" - {REQUEST_ID}``

``source_header``
  If not ``None`` then the ``request_id`` will be pulled from this header
  in the request. This is useful if another system upstream is setting a
  request identifier which you want to use in the WSGI application.
  Default: ``None``

``exclude_prefixes``
  A (space or line separated) list of URL paths to be ignored based on
  ``request.path_info``. Paths should have a leading ``/`` in order to match
  properly. Default: ``None``

Acknowledgements
----------------

This code is heavily based on the translogger middleware from `Paste`_.

.. _PEP-3101: https://www.python.org/dev/peps/pep-3101/
.. _Paste: http://pythonpaste.org/
