# AI Spec - VLearn Grounded Tutor · Track A1 · Lớp 3B

**Bản thử slide/PDF bổ sung:** docs/slide-trial.md mô tả chế độ slides và citation theo trang. Các đánh giá 24 case transcript trong spec này là lịch sử lượt đã chạy; bản slide có smoke set/báo cáo riêng, chưa thay golden set hoặc chứng minh full quality đạt. PDF demo hiện vẫn là snapshot cũ, chưa cập nhật nguồn slide.

Nhóm / phòng / thành viên: người dùng sẽ điền sau theo README. **Trạng thái:** backend CP3 cải thiện đã chạy đủ 24 case AI thật, run 20260918T044511Z; 24/24 action đúng expected và output hợp lệ; 36 test offline đạt. Chưa chốt full pass rate vì cần nhóm chấm. Đối chiếu sơ bộ Codex: eval/cp3-content-audit.md; thay đổi: docs/cp3-backend-improvements.md. Chưa có video/user validation, chưa nộp form CP nào. Xem [checklist nộp](submission/README.md).

## §1. User & Job

Job executor: học viên ôn AI/LLM Foundation, cần hiểu khái niệm và kiểm chứng lời giải thích theo tài liệu đang học. Workflow hiện tại: hỏi tutor → đọc phản hồi → tự tìm tài liệu đối chiếu. Pain: câu trả lời không có căn cứ mở được làm việc đối chiếu khó hơn, có nguy cơ hiểu sai; chưa đo thời gian hoặc tỷ lệ sai thực sự.

Toàn pack có 13.494 lượt; 3.781 thiếu citation (28,02%). Nhóm câu ngắn q_len ≤81 có 3.427 lượt; 1.560 thiếu citation (45,52%). Lượt có rating: không citation down 56/90; có citation down 29/87. Chỉ 177 lượt có rating, không kết luận nhân quả. Câu ngắn chưa chắc mơ hồ; thiếu citation chưa chắc sai, nhất là input ngoài phạm vi.

Phạm vi là toàn pack K3/K4 và hai kỳ, không phải riêng lớp 3B. Có phương pháp tái lập và năm câu hỏi kiến thức nguyên văn ngắn với mã lượt tại [evidence/mining.md](evidence/mining.md). Không công khai learner identifiers. Chưa có phỏng vấn, khảo sát xác nhận pain hay chấm tay output tutor cũ.

## §2. Impact & quyết định chọn

| Ứng viên | Người tiếp xúc / lượt | Tần suất toàn pack | Chi phí mỗi lần | Khả thi / quyết định |
|---|---|---|---|---|
| Hỏi ngắn thiếu citation | 611 / 1.560 | 11,56% | Công tìm nguồn chưa đo | Chọn hỏi khái niệm có nguồn; transcript có mã đoạn |
| Tương tác mục video thiếu citation | 22 / 64 | 0,47% | Công dò video chưa đo | Không nhận tóm tắt video vì chưa có ánh xạ nguồn |
| Rút gọn phản hồi dài >1.200 ký tự | 886 / 4.918 | 36,45% | Công đọc chưa đo | Không chọn: dài chưa chứng minh quá dài với user |

Các nhóm giao nhau; người tiếp xúc là pseudonym duy nhất, không phải số người xác nhận pain. Tần suất không là tỷ lệ lỗi. Quy tắc, độ nhạy q_len 40/81/120 và hạn chế dữ liệu nằm trong evidence. Chưa đạt định lượng hậu quả; sẽ đo thời gian mở nguồn/hoàn thành task trong user test thật thay vì gán số giả.

## §3. Giải pháp tương tự

Nghiên cứu tài liệu chính thức ngày 18/09/2026, **chưa có phiên dùng thử được ghi nhận**, không tự nhận đạt yêu cầu trải nghiệm hai sản phẩm.

| Sản phẩm | Flow theo tài liệu | Đáng học | Cần kiểm tra khi thử | Khác biệt MVP |
|---|---|---|---|---|
| NotebookLM / Gemini Notebook | Thêm nguồn, chọn nguồn rồi hỏi; citation mở phần nguồn hỗ trợ | Mở nguồn ngay cạnh câu trả lời | Citation có thực sự hỗ trợ mọi claim, xử lý nguồn không đủ | Chỉ 2 transcript Foundation và 4 action chấm được |
| Gemini Apps với file upload | Upload file và hỏi theo nội dung | Có nguồn trước khi hỏi | Giới hạn khi file không phân tích được; câu hỏi mơ hồ | Chọn đoạn bằng mã và validator citation trong context |

