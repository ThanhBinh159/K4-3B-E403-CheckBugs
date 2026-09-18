"""Run with python codebase/server.py. Local-only teaching prototype."""
import json
import os
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from core import SourceStore, retrieve, validate_request, validate_response, parse_model_output, RETRIEVAL_VERSION
from provider import ModelClient, ModelError, PROMPT_VERSION, SYSTEM

ROOT = Path(__file__).resolve().parents[1]


def load_env():
    path = ROOT / '.env'
    if path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() in {'AI_PROVIDER', 'AI_MODEL', 'AI_API_KEY', 'GEMINI_API_KEY', 'OPENAI_API_KEY', 'AI_BASE_URL', 'VLEARN_DATA_DIR', 'VLEARN_SOURCE_KIND', 'VLEARN_SLIDES_DIR', 'PORT'}:
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def configured_store():
    kind = os.getenv('VLEARN_SOURCE_KIND', 'slides')
    variable = 'VLEARN_SLIDES_DIR' if kind == 'slides' else 'VLEARN_DATA_DIR'
    suffix = 'slides' if kind == 'slides' else 'transcript'
    path = Path(os.getenv(variable, '../K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/' + suffix))
    return SourceStore(path if path.is_absolute() else ROOT / path, kind=kind)


class Tutor:
    def __init__(self, store, client, log_dir):
        self.store, self.client, self.log_dir = store, client, Path(log_dir)

    def ask(self, request):
        data = validate_request(request, self.store)
        context = retrieve(self.store.sources[data['source_id']]['segments'], data['question'], data['selected_segment_ids'])
        request_id, start = uuid.uuid4().hex, time.perf_counter()
        trace = dict(request_id=request_id, timestamp=datetime.now(timezone.utc).isoformat(),
                     model=self.client.model, provider=self.client.provider, prompt_version=PROMPT_VERSION,
                     retrieval_version=RETRIEVAL_VERSION, parser_version='json-fence-v2', request=data, system_prompt=SYSTEM, context=context,
                     context_ids=[s['id'] for s in context], status='error')
        try:
            output, raw = self.client.generate(data['question'], context)
            trace.update(raw_provider=raw, raw_output=output)
            try:
                result = validate_response(parse_model_output(output), trace['context_ids'])
            except (ValueError, TypeError) as error:
                raise ModelError(f'Output AI không hợp lệ: {error}') from None
            trace.update(status='validated', response=result)
            return dict(result, request_id=request_id, source_id=data['source_id'], model=self.client.model,
                        latency_ms=round((time.perf_counter() - start) * 1000), context_ids=trace['context_ids'])
        except ModelError as error:
            trace['error'] = str(error)
            if error.raw_provider:
                trace['raw_provider'] = error.raw_provider
            raise
        finally:
            trace['latency_ms'] = round((time.perf_counter() - start) * 1000)
            self.log_dir.mkdir(parents=True, exist_ok=True)
            # Raw provider and source content stay local and gitignored.
            text = json.dumps(trace, ensure_ascii=False, indent=2)
            if getattr(self.client, 'key', ''):
                text = text.replace(self.client.key, '[REDACTED]')
            (self.log_dir / f'{request_id}.json').write_text(text, encoding='utf-8')


def make_handler(tutor, source_error=''):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send_json(self, status, value):
            body = json.dumps(value, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def local_host(self):
            allowed = {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}
            if self.headers.get('Host', '').casefold() not in allowed:
                self.send_json(403, {'error': 'Host không thuộc giao diện local.'})
                return False
            return True

        def do_GET(self):
            if not self.local_host():
                return
            url = urlsplit(self.path)
            if url.path in {'/', '/app.js', '/style.css'}:
                path = ROOT / 'codebase' / 'web' / ('index.html' if url.path == '/' else url.path[1:])
                body = path.read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', {'.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8'}[path.suffix])
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            if url.path == '/api/health':
                configured = False
                if tutor:
                    try:
                        tutor.client.build_request('Configuration check only', [])
                        configured = True
                    except ModelError:
                        pass
                self.send_json(200, dict(source_ready=bool(tutor), model_configured=configured,
                                        error=source_error, live_verified=False))
                return
            if not tutor:
                self.send_json(503, {'error': source_error})
                return
            query = parse_qs(url.query)
            try:
                if url.path == '/api/sources':
                    self.send_json(200, [dict(id=s['id'], name=s['name'], kind=s.get('kind', 'transcript'),
                                             segment_count=len(s['segments']), page_count=s.get('page_count'),
                                             unindexed_pages=s.get('unindexed_pages', [])) for s in tutor.store.sources.values()])
                elif url.path == '/api/segments':
                    source = query.get('source_id', [''])[0]
                    if source not in tutor.store.sources:
                        raise ValueError('Nguồn không hợp lệ.')
                    self.send_json(200, [dict(id=s['id'], heading=s['heading'], preview=s['text'][:140]) for s in tutor.store.sources[source]['segments']])
                elif url.path == '/api/segment':
                    source = query.get('source_id', [''])[0]
                    segment = tutor.store.segment(source, query.get('id', [''])[0])
                    if 'page_number' in segment:
                        segment = dict(segment, pdf_url='/api/source-file?source_id=' + source + '#page=' + str(segment['page_number']))
                    self.send_json(200, segment)
                elif url.path == '/api/source-file':
                    path = tutor.store.source_file(query.get('source_id', [''])[0])
                    body = path.read_bytes()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/pdf')
                    self.send_header('Content-Disposition', 'inline; filename="' + path.name + '"')
                    self.send_header('Content-Length', str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                else:
                    self.send_json(404, {'error': 'Không có endpoint này.'})
            except ValueError as error:
                self.send_json(400, {'error': str(error)})

        def do_POST(self):
            if not self.local_host():
                return
            if self.path != '/api/ask':
                self.send_json(404, {'error': 'Không có endpoint này.'})
                return
            origin = self.headers.get('Origin')
            if origin and origin not in {f'http://127.0.0.1:{self.server.server_port}', f'http://localhost:{self.server.server_port}'}:
                self.send_json(403, {'error': 'Chỉ nhận yêu cầu từ giao diện local.'})
                return
            if not self.headers.get('Content-Type', '').startswith('application/json'):
                self.send_json(415, {'error': 'Cần Content-Type application/json.'})
                return
            if not tutor:
                self.send_json(503, {'error': source_error})
                return
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if not 0 < size <= 16000:
                    raise ValueError('Request trống hoặc quá lớn.')
                request = json.loads(self.rfile.read(size).decode('utf-8'))
                self.send_json(200, tutor.ask(request))
            except (ValueError, UnicodeDecodeError) as error:
                self.send_json(400, {'error': str(error)})
            except ModelError as error:
                self.send_json(502, {'error': str(error)})
            except OSError:
                self.send_json(500, {'error': 'Không ghi được trace local. Kiểm tra quyền thư mục logs.'})
    return Handler


def main():
    load_env()
    tutor, error = None, ''
    try:
        tutor = Tutor(configured_store(), ModelClient(), ROOT / 'logs')
    except (ValueError, ModelError) as e:
        error = str(e)
    port = int(os.getenv('PORT', '8765'))
    httpd = ThreadingHTTPServer(('127.0.0.1', port), make_handler(tutor, error))
    print(f'VLearn Grounded Tutor: http://127.0.0.1:{port}', flush=True)
    if error:
        print(error, flush=True)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
