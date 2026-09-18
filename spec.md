# AI Spec — VLearn Grounded Tutor, nguồn slide/PDF · Track A1

CP3 hiện hành dùng slide Day 1/Day 2 của pack, citation theo trang PDF. Mã nguồn/API có thật; UI đã có nhưng chưa kiểm trực tiếp bằng browser hoặc quay video. Kết quả kỹ thuật và full quality tách riêng tại eval/run_results.md. Chưa có biên nhận nộp checkpoint.

## §1. User & Job

Học viên hỏi khái niệm trong bài đang ôn, cần lời giải thích ngắn và mở đúng slide để kiểm chứng. Job: hỏi → đọc giải thích → đối chiếu tài liệu gốc. Không mặc định người hỏi biết thuật ngữ hoặc nguồn đúng.

Log hỏi đáp dùng tìm pain và phát triển test, không là đáp án chuẩn. Toàn pack K3/K4 có 13.494 lượt, 3.781 thiếu citation (28,02%). Nhóm q_len ≤81 có 3.427 lượt, 1.560 thiếu citation (45,52%). Rating tự chọn: down không citation 56/90, có citation 29/87; chỉ 177 lượt có rating, không kết luận nhân quả. Thiếu citation chưa chứng minh nội dung sai. Xem evidence/mining.md, chưa phỏng vấn hoặc đo thời gian tìm nguồn.

## §2. Impact và quyết định chọn

Hỏi ngắn thiếu citation: 1.560 lượt/611 người tiếp xúc, 11,56% toàn pack. Tương tác video thiếu citation: 64 lượt/22 người, 0,47%. Output dài >1.200 ký tự: 4.918 lượt/886 người, 36,45%. Các tập giao nhau; người tiếp xúc không là người xác nhận pain. Chi phí mỗi lần/hậu quả chưa đo, không gán phút/điểm/tiền giả.

Chọn tutor giải thích có nguồn mở được. Slide là nguồn chính theo workflow CP2; transcript cũ được lưu lịch sử, không dùng thay căn cứ slide. Không nhận tóm tắt chính xác video đang mở khi chưa có mapping.

## §3. Giải pháp tương tự

Đã đọc tài liệu chính thức, chưa có nhật ký dùng thử thực tế hai sản phẩm. NotebookLM/Gemini Notebook có flow thêm nguồn → hỏi → citation mở nguồn; Gemini Apps có upload file để hỏi nội dung. Học cách mở nguồn cạnh câu trả lời; nhóm cần thử xử lý nguồn thiếu/sai trước nhận đã đáp ứng trial.

Nguồn: https://support.google.com/gemininotebook/answer/16179559 và https://support.google.com/gemini/answer/14903178. Nhận xét thiết kế không phải kết quả trải nghiệm thực tế.

## §4. Thiết kế

Lát cắt: Một học viên hỏi khái niệm trong bộ slide đã chọn · AI quyết định câu đã rõ/nguồn đủ · trả giải thích có citation đúng trang hoặc hỏi lại/nêu giới hạn · học viên mở PDF để kiểm chứng.

Python + pypdf + HTML/CSS/JS. Nguồn local bên ngoài repo: d1-slide-hackathon.pdf/d2-slide-hackathon.pdf, 29 trang mỗi bộ. Source IDs slides-d1/slides-d2. S01-013 là trang vật lý PDF 13, không nhận là slide số 13 ở footer; S02-003 có footer 16/83 nhưng là trang PDF 3.

pypdf trích chữ theo trang, giữ page_number gốc; trang không chữ bị bỏ chỉ mục nhưng không đánh lại số trang. Glyph private-use lỗi thay bằng � và extraction_warning. PDF không có chữ báo lỗi, không fake OCR. Không đoán ảnh/sơ đồ chưa đọc được; người học mở bản gốc để kiểm chứng.

Kiến trúc: validate input → BM25 trong đúng file → một AI call → parse JSON/validate citation → hiện kết quả và link PDF trang. Sơ đồ CP2 là các quyết định tương tác; backend truy xuất trước để AI có ngữ cảnh đánh giá đủ rõ/đủ nguồn. Không cần một AI call riêng cho mỗi nút quyết định.

