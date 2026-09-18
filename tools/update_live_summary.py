"""Update public technical summary and editable slides; never expose raw output."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'eval'))
from run import technical_metrics


def main():
    run_dir = max((ROOT / 'eval' / 'runs').iterdir(), key=lambda p:p.name)
    rows = json.loads((run_dir / 'results.json').read_text(encoding='utf-8'))
    expected = len(json.loads((ROOT / 'eval' / 'golden_set.json').read_text(encoding='utf-8')))
    if len(rows) != expected:
        raise ValueError('Lượt chạy chưa đủ case, không cập nhật slide như đã hoàn tất.')
    metrics = technical_metrics(rows)
    total = metrics['total']
    model = rows[0]['model']
    citations = metrics['displayed_citations']
    validity = str(metrics['displayed_citation_validity']) + '%' if citations else 'N/A'
    lines = ['# Tóm tắt số đo AI thật - kỹ thuật', '',
             'Run ID (UTC): ' + run_dir.name, 'Model alias gửi: ' + model + '. Giao thức: Gemini native qua CLIProxyAPI.', '',
             f"Đã chạy {total} case thật. Output qua parser/schema/citation: {metrics['schema_valid']}/{total}. Action đúng expected: {metrics['action_correct']}/{total} ({metrics['action_accuracy']}%).", '',
             f'Citation hiển thị: {citations}; hợp lệ kỹ thuật {validity}. Không coi citation tồn tại là groundedness.', '',
             'Tỷ lệ case pass tất cả chiều: chưa chốt. Grounding/UX/risk cần nhóm chấm review.csv và ít nhất 5 output chấm độc lập nếu thực hiện được. Chưa có video/user validation hoặc baseline.', '',
             '## Lỗi/nhánh cần xem lại', '']
    failures = [r for r in rows if r['status'] != 'validated' or not r['action_match']]
    for r in failures:
        lines.append(f"- {r['case_id']}: expected {r['expected']}, actual {r.get('actual','error')}; {r.get('error','action mismatch')}.")
    if not failures:
        lines.append('Không có lỗi schema/action trong bộ này. Đây không chứng minh mọi claim đúng; nhóm vẫn cần đọc tất cả output theo context. Ưu tiên G06 (retrieval) và G19 (xác suất/tính đúng).')
    lines += ['', 'Raw trace/output ở logs/ và eval/runs/ local, không đưa lên repo. Report từng case: eval/run_results.md.', '']
    (ROOT / 'eval' / 'live_summary.md').write_text('\n'.join(lines), encoding='utf-8')
    path = ROOT / 'slides' / 'content.json'
    slides = json.loads(path.read_text(encoding='utf-8'))
    slides[1]['note'] = 'Gemini native /v1beta đã trả answer thật qua CLIProxyAPI. Không tích hợp LMS, không chấm điểm hoặc tra web.'
    slides[3]['body'] = f'{total} case đã gọi AI thật · {model}. Golden set: 10 thường + 10 khó + 4 hiếm; 12 case phát triển từ lượt chat thật.'
    slides[3]['table'] = [
        ['Tiêu chí','Quality bar / cách hiểu','Kết quả hiện tại'],
        ['Case pass mọi chiều','≥80% (ít nhất 20/24)','Chưa chốt: cần chấm nội dung'],
        ['Action đúng expected','Số kỹ thuật, không là case pass',f"{metrics['action_correct']}/{total} ({metrics['action_accuracy']}%)"],
        ['Citation hiển thị hợp lệ','100% thuộc context',f'{citations} citation, {validity} kỹ thuật']
    ]
    slides[3]['note'] = 'Nguồn: eval/run_results.md. Bar còn yêu cầu 0 output bịa logistics/giả nguồn; risk chưa chấm. Chưa có biên nhận khóa CP4. Action/citation đúng chưa chứng minh groundedness.'
    slides[4]['body'] = 'Proxy đã gọi model thật. Lượt smoke đầu gặp JSON bọc Markdown; đã sửa parser và giữ validator. Retrieval local có supporting ID ở 14/15 câu answer.'
    slides[4]['table'] = [
        ['Đã kiểm tra / chuẩn bị','Phần còn thiếu'],
        ['Parser nhận đúng một JSON block','Chấm grounding / UX / risk'],
        [f"{metrics['schema_valid']}/{total} output qua schema; trace local",'Chấm độc lập ≥5 output; baseline'],
        ['Protocol R6: mở nguồn, sửa câu hỏi','5 người ngoài nhóm, ≥2 đã khai CP1']
    ]
    slides[4]['note'] = 'Nguồn: eval/live_smoke.md, run_results.md, retrieval_diagnostics.md. Chưa có quote/thay đổi từ user feedback hoặc video thao tác thật.'
    slides[5]['body'] = 'Ưu tiên: nhóm chấm nội dung → cập nhật tỷ lệ đầy đủ → quay video CP3/CP5 → điền nhân sự và nộp đúng hạn. Giữ nguyên quality bar.'
    path.write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Updated eval/live_summary.md and slides/content.json with technical metrics only.')


if __name__ == '__main__':
    main()
