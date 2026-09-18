# CP3 — bản thử dùng slide/PDF làm nguồn

Giữ workflow CP2: chọn nguồn/trang → hỏi → answer/clarify/no_grounding/out_of_scope → kiểm citation → mở PDF gốc đúng trang. Chỉ thay cách nạp nguồn, không dùng câu trả lời giả.

## Chạy

```powershell
python -m pip install -r requirements.txt
```

Trong `.env`, giữ cấu hình API riêng, thêm:

```dotenv
VLEARN_SOURCE_KIND=slides
VLEARN_SLIDES_DIR=../K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/slides
```

Thư mục này cần `d1-slide-hackathon.pdf` và `d2-slide-hackathon.pdf` từ pack đề bài. Không copy PDF nguồn lên Git. Khởi động lại `python -X utf8 codebase/server.py`, mở http://127.0.0.1:8765.

Chọn slide Day 1, hỏi “Token là gì?”. Citation `S01-013` là **trang vật lý 13 của PDF Day 1**, `S02-003` là trang vật lý 3 của PDF Day 2. Số trang này có thể khác số slide in ở footer bản gốc, ví dụ Day 2 trang PDF 3 in “16/83”. Bấm citation để đọc chữ đã trích, rồi “Mở PDF gốc” để xem đúng trang (`#page=N`).

## Cách thực hiện

pypdf đọc chữ từng trang; giữ số trang gốc kể cả có trang không có chữ. Mỗi trang có chữ là một đơn vị retrieval với mã Sxx-NNN. Các giới hạn context/answer, selected_by_user, adapter API và validator được giữ. Citation cả trong answer lẫn danh sách phải thuộc context của đúng nguồn.

Không có OCR/vision: hình, sơ đồ và chữ trong ảnh có thể không được đọc. PDF hoàn toàn không có chữ bị báo lỗi, không tạo nguồn giả. Trang không có chữ bị bỏ khỏi chỉ mục và có danh sách `unindexed_pages`. Ký tự font private-use không giải mã được được thay bằng �, có extraction_warning; AI được yêu cầu không đoán phần lỗi. Nên mở PDF gốc để kiểm chứng, đặc biệt con số/bảng/sơ đồ.

## Kiểm thử

```powershell
python tools/verify_all.py
python -X utf8 eval/run.py --cases eval/slide_smoke_set.json
```

Smoke set slide có 10 case riêng, **không phải golden set 24 case transcript**. Báo cáo mới: `eval/slide_run_results.md`; không ghi đè `eval/run_results.md` của lượt transcript. Chất lượng nội dung vẫn cần người chấm. Không chuyển citation/expected của bộ transcript sang slide bằng cách đoán ánh xạ.

Để trở lại nguồn cũ: đổi `VLEARN_SOURCE_KIND=transcript`, kiểm tra `VLEARN_DATA_DIR`, khởi động lại server. Muốn chạy bộ transcript cũ cũng phải chuyển chế độ trước. Đây là bản thử; chưa chứng minh slide tốt hơn transcript trên cùng tập đánh giá.

## Kết quả bản thử

Run 20260918T075210Z gọi 10 case với Gemini qua proxy: 9/10 output hợp lệ/action đúng (90%), 6 citation hiển thị hợp lệ kỹ thuật. SL10 timeout sau 30 giây vẫn nằm trong mẫu số. 9 case còn pending nhóm chấm; không báo 90% là full pass rate. 43 kiểm thử offline đạt; đã kiểm tra HTTP PDF/citation và xem PDF gốc trang Day 1-13, Day 1-29, Day 2-3, chưa visual QA UI bằng browser.

Codex đối chiếu sơ bộ thấy SL03 trả đúng so sánh phạm vi nhưng thiếu required claim về dự đoán token dù S01-012 đã được gửi; cần nhóm chấm và cải thiện nội dung. SL05 dùng ký hiệu LaTeX có thể cần UI hiển thị tốt hơn. Bản thử đã dùng nguồn slide thật, chưa thay kết quả quality/golden set chính của CP3.

Chẩn đoán SL10: thử lại riêng với cùng câu hỏi đã trả đúng out_of_scope, trace 7662320576f94ca1a9b894e9d1e99f11, 22.694 ms. Retry không ghi đè kết quả 9/10/timeout của lượt đầu.
