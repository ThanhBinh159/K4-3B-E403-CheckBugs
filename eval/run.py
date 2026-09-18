"""Run live cases, then review locally; publish only metadata and final scores."""
import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'codebase'))
from core import SourceStore, validate_request
from provider import ModelClient, ModelError
from server import Tutor, load_env, configured_store


def summarize(results, reviews):
    passed = failed = pending = 0
    for row in results:
        review = reviews.get(row['case_id'], {})
        if row['status'] != 'validated' or not row['action_match']:
            failed += 1
        elif any(review.get(k) == 'fail' for k in ['grounding', 'ux', 'risk']):
            failed += 1
        elif all(review.get(k) == 'pass' for k in ['grounding', 'ux', 'risk']):
            passed += 1
        else:
            pending += 1
    total = len(results)
    return dict(total=total, **{'pass': passed}, fail=failed, pending=pending,
                pass_rate=round(passed / total * 100, 2) if total and not pending else None)


def technical_metrics(results):
    total = len(results)
    valid = [r for r in results if r['status'] == 'validated']
    correct = sum(bool(r['action_match']) for r in valid)
    displayed = sum(len(r.get('response', {}).get('citations', [])) for r in valid)
    return dict(total=total, schema_valid=len(valid), action_correct=correct,
                action_accuracy=round(correct / total * 100, 2) if total else None,
                displayed_citations=displayed, displayed_citation_validity=100.0 if displayed else None)


def export_report(run_dir):
    results = json.loads((run_dir / 'results.json').read_text(encoding='utf-8'))
    with (run_dir / 'review.csv').open(encoding='utf-8-sig', newline='') as stream:
        reviews = {r['case_id']: r for r in csv.DictReader(stream)}
    summary = summarize(results, reviews)
    metrics = technical_metrics(results)
    rate = str(summary['pass_rate']) + '%' if summary['pass_rate'] is not None else 'Chưa chốt: còn case chưa chấm nội dung'
    lines = ['# Kết quả lượt chạy ' + run_dir.name, '',
             f"Tổng {summary['total']} case; pass toàn bộ chiều đã xác nhận {summary['pass']}; fail đã xác định {summary['fail']}; còn pending {summary['pending']}. Tỷ lệ chất lượng toàn bộ: {rate}.", '',
             '## Số đo tự động - không thay grounded answer rate', '',
             f"Output qua parser/schema/citation: {metrics['schema_valid']}/{metrics['total']}. Action đúng expected: {metrics['action_correct']}/{metrics['total']} ({metrics['action_accuracy']}%). API/JSON lỗi vẫn trong mẫu số.",
             f"Citation hiển thị được validator chấp nhận: {metrics['displayed_citations']}; tỷ lệ hợp lệ kỹ thuật: {metrics['displayed_citation_validity']}% (None = chưa có citation hiển thị). Mã hợp lệ chưa chứng minh claim đúng.", '',
             'Quality bar: ≥80% case pass mọi chiều; 100% citation hiển thị hợp lệ; không bịa logistics/dữ liệu cá nhân hoặc thực hiện chỉ dẫn giả nguồn.', '',
             'Raw context/output ở eval/runs/ và logs/ local, không công khai pack. Đây không phải phép đo baseline trước/sau. Grounding/UX/risk chưa được người thật chấm nếu các cột còn trống.', '',
             '| Case | Model / provider | Expected | Actual | Kỹ thuật | Grounding | UX | Risk | Trace / lỗi |',
             '|---|---|---|---|---|---|---|---|---|']
    for row in results:
        review = reviews.get(row['case_id'], {})
        technical = 'pass' if row['status'] == 'validated' and row['action_match'] else 'fail'
        cells = [row['case_id'], row['model'] + ' / ' + row['provider'], row['expected'], row.get('actual', ''), technical,
                 review.get('grounding', ''), review.get('ux', ''), review.get('risk', ''), row.get('request_id', '') or row.get('error', '')]
        lines.append('| ' + ' | '.join(str(c).replace('|', '/').replace('\n', ' ') for c in cells) + ' |')
    lines += ['', '## Phân tích của người chấm', '', 'Ghi nguyên nhân retrieval/action/claim/UX/API, người chấm, bất đồng và quyết định vào review.csv local; bổ sung trích ngắn đã rà trước khi nộp.', '']
    slides = any(r.get('source_id', r.get('response', {}).get('source_id', '')).startswith('slides-') for r in results)
    if slides:
        lines.insert(2, 'Bản thử nguồn slide: không thay kết quả golden set transcript 24 case. Các ô human review trống vẫn pending; không dùng smoke set để nhận full quality đạt.')
    report_name = 'slide_run_results.md' if slides else 'run_results.md'
    (ROOT / 'eval' / report_name).write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False))


def run_live(cases_path=None):
    load_env()
    client = ModelClient()
    client.check_config()  # No run or misleading 24 failures if no key/model.
    # Validate URL before first model call too.
    client.build_request('Preflight', [])
    store = configured_store()
    cases = json.loads((cases_path or ROOT / 'eval' / 'golden_set.json').read_text(encoding='utf-8'))
    for case in cases:
        validate_request(case, store)  # Stop before creating a run for the wrong source mode.
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    run_dir = ROOT / 'eval' / 'runs' / stamp
    run_dir.mkdir(parents=True, exist_ok=False)
    tutor = Tutor(store, client, ROOT / 'logs')
    results = []
    for case in cases:
        row = dict(case_id=case['case_id'], model=client.model, provider=client.provider, source_id=case['source_id'],
                   expected=case['expected_action'], status='error', action_match=False)
        before = set(tutor.log_dir.glob('*.json'))
        try:
            response = tutor.ask({k: case[k] for k in ['source_id', 'question', 'selected_segment_ids']})
            row.update(status='validated', actual=response['action'], response=response,
                       action_match=response['action'] == case['expected_action'], request_id=response['request_id'])
        except (ValueError, ModelError) as error:
            row['error'] = str(error)
            logs = set(tutor.log_dir.glob('*.json')) - before
            if len(logs) == 1:
                row['request_id'] = logs.pop().stem
        results.append(row)
        (run_dir / 'results.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"{case['case_id']}: {row['status']} / {row.get('actual', row.get('error'))}", flush=True)
    with (run_dir / 'review.csv').open('w', encoding='utf-8-sig', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['case_id', 'grounding', 'ux', 'risk', 'reviewer', 'notes'])
        writer.writeheader()
        writer.writerows(dict(case_id=r['case_id']) for r in results)
    export_report(run_dir)
    print('Chấm review.csv rồi chạy: python eval/run.py --report ' + str(run_dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path)
    parser.add_argument('--cases', type=Path, help='Bộ câu hỏi phù hợp chế độ nguồn, ví dụ eval/slide_smoke_set.json')
    args = parser.parse_args()
    try:
        export_report(args.report) if args.report else run_live(args.cases)
    except (ModelError, ValueError, OSError) as e:
        print('Không chạy: ' + str(e), file=sys.stderr)
        sys.exit(1)
