"""Publish reviewed generated answers and allowlisted trace metadata, never pack text."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAMP = '20260918T080807Z'


def main():
    folder = ROOT / 'eval/runs' / STAMP
    rows = json.loads((folder / 'results.json').read_text(encoding='utf-8'))
    assert len(rows) == 24 and all(r['case_id'].startswith('SG') for r in rows)
    public = ROOT / 'eval/published-runs' / STAMP
    public.mkdir(parents=True, exist_ok=True)
    traces = []
    for row in rows:
        trace = json.loads((ROOT / 'logs' / (row['request_id'] + '.json')).read_text(encoding='utf-8'))
        item = {key: trace.get(key) for key in ['request_id', 'timestamp', 'model', 'provider', 'prompt_version',
                'retrieval_version', 'parser_version', 'request', 'context_ids', 'status', 'latency_ms']}
        item['case_id'] = row['case_id']
        item['context_metadata'] = [{**{k: c.get(k) for k in ['id', 'heading', 'page_number', 'extraction_warning',
                'truncated', 'selected_by_user']}, 'text_char_count': len(c['text'])} for c in trace['context']]
        traces.append(item)
    artifacts = {'results.json': (folder / 'results.json').read_bytes(),
                 'review.csv': (folder / 'review.csv').read_bytes(),
                 'trace_metadata.json': json.dumps(traces, ensure_ascii=False, indent=2).encode('utf-8')}
    # Read secrets locally without emitting them; never publish if a credential appears.
    secrets = []
    for line in (ROOT / '.env').read_text(encoding='utf-8').splitlines():
        if '=' in line:
            key, value = line.split('=', 1)
            if any(part in key.upper() for part in ['KEY', 'TOKEN', 'SECRET']) and value.strip():
                secrets.append(value.strip().strip('"\'').encode('utf-8'))
    for name, content in artifacts.items():
        assert not any(secret in content for secret in secrets), 'Credential detected'
        (public / name).write_bytes(content)
    shutil.copyfile(ROOT / 'eval/cp3-slide-content-audit.md', public / 'content-audit.md')
    (public / 'README.md').write_text(
        '# Kết quả CP3 slide-primary\n\n'
        'Run UTC: ' + STAMP + '. 24 case SG; SG02 timeout giữ nguyên. '
        '23/24 output đúng schema/action không thay tỷ lệ pass nội dung.\n\n'
        '- results.json: output AI thật, không sửa đáp án.\n'
        '- review.csv: nhóm điền grounding/UX/risk, reviewer và notes; hiện còn trống.\n'
        '- trace_metadata.json: request/version/ID trang, không có chữ pack hoặc raw provider.\n'
        '- content-audit.md: audit Codex sơ bộ, không thay người chấm độc lập.\n\n'
        'Dùng [golden set](../../golden_set.json), [worksheet](../../review_worksheet.md), '
        '[hướng dẫn chấm](../../README.md). Cần tải pack gốc của BTC: '
        'slides/d1-slide-hackathon.pdf và d2-slide-hackathon.pdf. '
        'S01-013 = Day 1, trang PDF vật lý 13; số footer có thể khác.\n\n'
        'Không có baseline/video/user validation. Kết quả transcript và smoke slide trước là lịch sử riêng.\n',
        encoding='utf-8')
    print('Published 24 generated outputs, blank review sheet and sanitized trace metadata.')


if __name__ == '__main__':
    main()