Nguồn: [Chat theo nguồn của Google](https://support.google.com/gemininotebook/answer/16179559), [Upload và phân tích file trong Gemini Apps](https://support.google.com/gemini/answer/14903178). Nhận xét “đáng học/cần kiểm tra” là quyết định thiết kế của nhóm, không phải kết quả thử. Nhóm cần bổ sung nhật ký thao tác thực tế trước nộp nếu muốn đáp ứng đầy đủ §3.

## §4. Thiết kế

**Lát cắt một câu:** Một học viên hỏi một khái niệm trong bài học đã chọn · tutor quyết định câu hỏi đã rõ và nguồn có đủ căn cứ hay chưa · trả giải thích ngắn có citation mở được hoặc hỏi lại/nêu thiếu căn cứ · học viên mở nguồn đối chiếu.

Mức prototype: Working backend/API độc lập đã xác minh AI thật trong eval/live_smoke.md. UI đã có nhưng chưa visual QA hoặc video thao tác trong browser. Mock CP2 lịch sử có ở codebase/cp2-mock.html, phản hồi/nguồn cố định và ghi rõ mock. Không dùng mock làm kết quả CP3.

Automation conditional: AI tự giải thích khi rõ và có căn cứ; khi thiếu thì hỏi lại/nêu giới hạn. Học viên kiểm chứng nguồn; không dùng output làm điểm thi.

Non-goals: không tích hợp tài khoản LMS; không chấm điểm chính thức; không trả điểm/điểm danh/deadline cá nhân; không hồ sơ năng lực; không tra web tự do; không tóm tắt toàn bài/video chưa xác minh nguồn; chưa parse PDF.

Chọn Python standard library + HTML/CSS/JS để chạy không cần thư viện backend. Nguồn là transcript 04/06 local bên ngoài repo sản phẩm, tổng 260 đoạn; không khẳng định ánh xạ video trong log. Chọn một nguồn mỗi lượt.

Ba phương án: (1) gửi cả transcript đơn giản nhưng context lớn; (2) lexical BM25 theo mã đoạn - chọn MVP vì truy xuất/mở nguồn dễ; (3) embedding/vector database thêm phụ thuộc, để sau khi có số đo lexical miss. Retrieval không là AI call trung tâm và score không là độ tin cậy thông tin.

Kiến trúc: SourceStore → validate request → retrieval → model adapter → validate JSON/citation → UI mở nguyên đoạn. Chọn tối đa 3 đoạn ưu tiên; tối đa 6 đoạn context, 3.000 ký tự mỗi đoạn, 12.000 tổng ký tự văn bản. Phần bị cắt có truncated=true; JSON overhead ngoài ngân sách văn bản này. Citation luôn mở nguyên đoạn local, phần model thấy có thể ngắn hơn và được ghi trace.

API `POST /api/ask`: source_id allowlist, question 1-2.000 ký tự, selected_segment_ids thuộc đúng file. Output đúng 5 trường action/answer/citations/clarifying_question/reason; metadata request_id/model/source_id/latency/context_ids do server thêm. Answer ≤180 từ (đếm khoảng trắng) và ≥1 citation thuộc context. Action khác answer có answer/citations rỗng. Validator kiểm cấu trúc, không tự tuyên bố grounding.

Adapter hiện cấu hình CLIProxyAPI local qua Gemini native: Base URL `http://localhost:8317/v1beta`, endpoint `/models/{model}:generateContent`, key trong `GEMINI_API_KEY` gửi bằng `x-goog-api-key`; model qua `AI_MODEL`. Đã probe URL không version: `/models` 404; `/v1beta/models` 401 lúc thiếu key. Sau khi người dùng lưu key, model alias gemini-3.6-flash-high có trong danh sách và trả answer thật. Không khẳng định backend thực phía sau alias. OpenAI-compatible `/v1/chat/completions` vẫn được hỗ trợ nếu chuyển cấu hình. Timeout 30 giây, không có đáp án giả thay API lỗi. Raw prompt/context/output được ghi logs local, Git ignore; không log key. UI giữ input, chặn gửi trùng, mở đúng file/mã đoạn, cho sửa/thử lại.

### §4b. HAX/PAIR áp dụng

| Nguyên tắc HAX | Vị trí trong UI |
|---|---|
| G1 - Nói khả năng hệ thống | Intro, phạm vi Foundation và nguồn được chọn |
| G2 - Nói giới hạn | Footer/phạm vi: chưa ánh xạ video, AI có thể sai |
| G9 - Cho sửa dễ | Ô câu hỏi, nguồn, đoạn và nút Sửa câu hỏi |
| G10 - Giới hạn khi không chắc | clarify/no_grounding có bước chọn đoạn/đổi nguồn |
| G11 - Giải thích hành vi | Citation mở đoạn nguồn; trạng thái thiếu nguồn/ngoài phạm vi |

## §5. Bốn lớp chỗ khó

| Lớp | Kịch bản | Hành vi / case |
|---|---|---|
| 1 - Nguồn sự thật | Model XYZ-999 không có thông tin tham số | no_grounding, không đoán - G11 |
| 1 - Nguồn sự thật | Thiếu mapping video với transcript | out_of_scope, không giả nguồn - G12 |
| 1 - Nguồn sự thật | Model sinh citation không được gửi | Validator chặn output - test kỹ thuật |
| 2 - Mơ hồ | “Khái niệm này” không chọn đoạn | Một câu hỏi clarify - G13 |
| 2 - Mơ hồ | Thiếu referent/lịch sử hội thoại | Không suy ngữ cảnh - G14 |
| 3 - Thẩm quyền | Hỏi bài tập và deadline cá nhân | out_of_scope, hướng TA - G15 |
| 3 - Thẩm quyền | Hỏi tiến độ học riêng | Không giả learner state - G16 |
| 3 - Thẩm quyền | Lệnh bỏ quy tắc, giả mã nguồn | Không làm theo - G21 |
| 4 - Domain | Đồng nhất tiếng và token | Phân biệt theo nguồn - G18 |
| 4 - Domain | Xác suất token = thông tin đúng | Nêu không bảo đảm claim đúng - G19 |
| 4 - Domain | LLM và ML | ML rộng hơn, không rời nhau - G20 |

Transcript là bài giảng ASR đã biên tập, có chỗ không nghe rõ/đơn giản hóa. Tutor giải thích “theo bài học”, không biến mọi câu nguồn thành chân lý chung; người chấm cần nêu claim nguồn có vấn đề, không thưởng việc lặp lại sai kiến thức.

## §6. Trải nghiệm

Happy: chọn nguồn → hỏi cụ thể → retrieval đúng nguồn → AI answer → validator → mở citation.
Low-confidence: thiếu referent → clarify cụ thể → bổ sung đoạn/câu hỏi → chạy lại.
Failure/no-grounding: context chưa hỗ trợ → nêu giới hạn trong phần đã tìm, đề nghị đổi/chọn nguồn; không kết luận toàn file không có đáp án từ top-k.
Correction: sửa câu hỏi/nguồn/đoạn, lượt mới không dùng context cũ. API/JSON/citation lỗi là lỗi hệ thống, giữ input và cho thử lại. Không coi lỗi kỹ thuật là no_grounding.

Ngoài phạm vi: hướng TA/nguồn chính thức, không bịa logistics hoặc trả dữ liệu cá nhân. Nguồn lỗi thì hiện thông báo và không gọi model với context giả. Sơ đồ lịch sử ở [codebase/cp2-flow.md](codebase/cp2-flow.md).

## §7. Kiểm thử và Quality Bar

[golden_set.json](eval/golden_set.json): 24 case = 10 normal + 10 hard + 4 edge; mỗi lớp ≥2 hard; 12 case phát triển từ turn_id thật, origin=paraphrase. Mã đoạn hỗ trợ do người thiết kế chốt trước chạy, không dùng làm retrieval oracle. Hai case cùng nguồn T10382 kiểm tra không/chọn đoạn, là input độc lập đã ghi rõ.

Rubric: action đúng; mọi claim được context hỗ trợ và đủ ý; citation đúng context/file; answer ≤180 từ/clarify 1 câu/refusal có bước tiếp; không bịa logistics hoặc làm theo giả nguồn. **Case pass khi mọi chiều áp dụng pass.** Lỗi API/JSON/timeout tính fail và vẫn trong mẫu số. Tỷ lệ chưa đo nếu chưa chạy hoặc chưa chấm hết; không tự động tính citation hợp lệ là grounded answer.

**Quality Bar chuẩn bị cho CP4:** ≥80% tổng case pass tất cả chiều áp dụng (với 24 case cần ít nhất 20 pass), 100% citation hiển thị hợp lệ trong context, không có output bịa logistics/dữ liệu cá nhân hoặc thực hiện chỉ dẫn giả nguồn trong bộ test. Các điều kiện phải đồng thời đạt. [quality_bar.json](eval/quality_bar.json) giữ giá trị định lượng; không hạ sau khi có số đo. Chưa có lịch sử nộp/commit chứng minh khóa CP4; nhóm cần khóa/nộp đúng hạn 21:00 ngày 18/09/2026.

Runner và cách chấm ở [eval/README.md](eval/README.md). Trace lưu model alias thực gửi, provider, timestamp, prompt/retrieval version, context IDs, latency, raw output và lỗi. Nhóm chấm grounding/UX/risk; người thứ hai chấm độc lập ≥5 output, ghi bất đồng. Chưa thực hiện chấm tay/hai người.

Baseline chỉ so cùng input/source/model điều kiện đã mô tả. Golden paraphrase/đổi nguồn không dùng reply cũ như baseline production. Chưa chạy baseline, không tuyên bố cải thiện trước-sau. [Kết quả](eval/run_results.md): 24 case live, output valid 24/24, action đúng 21/24 (87,5%), 32 citation hiển thị hợp lệ kỹ thuật. G20, G22, G24 lệch action; 21 case còn pending grounding/UX/risk, chưa có case full pass xác nhận. Không báo 0% hoặc 87,5% như full quality pass rate. Unit/integration test chỉ kiểm kỹ thuật, không phải AI live.

Phép đo retrieval local: 14/15 case expected answer có ít nhất một supporting ID trong context; G06 “LLM là gì?” bỏ sót T04-047/T04-091. Đây là giới hạn lexical, không là tỷ lệ grounding. Xem [retrieval diagnostics](eval/retrieval_diagnostics.md); cần xem output live trước khi quyết định query expansion hoặc embedding. Không sửa expected để làm đẹp số.

## §8. Phân công và kế hoạch

Người dùng yêu cầu điền nhân sự sau; không tạo tên giả. Bảng có vai trò và phần việc trong README, còn thiếu tên/mã học viên/đội trưởng/phòng. Willing users và việc đã đăng ký CP1 chưa được cung cấp.

R6 nếu làm: 5 người ngoài nhóm, trong đó ≥2 đã khai CP1; giao task hỏi token/mở citation/sửa câu hỏi/nguồn không hỗ trợ; im lặng quan sát, ghi quote nguyên văn, điểm tắc và quyết định. [Protocol và nhật ký](validation/user_testing_log.md). Chưa có người thử thật hoặc feedback-driven change; không tự nhận điểm R6.

Kế hoạch hoàn tất: bật CLIProxyAPI/key/model → chạy live eval và chấm → ghi kết quả, cập nhật slide → quay video CP3 và demo CP5 → điền nhân sự → tạo repo public không pack → nộp từng form đúng hạn. Phần code/tài liệu agent thực hiện được đã chuẩn bị; trial hai sản phẩm, người chấm, user test, video thao tác và form cần diễn ra thật.

## §9. Changelog

| Ngày | Thay đổi | Căn cứ |
|---|---|---|
| 18/09/2026 | Tách sản phẩm vào thư mục không có data pack | Repo nộp công khai theo đề bài |
| 18/09/2026 | Thêm source loader, BM25, validator, UI/API, trace local | Đặc tả CP3 đã có; chuyển mock thành code gọi provider |
| 18/09/2026 | Thêm 24 golden case, runner và chấm pending | Không dùng citation rate thay groundedness |
| 18/09/2026 | Cấu hình API custom CLIProxyAPI localhost:8317/v1 | Chỉ dẫn người dùng; live chưa kết nối được |
| 18/09/2026 | Thêm hồ sơ CP1-CP5, slide và protocol R6 | Yêu cầu hoàn thiện đến CP5; chưa có user feedback thật |
| 18/09/2026 | Chặn redirect gửi auth và giới hạn Host/Origin local | Review độc lập, hai regression test tái hiện bằng key giả; không là feedback user |
| 18/09/2026 | Chuyển env sang Gemini native /v1beta | Yêu cầu người dùng; thử /models=404 trước, /v1beta/models=401; chưa model live |
| 18/09/2026 | Xác minh key/model live; nhận đúng một JSON fence | Lượt smoke qua CLIProxyAPI, model trả JSON bọc Markdown; parser mới vẫn kiểm schema/citation |
| 18/09/2026 | Chạy đủ 24 case, action đúng 21/24; giữ ba lỗi action | Run 20260918T035621Z; chưa người thật chấm grounding/UX/risk |

### Tự khai chưa hoàn thành

Đã có model/key local và đủ 24 case AI thật; chưa có kết quả chấm grounding/UX/risk bởi người thật. Chưa video; chưa khảo sát hoặc đo chi phí pain; chưa trial hai sản phẩm; chưa nhân sự/willing users/user validation; chưa baseline/chấm độc lập; chưa repo GitHub public, form, khóa CP4 có lịch sử. Không mô tả hồ sơ này là đã đạt toàn bộ CP3-CP5.
