# CP3 làm lại theo slide

Slide là nguồn kiến thức/citation chính. Log hỏi đáp sinh viên chỉ dùng tìm pain và xây case; không dùng reply cũ làm đáp án chuẩn. Không dùng transcript thay căn cứ của slide. Bản cũ và số đo cũ đã tách lịch sử ở eval/archive.

## Nguồn và cách chạy

Cài requirements, copy .env.example thành .env, tự điền API key/model và VLEARN_SLIDES_DIR đến thư mục slides của pack. Hai file d1-slide-hackathon.pdf/d2-slide-hackathon.pdf có 29 trang mỗi bộ; không nằm trong Git. VLEARN_SOURCE_KIND=slides là chế độ chính/default. Chạy `python -X utf8 codebase/server.py`, mở http://127.0.0.1:8765.

Source IDs slides-d1/slides-d2, page IDs S01/S02-NNN. Số NNN là trang vật lý PDF, không là số in footer. Chọn Day 1 hỏi token, citation S01-013 mở PDF trang 13. Day 2 S02-003 mở PDF trang 3 dù footer in 16/83. Có thể chọn tối đa 3 trang.

## Xử lý

validate → BM25 trong đúng file → AI dùng context/selected_by_user để quyết định 4 action và tạo JSON → validator → hiện citation/mở PDF gốc. Prompt yêu cầu trả đủ mọi vế câu hỏi từ trang phù hợp, không đoán nghĩa chữ/font lỗi hoặc hình chưa đọc được. Giới hạn 6 trang/12.000 ký tự context, 3.000/trang, answer 180 từ giữ nguyên.

PDF không có chữ báo lỗi; trang trống không chỉ mục và không đánh lại page IDs. Glyph lỗi là �/extraction_warning; mô hình chỉ đọc chữ, chưa OCR/vision. Link `/api/source-file?source_id=slides-d1#page=13` chỉ phục vụ file nguồn allowlist, không nhận đường dẫn tùy ý. Key chỉ giữ backend.

## Đánh giá và bàn giao

Golden chính SG01–SG24 = 10 thường/10 khó/4 edge, 12 case phát triển từ log thật, thiết kế claims theo trang trước chạy. `python -X utf8 eval/run.py` chạy bộ này, report chính eval/run_results.md. Người chấm đọc published results + worksheet + PDF gốc, điền review.csv rồi export không gọi API. Full pass cần grounding/UX/risk, không chỉ schema/action/citation. Quality bar ≥80%, citation 100%, không bịa cá nhân/giả nguồn giữ nguyên.

G01–G24 transcript và SL01–SL10 smoke là lịch sử, không được nhận là số của SG24. Export lịch sử có file riêng để không ghi đè kết quả chính. Chưa có baseline/user feedback hay người thứ hai chấm, không tự nhận đã đạt quality hoặc nộp CP3.

Backend/API/nguồn được kiểm; UI browser QA, video thật và form/receipts do nhóm tiếp tục theo submission/CP3.md. UI hiện có chỉ bổ sung chữ/links để khớp nguồn slide, chưa là thiết kế giao diện hoàn chỉnh.
