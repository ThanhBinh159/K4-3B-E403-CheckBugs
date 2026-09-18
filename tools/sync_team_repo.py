"""Copy allowlisted product artifacts while preserving team CP1/CP2 files."""
import shutil
from pathlib import Path
from package_submission import ROOT, allowed


def main():
    target = ROOT.parent / 'CheckBugs-pkien1'
    assert target.resolve().parent == ROOT.parent.resolve() and (target / '.git').is_dir()
    for source in ROOT.rglob('*'):
        if source.is_file() and allowed(source):
            rel = source.relative_to(ROOT)
            dest = target / ('PRODUCT.md' if str(rel) == 'README.md' else rel)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
    path = target / 'README.md'
    original = path.read_text(encoding='utf-8')
    start = original.index('## Bàn giao CP3')
    end = original.index('**SPEC → Prototype → Demo.**', start)
    handoff = '''## Bàn giao CP3 — branch `pkien1`

**Đã làm lại theo slide/PDF làm nguồn chính:** 2 file Day 1/Day 2, 58 trang. Citation S01/S02 mở PDF gốc đúng số trang vật lý. Xem [hướng dẫn chạy](PRODUCT.md), [workflow](codebase/cp2-flow.md), [CP3](submission/CP3.md).

Golden SG01–SG24 đã gọi AI thật: 23/24 output hợp lệ và action đúng (95,83%), 1 timeout SG02 giữ nguyên; 45 test kỹ thuật đạt. **Full quality chưa chốt**, cần nhóm chấm grounding/UX/risk. [Output và phiếu chấm](eval/published-runs/20260918T080807Z/README.md) · [Kết quả](eval/run_results.md) · [Audit sơ bộ](eval/cp3-slide-content-audit.md).

Cài `python -m pip install -r requirements.txt`, copy `.env.example` thành `.env`, điền API riêng và `VLEARN_SLIDES_DIR` đến slides trong pack đề bài. Chạy `python -X utf8 codebase/server.py`. Hỗ trợ Gemini native và OpenAI-compatible; không cần API để chấm output đã có. Key/PDF nguồn/raw traces không nằm trong repo.

Chưa OCR hình/sơ đồ. Người tiếp tục kiểm UI, font/công thức, quay video AI thật theo [kịch bản](submission/video-scripts.md), chấm nội dung và nộp form. PDF demo 6 trang đã cập nhật số kỹ thuật mới; không thay bằng chứng video hoặc người dùng thật. Transcript cũ và smoke 10 case chỉ là lịch sử, không là số đo bản SG24.

README sự kiện và thông tin nhóm bên dưới được giữ lại; `canvas.md`, `cp2-archify.html`, `cp2-flow.svg` là hồ sơ CP1/CP2 đã có.

'''
    path.write_text(original[:start] + handoff + original[end:], encoding='utf-8')
    historic = target / 'eval/published-runs/20260918T044511Z/README.md'
    text = historic.read_text(encoding='utf-8')
    text = text.replace('../../review_worksheet.md', '../../archive/transcript-review-worksheet.md')
    text = text.replace('../../golden_set.json', '../../archive/golden-transcript.json')
    text = text.replace('cập nhật `eval/run_results.md`', 'cập nhật `eval/archive/transcript-run-results.md`')
    if '**Lịch sử transcript' not in text:
        text = text.replace('\n\n', '\n\n**Lịch sử transcript, không phải kết quả CP3 slide hiện hành SG01–SG24.**\n\n', 1)
    historic.write_text(text, encoding='utf-8')
    smoke = target / 'eval/published-runs/20260918T075210Z/README.md'
    text = smoke.read_text(encoding='utf-8').replace('không thay golden set transcript 24 case', 'lịch sử thử nguồn, không thay golden set slide chính SG01–SG24')
    smoke.write_text(text, encoding='utf-8')
    print('Synced allowlisted files; preserved team/event and CP1/CP2 artifacts.')


if __name__ == '__main__':
    main()
