"""Summarize complete slide runs; human scores remain pending."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'eval'))
from run import technical_metrics


def main():
    cases = json.loads((ROOT / 'eval/golden_set.json').read_text(encoding='utf-8'))
    expected = [c['case_id'] for c in cases]
    candidates = []
    for folder in (ROOT / 'eval/runs').iterdir():
        path = folder / 'results.json'
        if path.exists():
            rows = json.loads(path.read_text(encoding='utf-8'))
            if [r['case_id'] for r in rows] == expected:
                candidates.append((folder, rows))
    if not candidates:
        raise ValueError('No complete current slide run.')
    run_dir, rows = max(candidates, key=lambda pair: pair[0].name)
    m = technical_metrics(rows)
    total, valid, correct = m['total'], m['schema_valid'], m['action_correct']
    count, validity = m['displayed_citations'], m['displayed_citation_validity']
    lines = ['# Kết quả AI thật của bản slide', '',
             f'Run UTC: {run_dir.name}. Model alias: {rows[0]["model"]}; provider: {rows[0]["provider"]}.', '',
             f'Parser/schema/citation: {valid}/{total}. Action đúng expected: {correct}/{total} ({m["action_accuracy"]}%). API lỗi vẫn tính trong mẫu số.', '',
             f'{count} citation hiển thị; hợp lệ kỹ thuật {validity}%. Đây chưa phải groundedness.', '',
             'Nguồn chính: 2 PDF slide, 58 trang; S01/S02 dùng số trang PDF vật lý. SG01–SG24: 10 thường, 10 khó, 4 hiếm; 12 case có provenance từ chat thật. Retrieval offline lấy đủ supporting pages ở 15/15 câu kỳ vọng answer.', '',
             '## Lỗi giữ nguyên', '']
    failures = [r for r in rows if r['status'] != 'validated' or not r['action_match']]
    lines += [f'- {r["case_id"]}: expected {r["expected"]}; actual {r.get("actual", "error")}; {r.get("error", "action mismatch")}.' for r in failures] or ['Không có lỗi schema/action.']
    lines += ['', 'Pass mọi chiều chưa chốt: nhóm chấm grounding/UX/risk trong review.csv, đối chiếu claim với PDF. Audit Codex không thay người chấm độc lập. Chưa có baseline, video hoặc user validation.', '',
              'Báo cáo: [run_results.md](run_results.md). Output đã rà: [published-runs](published-runs/). Transcript cũ trong archive chỉ là lịch sử.', '']
    (ROOT / 'eval/live_summary.md').write_text('\n'.join(lines), encoding='utf-8')
    path = ROOT / 'slides/content.json'
    slides = json.loads(path.read_text(encoding='utf-8'))
    slides[1]['table'] = [['Bước', 'Vai trò'],
        ['1. Chọn slide Day 1 / Day 2', '2 PDF · 58 trang · số trang vật lý'],
        ['2. Tìm trang liên quan', 'BM25 · tối đa 6 trang / 12.000 ký tự'],
        ['3. Gọi API AI thật', 'AI chọn action và sinh JSON'],
        ['4. Kiểm tra mã → mở PDF', 'Mã S01/S02 mở đúng trang nguồn']]
    slides[1]['note'] = 'Gemini native qua CLIProxyAPI; hỗ trợ OpenAI-compatible. Chỉ dùng chữ trích xuất PDF, chưa OCR hình/sơ đồ.'
    slides[3]['body'] = f'{total} case slide đã gọi AI thật · {rows[0]["model"]}. Golden set: 10 thường + 10 khó + 4 hiếm; 12 case có provenance từ chat thật.'
    slides[3]['table'] = [['Tiêu chí', 'Quality bar / cách hiểu', 'Kết quả hiện tại'],
        ['Case pass mọi chiều', '≥80% (ít nhất 20/24)', 'Chưa chốt: cần chấm nội dung'],
        ['Action đúng expected', 'Kỹ thuật, không là case pass', f'{correct}/{total} ({m["action_accuracy"]}%)'],
        ['Citation hiển thị hợp lệ', '100% thuộc context', f'{count} mã, {validity}% kỹ thuật']]
    slides[3]['note'] = 'Nguồn: eval/run_results.md. API lỗi giữ trong mẫu số. Chưa có biên nhận khóa CP4; action/mã đúng chưa chứng minh claim đúng.'
    slides[4]['body'] = f'Nguồn chính đã đổi sang PDF slide. {valid}/{total} output qua schema. Retrieval offline lấy đủ supporting pages ở 15/15 câu kỳ vọng answer.'
    slides[4]['table'] = [['Đã kiểm tra / chuẩn bị', 'Phần còn thiếu'],
        ['PDF mở đúng trang, chặn mã giả', 'Chấm grounding / UX / risk'],
        ['Trace có prompt/context/action', 'Chấm độc lập ≥5 output; baseline'],
        ['Protocol R6: mở nguồn, sửa câu hỏi', '5 người ngoài nhóm, ≥2 đã khai CP1']]
    slides[4]['note'] = 'Chưa OCR; chữ lỗi font được đánh dấu. Chưa có user feedback/video thật. Transcript cũ chỉ là lịch sử.'
    slides[5]['note'] = 'Tiếp theo: kiểm UI và font/công thức, quay demo, chấm nội dung. Chưa tuyên bố tốt hơn tutor cũ khi chưa có baseline.'
    path.write_text(json.dumps(slides, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Updated slide-primary summary and PDF content for {run_dir.name}.')


if __name__ == '__main__':
    main()
