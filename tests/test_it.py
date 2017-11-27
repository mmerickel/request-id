import logging
from webob.dec import wsgify
from webob import Response
import webtest

import request_id

@wsgify
def dummy_app1(request):
    logging.info('dummy_app1 test message')
    return Response(
        'foo', status_code=200,
        headers={
            'xrid': request_id.get_request_id(request),
        },
    )

def test_header_in_message(caplog):
    wrapped_app = request_id.make_filter(dummy_app1, {})
    app = webtest.TestApp(wrapped_app)
    response = app.get('/')
    xrid = response.headers['xrid']
    rec = [rec for rec in caplog.records if rec.name == 'root'][0]
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
    msg = [tup[2] for tup in caplog.record_tuples if tup[0] == 'request_id'][0]
    assert 'fooreqid' in msg

def test_exclude_prefixes(caplog):
    wrapped_app = request_id.make_filter(
        dummy_app1, {},
        exclude_prefixes='/foo/',
    )
    app = webtest.TestApp(wrapped_app)
    app.get('/foo/bar/baz')
    msgs = [tup[2] for tup in caplog.record_tuples if tup[0] == 'request_id']
    assert len(msgs) == 0
