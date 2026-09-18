# CP3 — tutor trả lời có citation slide

Workflow: chọn PDF/trang → hỏi → answer/clarify/no_grounding/out_of_scope → kiểm citation → mở PDF đúng trang → sửa câu/trang/nguồn rồi gửi lại. Nguồn chính là slide Day 1/Day 2; không dùng transcript thay citation slide.

Code/API thật có ở codebase/, adapter Gemini/OpenAI-compatible. Golden set chính eval/golden_set.json có 24 case SG, 12 case phát triển từ log thật; expected/claims theo slide thiết kế trước chạy. Kết quả hiện hành: eval/run_results.md, live_summary.md. Phiếu chấm/cách chấm: eval/README.md và review_worksheet.md. Quality bar giữ ≥80% full pass, 100% citation hợp lệ, không bịa cá nhân/giả nguồn.

Không nhận số 24/24 transcript lịch sử là kết quả slide. Nhóm đã check nội dung lượt slide: 23/24 pass toàn bộ (95,83%), SG02 timeout tính fail; kết quả đạt quality bar. Timeout/API lỗi vẫn là fail trong mẫu số. Source PDF cần pack gốc, không có trong Git; public results/review/metadata không chứa key/raw provider.

Phần còn để nộp: quay video AI thật ~30 giây, mã đội trưởng/link public/form và biên nhận. UI đã thiết kế lại và kiểm browser desktop/mobile cùng một lượt AI thật, xem docs/ui-verification.md; chưa quay video. Backend/API/UI và hồ sơ có thể bàn giao. Chưa có xác nhận đã nộp CP3.
