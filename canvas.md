| # | Dòng | Nội dung |
|---|---|---|
| 1 | Track + đề | A · VLearn Tutor - trả lời có căn cứ từ tài liệu. |
| 2 | Job executor | Học viên dùng VLearn Tutor để hỏi nhanh về nội dung bài học và kiểm tra lại câu trả lời theo tài liệu gốc. |
| 3 | Pain một câu | Khi học viên hỏi ngắn hoặc mơ hồ, tutor thường trả lời mà thiếu căn cứ kiểm chứng, khiến học viên khó đối chiếu với tài liệu và có nguy cơ hiểu sai. |
| 4 | 1–2 bằng chứng đầu | Trong 3,427 câu hỏi ngắn (q_len ≤ 81), có 1,560 câu trả lời thiếu citation (45.5%), cao hơn mức 28.0% trên toàn bộ 13,494 lượt. Trong các lượt có rating, phản hồi không citation bị downvote 56/90 lượt (62.2%), so với 29/87 lượt (33.3%) khi có citation. |
| 5 | Lát cắt MỘT CÂU | "Giải thích khái niệm này?" - một câu hỏi ngắn nhưng tutor trả lời không kèm phần tài liệu/slide để học viên tự kiểm chứng. |
| 6 | AI tự làm đến đâu | Phát hiện câu hỏi ngắn/mơ hồ, truy xuất đúng đoạn slide/tài liệu liên quan, tạo câu trả lời ngắn gọn kèm citation có thể mở được; nêu rõ khi không đủ căn cứ. |
| 7 | Phân công có tên | - Phân tích dữ liệu: kiểm tra ngưỡng q_len và tỷ lệ citation; - Product: định nghĩa luồng hỏi ngắn và tiêu chí thành công; - Engineering/AI: retrieval, tạo citation và đánh giá groundedness. |
