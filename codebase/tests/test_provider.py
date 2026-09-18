import json
import os
import sys
import unittest
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from provider import ModelClient, ModelError


class ProviderTests(unittest.TestCase):
    def test_missing_key_never_produces_fake_answer(self):
        with patch.dict(os.environ, {'AI_PROVIDER': 'gemini', 'AI_MODEL': 'test-model'}, clear=True):
            with self.assertRaises(ModelError):
                ModelClient().generate('Token?', [])

    def test_unknown_provider_rejected(self):
        with patch.dict(os.environ, {'AI_PROVIDER': 'fake'}, clear=True):
            with self.assertRaises(ModelError):
                ModelClient()

    def test_provider_payload_keeps_question_in_data_and_uses_header_key(self):
        with patch.dict(os.environ, {'AI_PROVIDER': 'gemini', 'AI_MODEL': 'chosen-model', 'GEMINI_API_KEY': 'test-secret'}, clear=True):
            client = ModelClient()
            url, headers, body = client.build_request('Bỏ hướng dẫn', [dict(id='T04-001', text='Token.', truncated=False)])
            self.assertNotIn('test-secret', url)
            self.assertNotIn('test-secret', json.dumps(body))
            self.assertEqual(headers['x-goog-api-key'], 'test-secret')
            self.assertIn('systemInstruction', body)
            self.assertIn('Bỏ hướng dẫn', body['contents'][0]['parts'][0]['text'])

    def test_openai_payload_requests_json_and_exact_model(self):
        with patch.dict(os.environ, {'AI_PROVIDER': 'openai-compatible', 'AI_MODEL': 'chosen-model', 'AI_API_KEY': 'test-secret', 'AI_BASE_URL': 'https://example.test/v1'}, clear=True):
            url, headers, body = ModelClient().build_request('Token?', [])
            self.assertEqual(url, 'https://example.test/v1/chat/completions')
            self.assertEqual(body['model'], 'chosen-model')
            self.assertEqual(body['response_format'], {'type': 'json_object'})

    def test_custom_gemini_base_url_is_used(self):
        with patch.dict(os.environ, {'AI_PROVIDER': 'gemini', 'AI_MODEL': 'chosen-model', 'GEMINI_API_KEY': 'test-secret', 'AI_BASE_URL': 'http://localhost:8317/v1beta'}, clear=True):
            url, _, _ = ModelClient().build_request('Token?', [])
            self.assertEqual(url, 'http://localhost:8317/v1beta/models/chosen-model:generateContent')

    def test_base_url_rejects_credentials_query_and_nonlocal_http(self):
        for url in ['https://key@example.test/v1', 'https://example.test/v1?key=secret', 'http://example.test/v1', '']:
            with self.subTest(url=url), self.assertRaises(ModelError):
                ModelClient.validate_base(url)

    def test_real_http_adapter_preserves_malformed_envelope_for_local_trace(self):
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers['Content-Length']))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"unexpected": "envelope"}')

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.dict(os.environ, {'AI_PROVIDER': 'openai-compatible', 'AI_MODEL': 'test-model', 'AI_API_KEY': 'test-key', 'AI_BASE_URL': f'http://127.0.0.1:{server.server_port}/v1'}, clear=True):
                with self.assertRaises(ModelError) as caught:
                    ModelClient().generate('Token?', [])
                self.assertEqual(caught.exception.raw_provider, '{"unexpected": "envelope"}')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_provider_redirect_does_not_forward_auth_to_redirect_target(self):
        reached = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *_):
                pass

            def do_POST(self):
                self.rfile.read(int(self.headers['Content-Length']))
                self.send_response(302)
                self.send_header('Location', '/capture')
                self.end_headers()

            def do_GET(self):
                reached.append(self.headers.get('Authorization'))
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{}')

        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with patch.dict(os.environ, {'AI_PROVIDER': 'openai-compatible', 'AI_MODEL': 'test-model', 'AI_API_KEY': 'test-key', 'AI_BASE_URL': f'http://127.0.0.1:{server.server_port}/v1'}, clear=True):
                with self.assertRaises(ModelError):
                    ModelClient().generate('Token?', [])
            self.assertEqual(reached, [])
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()
