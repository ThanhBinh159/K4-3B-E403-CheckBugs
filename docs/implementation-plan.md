# VLearn Grounded Tutor - CP3 đến CP5

**Goal:** Prototype hỏi bài có nguồn, bộ eval và hồ sơ nộp từng checkpoint.
**Architecture:** Python standard library phục vụ web local; nguồn transcript đặt ngoài repo. Retrieval lexical theo mã đoạn; model quyết định action và sinh JSON; validator chặn citation không thuộc context. Gemini và API Chat Completions tương thích OpenAI được cấu hình qua biến môi trường.
**Spec:** ../../K4-3B-Day05-06-AI-Product-Hackathon/cp3-spec.md

## Giới hạn

- Không copy data pack hoặc API key vào repo sản phẩm.
- Câu hỏi tối đa 2.000 ký tự; chọn tối đa 3 đoạn; context tối đa 6 đoạn / 12.000 ký tự; mỗi đoạn tối đa 3.000 ký tự.
- Timeout 30 giây; output answer tối đa 180 từ; mọi answer cần citation.
- 24 golden case: 10 normal, 10 hard (ít nhất 2/lớp), 4 edge; ít nhất 10 từ lượt thật, phân biệt paraphrase.
- Không bịa số đo, tên người thử, quote, video hoặc việc đã nộp form.

## Thực hiện

- [x] 1. Viết test loader, retrieval, input/output validator trước; chạy RED. Implement codebase/core.py và chạy GREEN.
- [x] 2. Test provider và HTTP bằng local fake provider (chỉ là test kỹ thuật). Implement provider.py, server.py, UI; kiểm tra JSON lỗi, thiếu cấu hình và citation mở đúng file. UI chưa visual QA vì không có browser connected.
- [x] 3. Tạo golden_set.json từ mã lượt/đoạn thật, runner lưu raw trace local, phiếu chấm; số đo grounding chỉ sau chấm tay.
- [x] 4. Hoàn thiện spec, evidence/impact, README, validation protocol, reflection template và kịch bản video. Ghi rõ nhân sự/validation chưa được cung cấp.
- [x] 5. Tạo slide PDF đúng 6 trang, render kiểm tra; số đo chưa chạy ghi “chưa đo”. Tạo submission/ hướng dẫn hồ sơ CP1-CP5.
- [x] 6. Chạy toàn bộ test, kiểm tra golden set và package không chứa pack/key. Báo phần đã hoàn thành và phần phụ thuộc người dùng.

## Kết quả / điều chỉnh phạm vi

- 29 test kỹ thuật offline pass (24 codebase + 5 eval); JS syntax hợp lệ. Golden IDs/source mapping được kiểm tra local.
- Retrieval có supporting-ID overlap 14/15 case answer; giữ nguyên kết quả, không nhận là model pass rate.
- Review độc lập tìm ra redirect chuyển tiếp auth và Host không giới hạn; đã tái hiện bằng fixture và sửa, test regression pass.
- PDF 6 trang đã render và xem; UI chưa visual QA vì không có browser connected.
- Theo chỉ dẫn mới của người dùng, API live đang lỗi nên hoãn xác minh model/key, chạy/chấm live và video AI. Nhân sự do người dùng tự điền sau.
- Sau khi người dùng hoàn thiện .env: key/model alias xác minh được, smoke call thành công; bộ 24 case đã chạy (24 valid, 21 action match). Vẫn chưa có chấm grounding/UX/risk người thật hoặc video.
