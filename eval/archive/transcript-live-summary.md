# AI thật sau cải thiện backend CP3

Run UTC 20260918T044511Z. Model alias gemini-3.6-flash-high, Gemini native qua CLIProxyAPI. Không xác nhận backend thực phía sau alias.

- Output hợp lệ: 24/24; action đúng expected: 24/24 (100%). Run cũ 20260918T035621Z: 21/24 (87,5%); G20/G22/G24 đã đúng ở lượt mới.
- Citation hiển thị: 35, hợp lệ kỹ thuật 100%; chưa chứng minh mọi claim đúng.
- Answer dài nhất 159 từ; latency 3.439–19.006 ms/câu.
- Mọi trace đúng prompt grounded-selected-concise-v3/retrieval bm25-concept-continuation-v3; không vượt 6 đoạn, 3.000 ký tự/đoạn, 12.000 tổng ký tự.
- Offline: 36 test đạt. Retrieval có supporting ID ở 15/15 case expected answer, trước sửa 14/15; không phải grounded answer rate.

Full pass rate chưa chốt: 24 case pending nhóm chấm grounding/UX/risk, không phải 0% pass. Codex đối chiếu nội dung sơ bộ tại cp3-content-audit.md; không giả là người học/người chấm độc lập.

Giữ nguyên golden set/quality bar; các lượt dở không dùng làm kết quả cuối. So sánh cùng bộ câu hỏi chỉ là hồi quy, chưa là baseline tutor cũ, tập mới hoặc ước lượng thống kê. Chưa có UI visual QA/video/user validation/biên nhận nộp.

Report từng case: run_results.md; thay đổi: ../docs/cp3-backend-improvements.md. Raw traces/review.csv giữ trong logs/ và eval/runs/ local, ngoài ZIP/Git. PDF vẫn là snapshot run trước, cần cập nhật trước CP5.