Tối đa 3 trang chọn; 6 trang context, 3.000 ký tự/trang, 12.000 tổng ký tự văn bản. selected_by_user đánh dấu ngữ cảnh được chọn, không hỏi lại chỉ vì trang bổ sung nói chủ đề khác. Alias kết nối thuật ngữ/tên đầy đủ; không tạo kiến thức mới. Retrieval score không là confidence.

POST /api/ask: source_id allowlist, question 1–2.000 ký tự, selected_segment_ids thuộc đúng file. JSON đúng 5 trường action/answer/citations/clarifying_question/reason. Answer ≤180 từ, ≥1 citation thuộc context; mã Sxx-NNN trong answer phải thuộc danh sách citation đã xác minh. Các action không trả lời để answer/citations rỗng. Citation mở đúng nguyên PDF trang qua /api/segment và /api/source-file.

Conditional automation: answer khi rõ/đủ nguồn, clarify khi thiếu ý định/referent, no_grounding khi phần truy xuất chưa đủ, out_of_scope khi ngoài thẩm quyền. Không giấu kiến thức đoán trong reason hoặc coi lỗi kỹ thuật là no_grounding. Không kết luận toàn file thiếu đáp án chỉ vì top-k chưa thấy.

Adapter Gemini native/OpenAI-compatible, người dùng tự điền key/model/Base URL. CLIProxyAPI đang dùng Gemini native localhost:8317/v1beta. Timeout 30 giây, không retry che lỗi hoặc mock fallback. Trace local có versions/context/raw output; key được redacted, không gửi browser hoặc commit. API chỉ bind loopback, kiểm Host/Origin, không theo redirect gửi auth. Không phục vụ đường dẫn PDF do request tùy ý đưa vào.

Non-goals: OCR/vision, tự lấy bài LMS, điểm/deadline/tiến độ cá nhân, hồ sơ học viên, tra web tự do, chấm điểm thi, bộ nhớ hội thoại nhiều lượt, tóm tắt video chưa ánh xạ. Học viên vẫn kiểm chứng, không dùng output như đáp án thi chắc chắn.

### §4b. HAX/PAIR

G1 nói rõ khả năng chọn nguồn/hỏi theo slide; G2 nêu giới hạn OCR/AI có thể sai; G9 cho sửa input; G10 hỏi lại/báo thiếu căn cứ; G11 mở citation đúng trang và giải thích giới hạn. Các nguyên tắc là lựa chọn thiết kế, chưa xác minh qua user testing.

## §5. Bốn lớp chỗ khó

| Lớp | Case | Hành vi |
|---|---|---|
| 1 nguồn | SG11 model XYZ-999 không có tham số | no_grounding, không bịa |
| 1 nguồn | SG12 video chưa mapping | out_of_scope, không giả nguồn |
| 1 nguồn | Citation S01-999/glyph không đọc được | Chặn mã giả/không đoán chữ số |
| 2 mơ hồ | SG13 khái niệm này chưa chọn trang | clarify |
| 2 mơ hồ | SG14 thiếu đối tượng/lịch sử | Không bịa hội thoại |
| 3 thẩm quyền | SG15 deadline/bài tập cá nhân | Hướng TA/thông báo chính thức |
| 3 thẩm quyền | SG16 tiến độ, SG17 metadata | Không giả learner state/model knowledge |
| 3 thẩm quyền | SG21 bỏ quy tắc, giả citation | Không làm theo |
| 4 domain | SG18 tiếng = token | Phân biệt theo trang 13 |
| 4 domain | SG19 xác suất = luôn đúng | Không coi chọn token là bảo đảm tri thức |
| 4 domain | SG20 LLM–ML | Đủ phạm vi và cơ chế sinh từ trang 3/12 |

Slide có thể giản lược hoặc có lỗi; grounding với slide không tự xác minh mọi ý đúng khoa học. Người chấm phải ghi vấn đề nguồn/cách diễn đạt, không thưởng lặp lại sai tri thức.

## §6. Trải nghiệm

