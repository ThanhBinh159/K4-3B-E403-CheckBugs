# VLearn Grounded Tutor — trả lời có citation slide

CP3 dùng **slide/PDF làm nguồn chính**. Chọn Day 1/Day 2 → hỏi → AI trả lời/hỏi lại/nêu thiếu nguồn hoặc ngoài phạm vi → mở PDF gốc đúng trang. Transcript không được dùng thay nguồn citation slide.

## Chạy

```powershell
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Điền API key/model riêng và đường dẫn pack, không commit .env.
python -X utf8 codebase/server.py
```

Mở http://127.0.0.1:8765. Thư mục `VLEARN_SLIDES_DIR` cần `d1-slide-hackathon.pdf` và `d2-slide-hackathon.pdf` từ pack đề bài (mỗi file 29 trang). `.env.example` chọn `VLEARN_SOURCE_KIND=slides`; PDF gốc không nằm trong repo. Đọc [hướng dẫn nguồn slide](docs/slide-primary.md).

Gemini trực tiếp: `AI_PROVIDER=gemini`, `AI_BASE_URL=https://generativelanguage.googleapis.com/v1beta`, `GEMINI_API_KEY`, `AI_MODEL` là model khả dụng. OpenAI trực tiếp: `AI_PROVIDER=openai-compatible`, `AI_BASE_URL=https://api.openai.com/v1`, `AI_API_KEY`, `AI_MODEL`. CLIProxyAPI của người dùng dùng Gemini native với Base URL `http://localhost:8317/v1beta`. Key chỉ giữ server local; không đưa key vào frontend/URL/Git.

## Cách hoạt động và giới hạn

pypdf đọc chữ theo trang; BM25 tìm nguồn trong đúng file được chọn. Có thể chọn tối đa 3 trang; context tối đa 6 trang, 3.000 ký tự/trang, 12.000 tổng ký tự. Một AI call quyết định action và tạo JSON; backend kiểm schema, answer ≤180 từ và citation. Không có câu trả lời giả thay lỗi API.

`S01-013` = Day 1, trang vật lý PDF 13; `S02-003` = Day 2, trang PDF 3. Số này có thể khác footer của slide gốc. Bấm citation để xem chữ trích xuất và mở PDF tại `#page=N`. Mã hợp lệ chưa chứng minh claim đúng.

Chưa OCR/vision, không đoán hình/sơ đồ/chữ ảnh. Trang không có chữ không được lập chỉ mục; glyph lỗi có warning, cần đối chiếu bản gốc. Không lấy bài đang mở trên LMS, không trả điểm/deadline/tiến độ cá nhân và chưa có bộ nhớ hội thoại nhiều lượt. UI đã thiết kế đủ 4 bước, kiểm browser desktop/mobile và một lượt AI thật: [báo cáo UI](docs/ui-verification.md). Chưa quay video.

## Đánh giá CP3

`eval/golden_set.json` là **24 case slide SG01–SG24**, gồm 10 thường/10 khó/4 edge, 12 case phát triển từ lượt log thật; không dùng reply cũ làm đáp án chuẩn. Expected/claims được thiết kế theo trang PDF trước chạy. Quality bar vẫn ≥80% full case pass, 100% citation hợp lệ và không bịa dữ liệu cá nhân/giả nguồn.

```powershell
python tools/verify_all.py
python -X utf8 eval/run.py
# Điền review.csv của run rồi xuất báo cáo, không gọi API:
python -X utf8 eval/run.py --report eval/published-runs/<run>
```

[Kết quả hiện hành](eval/run_results.md) · [Tóm tắt](eval/live_summary.md) · [Cách chấm](eval/README.md) · [Worksheet](eval/review_worksheet.md). Full quality chưa chốt khi còn ô nhóm chấm trống. Timeout/API lỗi vẫn trong mẫu số. Codex review không thay người chấm độc lập.

Kết quả transcript trước và golden set cũ nằm ở `eval/archive/`; public run 20260918T044511Z là lịch sử, không được nhận là kết quả bản slide. Smoke slide 10 case cũng không thay golden set slide chính. Không hạ quality bar hoặc bỏ lỗi để làm đẹp số.

## Bàn giao và nhân sự

Nhân sự/đội trưởng/phòng do nhóm điền theo README repo nhóm; không tự tạo willing users hoặc kết quả thử nghiệm. [CP3 còn cần](submission/CP3.md): nhóm chấm nội dung, kiểm UI/video khi tiếp tục, link public/mã đội trưởng/form và biên nhận. [Spec](spec.md) và hồ sơ CP4/CP5 được cập nhật theo nguồn slide, chưa nhận đã đạt/nộp mọi checkpoint.

Raw provider/context/key và PDF nguồn không commit. Public run chỉ có response, phiếu chấm và metadata nguồn an toàn; người chấm cần pack đề bài để đối chiếu. `tools/package_submission.py` tạo ZIP sạch. Bản cũ dùng transcript chỉ còn để tái lập lịch sử, không là nguồn của CP3 hiện hành.
