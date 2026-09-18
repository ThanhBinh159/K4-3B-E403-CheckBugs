import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'codebase'))
from server import load_env
from provider import ModelClient, ModelError, NoRedirect

load_env()
base = os.getenv('AI_BASE_URL', 'http://localhost:8317/v1').rstrip('/')
headers = {}
provider = os.getenv('AI_PROVIDER', 'gemini')
key = os.getenv('GEMINI_API_KEY', '') if provider == 'gemini' else os.getenv('AI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
if key:
    if provider == 'gemini':
        headers['x-goog-api-key'] = key
    else:
        headers['Authorization'] = 'Bearer ' + key
try:
    ModelClient.validate_base(base)
    with build_opener(NoRedirect()).open(Request(base + '/models', headers=headers), timeout=5) as response:
        data = json.load(response)
    if provider == 'gemini':
        for model in data.get('models', []):
            print(model['name'].removeprefix('models/'))
    else:
        for model in data.get('data', []):
            print(model['id'])
except HTTPError as e:
    code = e.code
    e.close()
    print(f'Proxy HTTP {code}: kiểm tra key và cấu hình; không tự theo redirect.', file=sys.stderr)
    sys.exit(1)
except (URLError, TimeoutError, ModelError):
    print('Không kết nối được proxy. Kiểm tra CLIProxyAPI đang chạy và Base URL.', file=sys.stderr)
    sys.exit(1)
