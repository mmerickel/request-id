from webob.dec import wsgify
from webob import Response
import webtest

import request_id

@wsgify
def dummy_app1(request):
    return Response('foo', status_code=200)

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
