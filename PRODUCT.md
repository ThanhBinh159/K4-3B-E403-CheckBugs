# VLearn Grounded Tutor · Batch 04 · Lớp 3B

Prototype độc lập cho Track A1: học viên hỏi một khái niệm, AI trả lời dựa trên transcript đã chọn và citation mở được, hoặc hỏi lại/nêu giới hạn.

**Trạng thái:** backend CP3 cải thiện đã chạy Gemini native thật qua CLIProxyAPI. Run 20260918T044511Z: 24/24 output hợp lệ, 24/24 action đúng expected, 35 citation hợp lệ kỹ thuật; 36 test offline đạt. Grounding/UX/risk cần nhóm chấm, chưa chốt full pass rate. Đối chiếu sơ bộ Codex: eval/cp3-content-audit.md; thay đổi: docs/cp3-backend-improvements.md. Video/user validation chưa có; chưa nhận đã đạt/nộp CP3-CP5. PDF là snapshot lượt trước, cần cập nhật trước nộp CP5.

## Nhân sự - người dùng sẽ điền sau

Lớp **3B** · Phòng **[điền E402/E403]** · Nhóm **[điền]** · Đội trưởng **[điền tên + mã]**.

| Họ tên | Mã học viên | Vai trò | Phần việc |
|---|---|---|---|
| [điền] | [điền] | Product / evidence | Mining, Canvas, impact, spec |
| [điền] | [điền] | Engineering / AI | Retrieval, API, UI, trace |
| [điền] | [điền] | Eval / demo | Chấm golden set, user test, video, slide |

## Chạy local

Yêu cầu Python 3.10+; prototype không cần pip install. Data pack để ngoài repo công khai.

```powershell
cd C:\Users\ADMIN\AI20K\MINIHACKATHON\VLearn-GroundedTutor-Submission
# .env local đã được chuẩn bị; nếu clone mới:
# Copy-Item .env.example .env
notepad .env
python -X utf8 codebase/server.py
```

Mở http://127.0.0.1:8765. Cấu hình CLIProxyAPI dùng:

```dotenv
AI_PROVIDER=gemini
AI_BASE_URL=http://localhost:8317/v1beta
AI_MODEL=<tên model thực có trong proxy>
GEMINI_API_KEY=<key do bạn cấu hình cho proxy>
```

Hiện cấu hình **Gemini native**: `AI_BASE_URL` có `/v1beta`; ứng dụng nối `/models/{model}:generateContent` và gửi `GEMINI_API_KEY` trong header `x-goog-api-key`. Đã probe URL không có version trước: `/models` trả 404, `/v1beta/models` trả 401 khi thiếu key. Sau khi người dùng lưu key, danh sách model và một lượt sinh answer đã xác minh được. Không điền key vào URL hoặc frontend. Phải chạy CLIProxyAPI, đăng nhập provider và có model khả dụng trước. Đọc model bằng `python -X utf8 tools/check_proxy.py`; script dùng key trong .env nhưng không in key. Nếu proxy yêu cầu key, điền key đúng; ứng dụng không thử đoán key. Tên model lưu đúng alias đã cấu hình; không khẳng định backend/phiên bản thực phía sau alias khi proxy không cung cấp thông tin.

Nếu chuyển sang OpenAI-compatible: `AI_PROVIDER=openai-compatible`, `AI_BASE_URL=http://localhost:8317/v1`, `AI_API_KEY=...`, `AI_MODEL=...`; ứng dụng nối `/chat/completions`. Gemini trực tiếp dùng `AI_PROVIDER=gemini`, `AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta`, `GEMINI_API_KEY=...`, `AI_MODEL=...`.

Nguồn MVP: `transcript-04-clean.md` và `transcript-06-clean.md`. `VLEARN_DATA_DIR` trong .env trỏ đến thư mục transcript. Không upload/copy pack vào GitHub.

## Kiểm thử và số đo

```powershell
python -X utf8 -m unittest discover -s codebase/tests -v
python -X utf8 -m unittest discover -s eval -p test_eval.py -v
# Chỉ chạy sau khi proxy/key/model sẵn sàng:
python -X utf8 eval/run.py
# Điền pass/fail cho grounding, ux, risk trong eval/runs/<run>/review.csv:
python -X utf8 eval/run.py --report eval/runs/<run>
```

Golden set có 10 thường + 10 khó + 4 hiếm; 12 case phát triển từ turn_id thật. Test kỹ thuật dùng fake provider **chỉ trong codebase/tests/**; UI và eval không có chế độ giả AI. Citation kỹ thuật kiểm tự động, grounding/UX/risk cần người chấm. Tỷ lệ pass toàn bộ không công bố khi còn case chưa chấm. Timeout và API lỗi nằm trong mẫu số khi lượt chạy đã bắt đầu.

Raw prompt/context/response lưu trong `logs/` và `eval/runs/`, bị Git ignore. Chỉ `eval/run_results.md` chứa metadata và điểm đã chấm được đưa lên repo.

## Hồ sơ bàn giao

- [spec.md](spec.md): CP4, quality bar và phần tự khai chưa hoàn thành.
- [submission/README.md](submission/README.md): checklist CP1-CP5 và nội dung form.
- [submission/video-scripts.md](submission/video-scripts.md): CP3 30 giây và CP5 demo dự phòng.
- [validation/user_testing_log.md](validation/user_testing_log.md): mẫu nhật ký R6, chưa có người thử thật.
- `demo-slides.pdf`: slide 6 trang; `slides/content.json` và `tools/build_slides.py` là nguồn chỉnh sửa/tạo lại.
- `tools/package_submission.py`: tạo ZIP sạch để copy vào repo mới; không chứa .env, data, raw logs hoặc cache.

Tạo repo mới theo tên `K4-3B-<phòng>-<tên nhóm>`, công khai. Chưa tạo repo GitHub hoặc nộp form. Năm form dùng cùng mã học viên đội trưởng. Deadline từng CP vẫn áp dụng dù sản phẩm được làm đến CP5 trước.

Để sửa slide: chỉnh slides/content.json; nếu máy chưa có thư viện tạo PDF, chạy `python -m pip install reportlab pymupdf`, rồi `python -X utf8 tools/build_slides.py`. Giữ đúng 6 trang, kiểm tra hình render trong tmp/slide-review/. Backend không cần các thư viện này.

## Tài liệu API đã đối chiếu

[CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI), [Chat Completions](https://developers.openai.com/api/reference/resources/chat), [Gemini generateContent](https://ai.google.dev/api/generate-content).
