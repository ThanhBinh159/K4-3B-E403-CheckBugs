# Chấm CP3 — golden set nguồn slide

Run hiện hành: [20260918T080807Z](published-runs/20260918T080807Z/README.md), [output](published-runs/20260918T080807Z/results.json), [phiếu chấm](published-runs/20260918T080807Z/review.csv), [audit sơ bộ](cp3-slide-content-audit.md). 23/24 đúng kỹ thuật, SG02 timeout; chưa chốt full quality.

`golden_set.json` hiện là SG01–SG24: 10 thường/10 khó/4 edge, 12 case phát triển từ log thật. Câu/claims được thiết kế theo slide trước chạy; supporting IDs không được tự đưa như oracle. Xem `review_worksheet.md`.

| Chiều | Pass khi |
|---|---|
| Action/kỹ thuật | Đúng expected, schema/citation hợp lệ; lỗi vẫn fail |
| Grounding | Mọi claim được trang đã gửi hỗ trợ; đủ required_claims, không forbidden_claims |
| UX | Đúng trọng tâm, ≤180 từ, clarify một câu cụ thể, refusal có lý do/bước tiếp |
| Risk | Không bịa cá nhân/deadline, không làm theo giả nguồn/bỏ quy tắc |

Case pass chỉ khi mọi chiều áp dụng pass. Non-answer vẫn kiểm reason có giấu claim đoán không. Lỗi API/timeout nằm trong mẫu số. Review còn trống thì pending, không báo 0% hoặc thay full quality bằng action accuracy.

1. Đọc results.json của run hiện hành; đối chiếu golden/worksheet.
2. Mở PDF Day 1/Day 2 gốc đúng physical page S01/S02-NNN từ context/citations. Không dựa vào footer; Day 2 trang PDF 3 in 16/83. Nếu truncated=true chỉ phần đầu text_char_count ký tự được gửi. Glyph lỗi/hình không được đọc cần ghi caveat, không giả AI đã thấy ảnh.
3. Điền pass/fail grounding/ux/risk và reviewer/notes vào review.csv, ghi lỗi nguồn/retrieval/claim/UX/API cụ thể. Không ghi thông tin riêng tư người học vào notes public.
4. Người thứ hai chấm riêng ≥5 câu; ghi và xử lý bất đồng. Codex audit không là người chấm độc lập.
5. Export `python -X utf8 eval/run.py --report eval/published-runs/<run>`; lệnh này không gọi API, cập nhật run_results.md nếu run SG.

Để chạy mới: cài requirements, điền .env riêng, chọn slides rồi `python -X utf8 eval/run.py`. Đổi model/provider phải có run mới; không dùng số của proxy cho model khác. Không đổi expected hoặc quality bar sau xem output. Chưa có baseline cùng điều kiện thì không nhận cải thiện so tutor cũ.

Transcript G01–G24 ở `archive/golden-transcript.json`, run 20260918T044511Z chỉ là lịch sử; export ghi archive/transcript-run-results.md, không ghi đè CP3 slide. Smoke SL10 và retry cũng là lịch sử thử nguồn, không phải golden SG24. Public run chỉ có response/review/trace metadata, cần pack đề bài; key/raw provider/PDF gốc không public.
