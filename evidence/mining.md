# Evidence tái lập - VLearn Grounded Tutor

Phạm vi: toàn pack K3/K4 và hai kỳ; không gọi đây là riêng lớp 3B. Mỗi dòng là một lượt hỏi-đáp, không phải người dùng độc lập.

Toàn pack: 13,494 lượt; 3,781 thiếu citation (28.02%).
Hỏi ngắn q_len ≤81: 3,427 lượt, 1,560 thiếu citation (45.52%).

| Rating | Số lượt có rating | Down | Tỷ lệ down |
|---|---:|---:|---:|
| Không citation | 90 | 56 | 62.22% |
| Có citation | 87 | 29 | 33.33% |

Chỉ 177/13494 lượt có up/down; rating tự chọn, chỉ là tương quan. Không chứng minh citation gây giảm downvote hoặc thiếu citation là trả lời sai.

## Impact so sánh ba ứng viên

Tần suất dưới đây dùng chung mẫu số toàn pack. Các tập giao nhau. Số người là learner pseudonym duy nhất, chỉ công bố số tổng.

| Ứng viên | Lượt | Người tiếp xúc | Tần suất | Quy tắc |
|---|---:|---:|---:|---|
| Hỏi ngắn thiếu citation | 1560 | 611 | 11.56% | q_len ≤81 và has_citation=False |
| Tương tác ở video thiếu citation | 64 | 22 | 0.47% | has_citation=False và tiền tố/tên mục video trong question |
| Rút gọn phản hồi dài | 4918 | 886 | 36.45% | reply_len >1.200 |

Chọn hỏi bài có nguồn: tập hỏi ngắn cho thấy thiếu căn cứ kiểm chứng, và transcript có mã đoạn giúp làm prototype nhỏ. Video có tín hiệu yêu cầu lời chép nhưng thiếu ánh xạ video; không nhận làm tóm tắt video chính xác. Output dài chưa chứng minh người học thấy quá dài; để ngoài MVP.

Chi phí mỗi lần và mức thiệt hại chưa đo. Không gán phút mất, điểm mất hay impact tiền giả. Tần suất trong log là mức tiếp xúc, chưa phải tỷ lệ lỗi kiến thức.

## Độ nhạy ngưỡng độ dài

| q_len tối đa | Lượt | Thiếu citation | Tỷ lệ |
|---|---:|---:|---:|
| 40 | 443 | 374 | 84.42% |
| 81 | 3427 | 1560 | 45.52% |
| 120 | 7941 | 2672 | 33.65% |

Ngưỡng 81 là lựa chọn mining kế thừa Canvas, chưa được tối ưu. Câu ngắn không mặc định là mơ hồ; còn ảnh hưởng preset/cohort và ngữ cảnh trước đó.

## Năm ví dụ câu hỏi kiến thức nguyên văn ngắn

| Turn | Trích câu hỏi | Có citation |
|---|---|---|
| T10399 | “AI khác Machine Learning như thế nào?” | False |
| T10400 | “llm là gì” | False |
| T10410 | “Sự khác biệt chính giữa Machine Learning và Deep Learning là gì?” | True |
| T10407 | “LLM khác biệt thế nào với Machine Learning?” | False |
| T10417 | “LLM có phải là một dạng của Machine Learning không?” | False |

Các câu trên chứng minh có tương tác kiến thức, chưa là nhãn reply sai; cần chấm output theo nguồn. Golden set phát triển/paraphrase từ lượt thật, không giữ ánh xạ video chưa kiểm chứng.

## Phương pháp tái kiểm tra

Python csv.DictReader UTF-8-SIG; q_len/reply_len chuyển số nguyên; has_citation so sánh đúng False/True; rating chỉ lấy up/down. Không xuất student, prompt đầy đủ hay nguyên pack.

Chạy từ repo sản phẩm:
```powershell
python -X utf8 tools/mine_evidence.py ../K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/chatlog/tutor_turns.csv
```
