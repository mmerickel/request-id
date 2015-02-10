import logging
import threading
import time
import uuid

from webob.dec import wsgify

REQUEST_ID_KEY = 'X-Request-ID'

def includeme(config):
    config.add_request_method(get_request_id, 'id', property=True)

def make_filter(app,
                global_conf,
                logger_name='wsgi',
                logging_level=logging.INFO,
                ):
    if isinstance(logging_level, str):
        logging_level = logging._levelNames[logging_level]
    return Tracker(
        app,
        logger_name=logger_name,
        logging_level=logging_level,
    )

class Tracker(object):
    format = (
        '%(REMOTE_ADDR)s %(HTTP_HOST)s %(REMOTE_USER)s [%(time)s] '
        '"%(REQUEST_METHOD)s %(REQUEST_URI)s %(HTTP_VERSION)s" '
        '%(status)s %(bytes)s %(duration)s '
        '"%(HTTP_REFERER)s" "%(HTTP_USER_AGENT)s" - %(REQUEST_ID)s'
    )

    def __init__(self, app, logger_name='wsgi', logging_level=logging.INFO):
        self.app = app
        self.logger = logging.getLogger(logger_name)
        self.logging_level = logging_level

    @wsgify
    def __call__(self, request):
        if self.logger.isEnabledFor(self.logging_level):
            start = time.time()
            response = self.track_request(request)
            duration = time.time() - start
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
        request_id = get_request_id(request)

        current_thread = threading.current_thread()
        current_thread.name = 'request=%s' % request_id

        response = request.get_response(self.app)
        response.headers[REQUEST_ID_KEY] = request_id
        return response

    def write_log(self, request, start, duration, status, bytes):
        if bytes is None:
            bytes = '-'
        if time.daylight:
            offset = time.altzone / 60 / 60 * -100
        else:
            offset = time.timezone / 60 / 60 * -100
        if offset >= 0:
            offset = '+%0.4d' % offset
        elif offset < 0:
            offset = '%0.4d' % offset
        remote_addr = '-'
        if request.environ.get('HTTP_X_FORWARDED_FOR'):
            remote_addr = request.environ['HTTP_X_FORWARDED_FOR']
        elif request.environ.get('REMOTE_ADDR'):
            remote_addr = request.environ['REMOTE_ADDR']
        kw = {
            'REQUEST_ID': get_request_id(request),
            'REMOTE_ADDR': remote_addr,
            'REMOTE_USER': request.environ.get('REMOTE_USER') or '-',
            'REQUEST_METHOD': request.method,
            'REQUEST_URI': request.url,
            'HTTP_HOST': request.host,
            'HTTP_VERSION': request.environ.get('SERVER_PROTOCOL'),
            'HTTP_REFERER': request.environ.get('HTTP_REFERER', '-'),
            'HTTP_USER_AGENT': request.environ.get('HTTP_USER_AGENT', '-'),
            'time': time.strftime('%d/%b/%Y:%H:%M:%S ', start) + offset,
            'duration': '%.3f' % duration,
            'bytes': bytes,
            'status': status,
        }
        message = self.format % kw
        self.logger.log(self.logging_level, message)

def get_request_id(request):
    request_id = request.environ.get(REQUEST_ID_KEY, None)
    if request_id is None:
        request_id = str(uuid.uuid4())
        request.environ[REQUEST_ID_KEY] = request_id
    return request_id
