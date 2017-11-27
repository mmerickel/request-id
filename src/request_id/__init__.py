import logging
import threading
import time
import uuid

from webob.dec import wsgify
from webob.exc import HTTPInternalServerError

REQUEST_ID_KEY = 'X-Request-ID'

def make_filter(
    app,
    global_conf,
    logging_level=logging.INFO,
    exclude_prefixes=None,
    **kw
):
    if isinstance(logging_level, str):
        try:
            level_names = logging._nameToLevel
        except AttributeError:
            level_names = logging._levelNames
        if logging_level not in level_names:
            raise ValueError('Unknown logging level: %s' % logging_level)
        logging_level = level_names[logging_level]

    if exclude_prefixes is not None:
        exclude_prefixes = aslist(exclude_prefixes)

    kw['exclude_prefixes'] = exclude_prefixes
    kw['logging_level'] = logging_level
    return RequestIdMiddleware(app, **kw)

class RequestIdMiddleware(object):
    default_format = (
        '{REMOTE_ADDR} {HTTP_HOST} {REMOTE_USER} [{time}] '
        '"{REQUEST_METHOD} {REQUEST_URI} {HTTP_VERSION}" '
        '{status} {bytes} {duration} '
        '"{HTTP_REFERER}" "{HTTP_USER_AGENT}" - {REQUEST_ID}'
    )

    def __init__(
        self,
        app,
        logger_name='request_id',
        logging_level=logging.INFO,
        format=None,
        source_header=None,
        exclude_prefixes=None,
    ):
        self.app = app
        self.logger = logging.getLogger(logger_name)
        self.logging_level = logging_level
        self.format = format or self.default_format
        self.source_header = source_header
        self.exclude_prefixes = exclude_prefixes or []

    @wsgify
    def __call__(self, request):
        if self.logger.isEnabledFor(self.logging_level):
            start = time.time()
            response = self.track_request(request)
            duration = time.time() - start
            p = request.path_info
            if not any(p.startswith(e) for e in self.exclude_prefixes):
                self.write_log(
                    request,
                    time.localtime(start),
                    duration,
                    response.status_code,
                    response.content_length,
                )
        else:
            response = self.track_request(request)
        return response

    def track_request(self, request):
        request_id = get_request_id(request, _header=self.source_header)
        if self.source_header is not None and request_id == '-':
            self.logger.warn(
                'could not find request id in header="%s"',
                self.source_header)

        current_thread = threading.current_thread()
        old_name = current_thread.name
        try:
            current_thread.name = 'request=%s' % request_id

            response = request.get_response(self.app)
        except Exception:
            self.logger.exception(
                'unknown exception during request=%s', request_id)
            response = HTTPInternalServerError()
        finally:
            current_thread.name = old_name
        response.headers[REQUEST_ID_KEY] = request_id
        return response

    def write_log(self, request, start, duration, status, bytes):
        if bytes is None:
            bytes = '-'
        kw = {
            'REQUEST_ID': get_request_id(request),
            'REMOTE_ADDR': request.client_addr or '-',
            'REMOTE_USER': request.environ.get('REMOTE_USER') or '-',
            'REQUEST_METHOD': request.method,
            'REQUEST_URI': request.url,
            'REQUEST_PATH': request.path_qs,
            'HTTP_HOST': request.host,
            'HTTP_VERSION': request.environ.get('SERVER_PROTOCOL'),
            'HTTP_REFERER': request.environ.get('HTTP_REFERER', '-'),
            'HTTP_USER_AGENT': request.environ.get('HTTP_USER_AGENT', '-'),
            'time': time.strftime('%d/%b/%Y:%H:%M:%S %z', start),
            'duration': '%.3f' % duration,
            'bytes': bytes,
            'status': status,
        }
        message = self.format.format(**kw)
        self.logger.log(self.logging_level, message)

def get_request_id(request, _header=None):
    request_id = request.environ.get(REQUEST_ID_KEY, None)
    if request_id is None:
        if _header is not None:
            request_id = request.headers.get(_header, '-')
        else:
            request_id = str(uuid.uuid4())
        request.environ[REQUEST_ID_KEY] = request_id
    return request_id

def aslist(value):
    """
    Return a list of strings, separating the input based on newlines.

    """
    return filter(None, [x.strip() for x in value.splitlines()])
