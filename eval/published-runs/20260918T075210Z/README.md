# Smoke run slide — 20260918T075210Z

10 case thử nguồn slide thật, lịch sử thử nguồn, không thay golden set slide chính SG01–SG24. `results.json` giữ nguyên 9 output hợp lệ và 1 timeout SL10 (30 giây); action đúng 9/10, 6 citation hợp lệ kỹ thuật. Phiếu chấm chưa được nhóm điền, full quality còn pending.

Đọc `../../slide_smoke_set.json` để xem expected/required/forbidden claims; dùng PDF Day 1/Day 2 của pack đề bài để mở trang tương ứng. Mã S01/S02-NNN là số trang vật lý PDF, không phải footer slide gốc. `trace_metadata.json` ghi context IDs, số trang, warning và độ dài trích xuất; không public key, raw provider hoặc PDF nguồn. Trang có extraction_warning cần đối chiếu ký tự lỗi với PDF gốc.

Điền grounding/ux/risk, reviewer và notes trong review.csv. Export không gọi API:

```powershell
python -X utf8 eval/run.py --report eval/published-runs/20260918T075210Z
```

Report ghi vào `eval/slide_run_results.md`, không ghi đè báo cáo transcript. Codex thấy SL03 thiếu required claim về dự đoán token; nhóm cần xác nhận/chấm thật. Timeout giữ là fail kỹ thuật trong mẫu số, không loại đi hoặc biến retry thành kết quả lượt đầu.
