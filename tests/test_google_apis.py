from ferrisnose import AppEngineTest
from ferris3 import google_apis
import mock
from apiclient.http import HttpError
import json


class GoogleApisTest(AppEngineTest):

    def test_retry(self):
        # Patch out sleep, so this doesn't pause.
        with mock.patch('time.sleep'):
            request = mock.Mock()

            # Test 5xx
            for code in (500, 501, 502, 503, 504):
                request.execute = mock.Mock(side_effect=make_fail_function(2, code, 'Test'))
                result = google_apis.retry_execute(request)
                assert request.execute.call_count == 3
                assert result == 'success'

            # Test retryable 403s
            for reason in ('rateLimitExceeded', 'userRateLimitExceeded'):
                request.execute = mock.Mock(side_effect=make_fail_function(2, 403, reason))
                result = google_apis.retry_execute(request)
                assert request.execute.call_count == 3
                assert result == 'success'

            # Test non-retryable 40x
            for code in (400, 401, 402, 403, 404):
                request.execute = mock.Mock(side_effect=make_fail_function(2, code, 'dailyLimitExceeded'))
                self.assertRaises(HttpError, google_apis.retry_execute, request)
                assert request.execute.call_count == 1

            # Test generic error
            request.execute = mock.Mock(side_effect=RuntimeError())
            self.assertRaises(RuntimeError, google_apis.retry_execute, request)
            assert request.execute.call_count == 1

            # Test bad json
            request.execute = mock.Mock(side_effect=make_fail_function(2, 400, use_json=False))
            self.assertRaises(HttpError, google_apis.retry_execute, request)
            assert request.execute.call_count == 1

    def test_discovery_doc_caching(self):
        http_patch = mock.patch('httplib2.Http.request', return_value=(200, 'test'))
        with http_patch as http:
            doc = google_apis._get_discovery_document('test', 'v1')
            assert doc == 'test'
            assert http.call_count == 1

            doc = google_apis._get_discovery_document('test', 'v1')
            assert doc == 'test'
            assert http.call_count == 1

            doc = google_apis._get_discovery_document('meep', 'v1')
            assert doc == 'test'
            assert http.call_count == 2

    def test_client_caching(self):
        from contextlib import nested

        http_patch = mock.patch('httplib2.Http.request', return_value=(200, 'test'))
        client_patch = mock.patch('apiclient.discovery.build')

        with nested(http_patch, client_patch) as (http, client):
            creds = mock.MagicMock()
            creds.to_json = mock.Mock(return_value="{}")

            google_apis.build("test", "v1", creds)
            assert client.call_count == 1

            google_apis.build("test", "v1", creds)
            assert client.call_count == 1

            google_apis.build("meep", "v1", creds)
            assert client.call_count == 2


def make_fail_function(times, code, reason=None, use_json=True):
    def fail(*args, **kwargs):
        if fail.times_called < times:
            fail.times_called += 1
            resp = mock.Mock()
            resp.status = code
            if use_json:
                content = {
                    'error': {
                        'code': code,
                        'errors': [{
                            'reason': reason
                        }]
                    }
                }
                raise HttpError(resp, json.dumps(content))
            else:
                raise HttpError(resp, '')

        return 'success'
    fail.times_called = 0
    return fail
