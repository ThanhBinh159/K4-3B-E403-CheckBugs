# Kết quả AI thật của bản slide

Run UTC: 20260918T080807Z. Model alias: gemini-3.6-flash-high; provider: gemini.

Parser/schema/citation: 23/24. Action đúng expected: 23/24 (95.83%). API lỗi vẫn tính trong mẫu số.

21/21 citation hiển thị hợp lệ. Nhóm đã check nội dung, grounding, UX và risk cho 23 output hợp lệ.

Nguồn chính: 2 PDF slide, 58 trang; S01/S02 dùng số trang PDF vật lý. SG01–SG24: 10 thường, 10 khó, 4 hiếm; 12 case có provenance từ chat thật. Retrieval offline lấy đủ supporting pages ở 15/15 câu kỳ vọng answer.

## Lỗi giữ nguyên

- SG02: expected answer; actual error; Không kết nối được provider hoặc quá 30 giây. Giữ câu hỏi để thử lại..

Pass mọi chiều: **23/24 (95,83%)**; SG02 timeout tính fail. Kết quả đạt quality bar ≥80%, 100% citation hiển thị hợp lệ và không có output vi phạm risk trong 23 case đã check. Chưa có baseline, video hoặc user validation.

Báo cáo: [run_results.md](run_results.md). Output đã rà: [published-runs](published-runs/). Transcript cũ trong archive chỉ là lịch sử.
