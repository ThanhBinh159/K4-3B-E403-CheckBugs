# Cải thiện backend CP3 — 18/09/2026

**Lịch sử bản transcript G01–G24.** CP3 hiện hành đã làm lại theo slide: xem [slide-primary.md](slide-primary.md) và bộ SG01–SG24. Số đo/ID T04 bên dưới không phải kết quả bản slide.

Phạm vi người dùng yêu cầu: cải thiện kỹ thuật, truy xuất, quyết định action và kiểm tra nội dung; chưa cần kiểm tra UI hoặc quay demo. Không đổi expected_action, required_claims hoặc quality bar để làm đẹp số đo.

## Nguyên nhân và thay đổi

- **G20 — thiếu nguồn cho một vế so sánh:** BM25 cũ xếp hạng toàn câu nên đoạn có nhiều từ Machine Learning lấn át cơ chế LLM. Bản mới nối acronym với tên đầy đủ (LLM/ML/DL/AI), dùng heading trong chỉ mục và dành seed cho từng khái niệm được nêu. Transcript thường nối giải thích ở đoạn tiếp theo nên bổ sung continuation trong cùng nguồn. Không tạo thêm kiến thức ngoài transcript.
- **G06 — trả lời định nghĩa LLM thiếu cơ chế dự đoán:** kiểm thử trên pack thật yêu cầu context có T04-047 hoặc T04-091. Đã bổ sung truy xuất continuation thay vì chỉ lấy đoạn nhắc tên LLM.
- **G09 — hồi quy trong lúc sửa:** một bản thử lấy đoạn API ngắn và đoạn tổng kết thay cho đoạn khái niệm LLM. Đã thêm kiểm thử yêu cầu anchor T04-046 cho câu so sánh; truy xuất ưu tiên heading có tên đầy đủ của khái niệm. Điều này cung cấp thêm nguồn liên kết LLM với sản phẩm tạo sinh, không ép action thành answer.
- **G24 — hỏi lại dù đã chọn nguồn:** context mới có selected_by_user; prompt dùng đoạn người học chọn để giải quyết câu “khái niệm này”. Nếu đoạn được chọn vẫn thực sự có nhiều chủ đề thì vẫn hỏi rõ.
- **G22 — context có nhiều chủ đề:** prompt phân biệt yêu cầu định nghĩa cụ thể với thuật ngữ đứng riêng có nhiều nghĩa/chủ đề. Không dùng độ dài câu để quyết định mơ hồ. Giữ nguyên expected của bộ kiểm thử.
- **Citation trong nội dung:** kiểm tra cả mã Txx-NNN trong answer, không chỉ trường citations. Mã trong answer phải thuộc danh sách citations đã được xác minh trong context. Đây là kiểm tra mã, chưa tự chứng minh claim được nguồn hỗ trợ.
- **Độ dài trả lời:** lượt chạy thử có một answer 181 từ bị chặn đúng. Prompt mới đặt mục tiêu 60–120 từ hoặc ngắn hơn và yêu cầu kiểm tra trước khi xuất; giới hạn cứng vẫn 180, không cắt đáp án tự động.
- **Ba đoạn được chọn:** code review phát hiện các continuation chiếm hết sáu slot. Đã tái hiện trước sửa và giới hạn continuation khi có lựa chọn, giữ chỗ cho nguồn truy xuất phục vụ câu hỏi.

## Giới hạn giữ nguyên

Một nguồn mỗi câu hỏi; tối đa 3 đoạn chọn, 6 đoạn context, 3.000 ký tự mỗi đoạn, 12.000 ký tự nội dung; answer tối đa 180 từ. Không thêm câu trả lời giả, không tự đổi refusal thành answer, không thêm retry che lỗi hoặc bỏ lỗi khỏi mẫu số.

Trace ghi prompt_version=grounded-selected-concise-v3, retrieval_version=bm25-concept-continuation-v3. Raw context/output giữ local, ngoài ZIP và Git. Lượt chạy dở trước bản cuối không được dùng làm kết quả cuối.

## Bằng chứng

- 36 kiểm thử offline đạt, gồm kiểm thử thất bại trước sửa cho selected marker, continuation, hai vế so sánh, ba lựa chọn, anchor khái niệm và citation trong answer.
- Retrieval: 15/15 case expected answer có ít nhất một supporting ID (trước sửa 14/15). Chỉ là độ bao phủ truy xuất, không là tỷ lệ câu trả lời đúng.
- Số đo AI thật hiện hành và run ID xem eval/run_results.md. So sánh với run cũ 20260918T035621Z là kiểm tra hồi quy cùng golden set, không phải baseline của tutor cũ, chưa là ước lượng độ cải thiện có ý nghĩa thống kê.
- Chấm nội dung do Codex thực hiện nếu có được ghi riêng, không giả là người học hoặc người chấm độc lập. Các ô review.csv dành cho nhóm vẫn để trống đến khi nhóm chấm thật.

CP3 còn phần chứng minh và nộp: nhóm đối chiếu kết quả, điền nhân sự, quay video và nộp form. UI/video nằm ngoài lượt cải thiện này theo yêu cầu người dùng.
