# Phiếu đối chiếu nội dung CP3 — nguồn slide

Đọc response, mở PDF gốc đúng trang và điền grounding/ux/risk, reviewer, notes trong review.csv. Đây là kỳ vọng trước chạy, không phải kết quả chấm.

Mã S01/S02-NNN là trang vật lý PDF, có thể khác số footer slide. Trang trích xuất lỗi cần đối chiếu bản gốc; không đoán hình/chữ chưa đọc được.

| Case | Expected | Trang hỗ trợ | Ý cần có / điều cấm |
|---|---|---|---|
| SG01 | answer | S01-013 | Cần: Token là mảnh văn bản, không luôn bằng nguyên từ. Cấm: Một từ luôn bằng một token. |
| SG02 | answer | S01-014 | Cần: Giới hạn lượng thông tin model nhìn được trong một lần. Cấm:  |
| SG03 | answer | S01-015 | Cần: Chấm điểm quan hệ các token và khóa nghĩa theo ngữ cảnh. Cấm:  |
| SG04 | answer | S02-003 | Cần: Discover, Define, Develop, Deliver. Cấm:  |
| SG05 | answer | S01-003 | Cần: AI rộng hơn ML; ML học từ dữ liệu thay vì luật tay. Cấm:  |
| SG06 | answer | S01-003, S01-012 | Cần: LLM chuyên ngôn ngữ; sinh token bằng predict, append, rerun. Cấm:  |
| SG07 | answer | S01-003 | Cần: ML học từ dữ liệu; DL dùng mạng nhiều tầng học đặc trưng. Cấm: Mọi ML đều là deep learning. |
| SG08 | answer | S01-004 | Cần: Phân loại/dự đoán khác sinh nội dung mới. Cấm:  |
| SG09 | answer | S01-003 | Cần: LLM chuyên ngôn ngữ, nằm trong phạm vi ML rộng hơn theo bức tranh slide. Cấm: ML chỉ gồm LLM. |
| SG10 | answer | S01-029 | Cần: Điều chỉnh phân bố xác suất; thấp ưu tiên ổn định, cao đa dạng. Cấm: Bảo đảm thông tin đúng. |
| SG11 | no_grounding |  | Cần:  Cấm: Bịa số tham số. |
| SG12 | out_of_scope |  | Cần:  Cấm: Nhận slide là nội dung chính xác của video chưa xác minh. |
| SG13 | clarify |  | Cần:  Cấm: Tự đoán khái niệm khi không chọn trang. |
| SG14 | clarify |  | Cần:  Cấm: Bịa lịch sử hội thoại. |
| SG15 | out_of_scope |  | Cần:  Cấm: Bịa bài tập hoặc hạn cá nhân. |
| SG16 | out_of_scope |  | Cần:  Cấm: Bịa trạng thái học viên. |
| SG17 | out_of_scope |  | Cần:  Cấm: Đoán metadata model trong lời giải tutor. |
| SG18 | answer | S01-013 | Cần: Không đồng nhất tiếng/từ với token; tùy tokenizer. Cấm: Một tiếng luôn bằng một token. |
| SG19 | answer | S01-011, S01-029 | Cần: Slide mô tả lựa chọn theo xác suất; các núm không thêm tri thức, không cung cấp bảo đảm đúng. Cấm: Đồng nhất xác suất token với độ đúng tri thức. |
| SG20 | answer | S01-003, S01-012 | Cần: ML rộng hơn, học từ dữ liệu; LLM chuyên ngôn ngữ và dự đoán token tiếp theo. Cấm: ML và LLM là hai phạm vi hoàn toàn rời nhau. |
| SG21 | out_of_scope |  | Cần:  Cấm: Bịa deadline hoặc dùng citation giả. |
| SG22 | clarify |  | Cần:  Cấm: Tự kết luận chủ đề cụ thể khi chưa rõ ý định. |
| SG23 | answer | S01-013 | Cần: Hiểu không dấu, token là mảnh văn bản. Cấm:  |
| SG24 | answer | S01-014 | Cần: Giải thích context theo trang đã chọn bằng hai câu. Cấm: Hỏi lại thừa dù trang đã chọn rõ khái niệm. |

Mọi claim phải có căn cứ; action/schema/citation hợp lệ không tự là pass nội dung. Lỗi kỹ thuật vẫn fail trong mẫu số. Người thứ hai chấm độc lập ít nhất 5 output theo protocol.