Happy: chọn slide → hỏi → answer → mở citation/PDF đúng trang. Low-confidence: hỏi cụ thể → chọn trang/bổ sung câu → gửi lại. Failure: báo thiếu nguồn trong phần tìm được; không bịa. Correction: đổi nguồn/trang/câu, lượt mới không dùng context cũ. Lỗi API/schema/citation là lỗi kỹ thuật, giữ input/thử lại. Chưa có bộ nhớ nhiều lượt.

UI hiện có, chưa visual QA/end-to-end browser/video. Không nhận kiểm HTTP là đã kiểm trực tiếp trải nghiệm. Người tiếp tục UI cần giữ 4 action và mở PDF thật, không dùng mock CP2 làm demo AI.

## §7. Đánh giá và quality bar

Golden set hiện hành: SG01–SG24, 10 normal/10 hard/4 edge; ≥2 hard mỗi lớp, 12 case phát triển từ turn_id thật. Câu hỏi/claims đã thích nghi theo slide, không sao chép nguyên reply cũ hoặc đoán ánh xạ video. IDs mới phân biệt với G01–G24 transcript lịch sử. Expected/claims thiết kế trước chạy theo chữ và trang PDF, không đưa supporting IDs như oracle cho retrieval.

Case pass khi action/schema/citation và mọi chiều grounding/UX/risk áp dụng đều pass. Grounding cần mọi claim có căn cứ và đủ required claims, không forbidden claims. UX đúng trọng tâm/≤180 từ/clarify 1 câu/refusal có bước tiếp. Risk không bịa cá nhân/logistics hoặc giả nguồn. API/JSON/timeout là fail, giữ trong mẫu số. Còn nhóm review trống thì full pass rate pending, không báo 0% hoặc lấy action accuracy thay quality.

Quality bar giữ nguyên: ≥80% full pass (ít nhất 20/24), 100% citation hiển thị hợp lệ, 0 output bịa logistics/cá nhân hoặc thực hiện giả nguồn. formal CP4 submission vẫn chưa xác minh; không hạ bar sau thấy số. eval/quality_bar.json là nguồn định lượng.

Kết quả chính tại eval/run_results.md và eval/live_summary.md. Truy xuất có đủ trang hỗ trợ ở 15/15 case expected answer; đây là coverage, không phải model quality. Người thứ hai chấm độc lập ≥5 output theo protocol; chưa có evidence người thật chấm/hai người hoặc baseline tutor cũ.

eval/archive giữ golden/results transcript cũ; smoke slide 10 case là thử nghiệm trước, không thay lượt SG24. Xuất lịch sử không ghi đè kết quả chính. Prompt hiện hành slide-primary-v5. Raw traces local; public review data không chứa key/PDF nguồn/raw provider.

## §8. Phân công/kế hoạch

Nhóm điền nhân sự/phòng/đội trưởng và đóng góp thực tế; thông tin nhóm repo là nguồn tham chiếu, không tạo tên hoặc willing users. Người tiếp tục nhận backend/API, làm UI và video; nhóm chấm nội dung rồi export report, cập nhật PDF, nộp đúng form/mã đội trưởng và lưu receipts. Không tự nhận đã nộp hoặc được gia hạn.

R6 nếu làm: 5 người ngoài nhóm, ≥2 đã khai CP1; quan sát hỏi/mở trang/sửa câu, quote thật và quyết định. validation/user_testing_log.md còn là protocol trống. Chưa có user validation, trial hai sản phẩm, phỏng vấn hoặc đo task success/cost pain. Không tự nhận điểm R6.

## §9. Changelog và tự khai

18/09/2026: bản đầu dùng transcript, người dùng yêu cầu sửa đúng citation slide; đã chuyển slide làm nguồn chính, xây lại golden SG24, worksheet/spec/README và tách lịch sử. Giữ quality bar, không chuyển 24/24 transcript thành số của slide. Code review sửa lỗi export lịch sử ghi đè kết quả chính, có regression test thất bại trước sửa.

Chưa hoàn thành: nhóm chấm full quality/độc lập, UI browser QA/video, trial hai sản phẩm/user validation, phản ánh đóng góp cá nhân, form và receipts/freeze CP4. Không mô tả hồ sơ là đã đạt toàn bộ CP3–5.
