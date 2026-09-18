# CP2 - Luồng tương tác

[Mock HTML](cp2-mock.html) · [Sơ đồ SVG](cp2-flow.svg) · [Mã Mermaid](cp2-flow.mmd).

Chọn bài → nhập câu hỏi → kiểm tra input → AI quyết định đủ rõ/đủ nguồn → answer có citation hoặc clarify/no_grounding/out_of_scope → mở nguồn hoặc sửa input. JSON/citation/API lỗi là lỗi kỹ thuật riêng, giữ input để thử lại.

Mock CP2 dùng nguồn/phản hồi giả minh họa và không gọi AI. CP3 dùng provider API thật, không có câu trả lời hardcode thay API lỗi. Run 20260918T044511Z đã xác minh đủ 24 case thật; output/action hợp lệ 24/24, full pass rate còn chờ nhóm chấm.

## Đối chiếu CP3

Backend giữ các hành vi trong flow: kiểm input, answer/clarify/no_grounding/out_of_scope, kiểm citation và mở đúng đoạn nguồn. Các sửa lỗi G20/G22/G24 không đổi workflow.

Thứ tự nội bộ được gộp: validate input → retrieve → một AI call quyết định action và tạo nội dung → validate output/citation. Sơ đồ CP2 vẽ kiểm rõ/phạm vi trước retrieve để diễn tả tương tác; CP3 cần context truy xuất để AI đánh giá đủ rõ/đủ nguồn. Không phải nhiều AI call riêng cho từng diamond.

Phạm vi nguồn MVP là transcript 04/06 có mã đoạn, chưa đọc slide/PDF hoặc tự lấy bài đang mở trên VLearn. clarify được tiếp tục bằng sửa câu hỏi/chọn đoạn rồi gửi lại; chưa có bộ nhớ hội thoại nhiều lượt. UI đã có nhưng chưa visual QA/end-to-end bằng browser. Do đó đã khớp hành vi backend, chưa xác minh toàn bộ luồng tương tác trực tiếp.
