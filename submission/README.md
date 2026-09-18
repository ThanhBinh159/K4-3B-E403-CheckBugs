# Hồ sơ nộp từng checkpoint · Lớp 3B

**Chưa nộp form.** Bản này gom hồ sơ đã chuẩn bị và phần phải bổ sung thật. Xây đến CP5 trước không gia hạn CP1-CP4. Các form cùng mã học viên đội trưởng; link form lấy từ BTC/Discord/VLearn, không có link thật trong workspace.

| Mốc | Hạn | Nộp | File có sẵn | Phần còn thiếu |
|---|---|---|---|---|
| CP1 | 19:30 · 17/09 | Canvas 7 dòng, đội trưởng/mã, repo public, ≥3 willing users | CP1.md, spec §1-2, evidence/mining.md | Nhân sự, repo public, willing users/đăng ký thật |
| CP2 | 21:00 · 17/09 | Link mock/flow/video đi hết luồng | CP2.md, codebase/cp2-mock.html, cp2-flow.svg/mmd | Link kiểm chứng mở được / form |
| CP3 | 16:00 · 18/09 | Video thao tác ~30 giây AI thật + tổng/pass/fail/% | CP3.md, codebase/, golden set, run_results.md; live 24/24 action đúng | Nhóm chấm full pass/fail; kiểm UI/quay video khi tiếp tục; đội trưởng/repo public/form |
| CP4 | 21:00 · 18/09 | Link spec chốt, quality bar và tự khai chưa xong | CP4.md, spec.md, eval/quality_bar.json | Điền nhân sự; khóa có lịch sử commit/nộp đúng hạn |
| CP5 | 22:30 · 18/09 | PDF đúng 6 trang + video demo dự phòng; R6 nếu làm | CP5.md, demo-slides.pdf, validation protocol | Kết quả live cập nhật vào PDF; video thật; R6 thật nếu làm |

## Trình tự hoàn tất

1. Điền .env local: Gemini native với Base URL http://localhost:8317/v1beta, AI_MODEL là model alias thật và GEMINI_API_KEY là key của proxy. Chạy CLIProxyAPI, kiểm tra tools/check_proxy.py.
2. Chạy codebase/server.py, hỏi thật, mở citation; chạy eval/run.py và chấm tất cả output, ghi report. Hai người chấm ≥5 case nếu làm được.
3. Điền nhân sự/phòng/đội trưởng ở README/spec; willing users chỉ ghi người đã đồng ý và đăng ký thực.
4. Sửa slides/content.json theo số thật, chạy tools/build_slides.py và kiểm tra PDF đủ 6 trang. Không thay quality bar để vừa kết quả.
5. Quay video theo video-scripts.md. CP3 và CP5 là hai video khác mục đích; không dùng phản hồi test giả để chứng minh AI live.
6. R6 nếu làm: 5 người ngoài nhóm, ≥2 đã khai CP1, quote thực và quyết định; cập nhật spec/slide. Nếu không, khai chưa làm.
7. Chạy tools/package_submission.py để ZIP sạch; copy vào **repo GitHub mới**, công khai, tên K4-3B-<phòng>-<nhóm>. Không fork/push nguyên repo đề bài.
8. Nộp riêng từng form, đúng mã đội trưởng; lưu biên nhận/link/thời gian thực vào submission/receipts.md.

Chưa có xác nhận nộp thì không đánh dấu CP hoàn thành. Form quá hạn theo README đề bài được 0 điểm checkpoint đó; sản phẩm vẫn chấm theo rubric. Hỏi BTC nếu cần xử lý ngoại lệ, không tự coi là có gia hạn.
