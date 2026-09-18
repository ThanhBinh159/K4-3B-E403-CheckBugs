# CP2 → CP3 — hỏi bài có citation slide

Chọn bộ slide và có thể chọn trang → nhập câu hỏi → validate input → truy xuất trang đúng nguồn → AI quyết định đủ rõ/đủ nguồn → answer có citation hoặc clarify/no_grounding/out_of_scope → kiểm citation → mở PDF gốc đúng trang hoặc sửa input/gửi lại.

CP2 mock minh họa, không gọi AI. CP3 gọi provider thật; JSON/API/citation lỗi là lỗi kỹ thuật, giữ input, không dùng câu trả lời hardcode. Backend gộp các quyết định của sơ đồ CP2 trong một AI call sau retrieval, để model có nguồn đánh giá rõ/đủ căn cứ.

Nguồn chính d1/d2-slide-hackathon.pdf, S01/S02-NNN là physical page. Không thay bằng citation transcript. Có thể sửa câu/trang rồi hỏi lại, chưa có bộ nhớ hội thoại nhiều lượt, chưa tích hợp trực tiếp LMS. UI hiện có nhưng chưa visual QA/video; HTTP/API tests không thay kiểm luồng trên browser.
