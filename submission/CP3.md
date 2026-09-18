# CP3 — tutor trả lời có citation slide

Workflow: chọn PDF/trang → hỏi → answer/clarify/no_grounding/out_of_scope → kiểm citation → mở PDF đúng trang → sửa câu/trang/nguồn rồi gửi lại. Nguồn chính là slide Day 1/Day 2; không dùng transcript thay citation slide.

Code/API thật có ở codebase/, adapter Gemini/OpenAI-compatible. Golden set chính eval/golden_set.json có 24 case SG, 12 case phát triển từ log thật; expected/claims theo slide thiết kế trước chạy. Kết quả hiện hành: eval/run_results.md, live_summary.md. Phiếu chấm/cách chấm: eval/README.md và review_worksheet.md. Quality bar giữ ≥80% full pass, 100% citation hợp lệ, không bịa cá nhân/giả nguồn.

Không nhận số 24/24 transcript lịch sử là kết quả slide. Action/schema/citation kỹ thuật không thay full quality; cần nhóm chấm grounding/UX/risk. Timeout/API lỗi vẫn là fail trong mẫu số. Source PDF cần pack gốc, không có trong Git; public results/review/metadata không chứa key/raw provider.

Phần còn để nộp: nhóm chấm nội dung và chốt tổng/pass/fail/%, kiểm UI/browser và quay video AI thật ~30 giây khi tiếp tục, mã đội trưởng/link public/form và biên nhận. UI/video hoãn theo yêu cầu trước; backend/API và hồ sơ có thể bàn giao. Chưa có xác nhận đã nộp CP3.
