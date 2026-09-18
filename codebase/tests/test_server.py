import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import SourceStore
from server import Tutor, make_handler
from provider import ModelError


class FixtureClient:
    # External provider substitute used ONLY in tests, not available from UI.
    provider = 'test-fixture'
    model = 'not-live'
    key = ''
    output = '{"action":"answer","answer":"Token là đơn vị văn bản.","citations":["T04-001"],"clarifying_question":"","reason":"Có nguồn."}'

    def generate(self, question, context):
        return self.output, '{"test_fixture":true}'

    def check_config(self):
        pass

    def build_request(self, question, context):
        return 'test-only', {}, {}


class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        for n in ['04', '06']:
            (root / f'transcript-{n}-clean.md').write_text(f'**[T{n}-001]** Token là đơn vị văn bản.', encoding='utf-8')
        self.client = FixtureClient()
        self.tutor = Tutor(SourceStore(root), self.client, root / 'logs')
        self.server = ThreadingHTTPServer(('127.0.0.1', 0), make_handler(self.tutor))
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.tmp.cleanup()

    def post(self, data):
        return urlopen(Request(self.url + '/api/ask', json.dumps(data).encode(), {'Content-Type': 'application/json'}), timeout=3)

    def test_http_answer_saves_trace_and_correct_citation_opens(self):
        with self.post(dict(source_id='transcript-04', question='Token?')) as response:
            value = json.load(response)
        self.assertEqual(value['citations'], ['T04-001'])
        trace = json.loads((self.tutor.log_dir / (value['request_id'] + '.json')).read_text(encoding='utf-8'))
        self.assertEqual(trace['status'], 'validated')
        self.assertIn('raw_output', trace)
        with urlopen(self.url + '/api/segment?source_id=transcript-04&id=T04-001') as response:
            self.assertEqual(json.load(response)['text'], 'Token là đơn vị văn bản.')

    def test_invalid_model_output_is_error_and_raw_output_is_logged(self):
        self.client.output = '{not json}'
        with self.assertRaises(HTTPError) as caught:
            self.post(dict(source_id='transcript-04', question='Token?'))
        self.assertEqual(caught.exception.code, 502)
        caught.exception.close()
        traces = list(self.tutor.log_dir.glob('*.json'))
        self.assertEqual(len(traces), 1)
        self.assertEqual(json.loads(traces[0].read_text(encoding='utf-8'))['raw_output'], '{not json}')

    def test_wrong_source_citation_blocked_at_http_boundary(self):
        with self.assertRaises(HTTPError) as caught:
            urlopen(self.url + '/api/segment?source_id=transcript-06&id=T04-001')
        self.assertEqual(caught.exception.code, 400)
        caught.exception.close()

    def test_nonlocal_host_cannot_read_private_sources(self):
        request = Request(self.url + '/api/sources', headers={'Host': 'external.example'})
        with self.assertRaises(HTTPError) as caught:
            urlopen(request)
        self.assertEqual(caught.exception.code, 403)
        caught.exception.close()


if __name__ == '__main__':
    unittest.main()
