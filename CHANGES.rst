1.0 (2018-11-26)
================

- Fix a bug in ``exclude_prefixes`` where it only matches the first request
  on Python 3.

0.3.1 (2017-11-26)
==================

- Fix changelog.

0.3 (2017-11-26)
================

- Do not crash when the source header is missing. Instead set the request id
  to "-".

- Properly format the UTC offset in the ``{time}`` timestamp.

- Add 100% test coverage.

0.2.1 (2016-11-03)
==================

- Fix ``logging_level`` option on Python 3.
  See https://github.com/mmerickel/request-id/pull/2

0.2 (2016-08-09)
================

- Catch exceptions and return ``webob.exc.HTTPInternalServerError`` so
  that a ``request_id`` may be attached to the response.

0.1.2 (2016-07-26)
==================

- Fix a couple bugs with ``exclude_prefixes`` and add some docs for it.

0.1.1 (2016-07-26)
==================

- Add a new setting ``exclude_prefixes`` which can be used to avoid
  logging certain requests.

0.1.0 (2016-07-26)
==================

- Initial release.
