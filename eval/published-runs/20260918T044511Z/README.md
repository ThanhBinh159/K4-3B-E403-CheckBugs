# Dữ liệu chấm CP3 — run 20260918T044511Z

- `results.json`: 24 câu trả lời thật, action, citation và metadata; giữ nguyên kết quả lượt chạy, không sửa câu trả lời để chấm đẹp hơn.
- `review.csv`: phiếu chấm trống với grounding/ux/risk, reviewer và notes. Chưa có người chấm nội dung; các ô trống không phải fail.
- `trace_metadata.json`: câu hỏi/đoạn chọn, phiên bản prompt/retrieval, context IDs, heading, độ dài và cờ truncated. Không có API key, raw provider, nội dung nguyên pack hoặc thông tin học viên từ log gốc.

Người chấm không cần API để chấm lượt này. Cần transcript 04/06 từ pack đề bài để mở đúng mã đoạn trong `context_ids` và đối chiếu `citations`. Tất cả context của lượt này có truncated=false, nên nguyên đoạn trong transcript chính là nội dung đoạn AI đã thấy. Metadata không thay cho tài liệu nguồn.

1. Đọc `../../review_worksheet.md` và `../../golden_set.json` để xem expected, required_claims và forbidden_claims.
2. Đọc response trong `results.json`, mở nguồn tương ứng để kiểm chứng mọi ý kiến thức.
3. Điền pass/fail cho grounding, ux, risk trong `review.csv`; ghi reviewer và lý do. Không điền tên/ID người học hoặc thông tin riêng tư vào notes công khai.
4. Nhờ người thứ hai chấm độc lập ít nhất 5 câu; ghi và giải quyết bất đồng theo `../../README.md`.
5. Từ root repo chạy:

```powershell
python -X utf8 eval/run.py --report eval/published-runs/20260918T044511Z
```

Lệnh export không gọi API; cập nhật `eval/run_results.md` theo phiếu chấm. Không đổi expected/quality bar sau khi đọc output. 24/24 action đúng là số kỹ thuật; full pass rate vẫn pending đến khi mọi case được chấm. Dữ liệu này chỉ là một lượt dùng Gemini qua proxy, không phải kết quả của model/provider khác.
