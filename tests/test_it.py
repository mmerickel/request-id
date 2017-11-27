import logging
import pytest
from webob.dec import wsgify
from webob import Response
import webtest

import request_id

@wsgify
def dummy_app1(request):
    logging.info('dummy_app1 test message')
    if request.path_info == '/fail':
        raise Exception
    return Response(
        'foo', status_code=200,
        headers={
            'xrid': request_id.get_request_id(request) or '-',
        },
    )

def test_disabled_via_log_level(caplog):
    caplog.set_level(logging.INFO, logger='request_id')
    wrapped_app = request_id.make_filter(
        dummy_app1, {},
        logging_level='DEBUG',
    )
    app = webtest.TestApp(wrapped_app)
    app.get('/')
    records = filter_records(caplog.records, 'request_id')
    assert len(records) == 0

def test_header_in_message(caplog):
    wrapped_app = request_id.make_filter(dummy_app1, {})
    app = webtest.TestApp(wrapped_app)
    response = app.get('/')
    xrid = response.headers['xrid']
    rec = filter_records(caplog.records, 'root')[0]
    assert 'request={}'.format(xrid) in rec.threadName

def test_source_header(caplog):
    wrapped_app = request_id.make_filter(
        dummy_app1, {},
        source_header='src-req-id',
    )
    app = webtest.TestApp(wrapped_app)
    app.get('/', headers={
        'src-req-id': 'fooreqid',
    })
    rec = filter_records(caplog.records, 'request_id')[0]
    assert 'fooreqid' in rec.message

def test_source_header_missing(caplog):
    wrapped_app = request_id.make_filter(
        dummy_app1, {},
        source_header='src-req-id',
    )
    app = webtest.TestApp(wrapped_app)
    app.get('/')
    rec = filter_records(caplog.records, 'request_id', logging.WARN)[0]
    assert 'could not find request id in header' in rec.message

def test_exclude_prefixes(caplog):
    wrapped_app = request_id.make_filter(
        dummy_app1, {},
        exclude_prefixes='/foo/',
    )
    app = webtest.TestApp(wrapped_app)
    app.get('/foo/bar/baz')
    records = filter_records(caplog.records, 'request_id')
    assert len(records) == 0

def test_error_caught():
    wrapped_app = request_id.make_filter(dummy_app1, {})
    app = webtest.TestApp(wrapped_app)
    response = app.get('/fail', expect_errors=True)
    assert 'X-Request-Id' in response.headers

def test_unrecognized_log_level():
    with pytest.raises(ValueError):
        request_id.make_filter(dummy_app1, {}, logging_level='DOESNTEXIST')

def filter_records(records, logger, level=None):
    return [
        rec
        for rec in records
        if rec.name == logger and (
            level is None
            or rec.levelno == level
        )
    ]
