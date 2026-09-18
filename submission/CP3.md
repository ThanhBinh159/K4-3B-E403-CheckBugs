# CP3 - AI thật và backend đã cải thiện

Hồ sơ: codebase/ có API adapter, eval/golden_set.json có 24 case và 12 mã lượt thật, eval/run.py chạy/chấm, eval/run_results.md tách số kỹ thuật tự động và quality pending. Raw trace local không public nguyên context. Đã có một lượt AI thật được xác minh ở eval/live_smoke.md.

Form cần: mã đội trưởng, video thao tác ~30 giây AI thật và số đo tổng case/pass/fail/tỷ lệ, link kiểm chứng repo/report theo yêu cầu form BTC.

Run mới 20260918T044511Z: 24/24 output hợp lệ; action đúng 24/24 (100%); 35 citation hợp lệ kỹ thuật; answer dài nhất 159 từ. Mọi trace đúng phiên bản prompt/retrieval và giới hạn context. 36 test offline đạt. Run cũ 20260918T035621Z có action đúng 21/24; G20/G22/G24 đã đúng trong lượt mới. Một lượt không bảo đảm mọi lần gọi đều đúng.

Đã sửa truy xuất hai vế so sánh/tên đầy đủ/đoạn kế tiếp, dấu đoạn được chọn, quy tắc hỏi lại và kiểm citation trong answer. Xem docs/cp3-backend-improvements.md. Codex đối chiếu sơ bộ ở eval/cp3-content-audit.md, không thay nhóm chấm độc lập.

**Chưa đủ nộp như CP3 hoàn thành:** grounding/UX/risk cần nhóm chấm; UI/video được hoãn theo yêu cầu người dùng. Full pass rate chưa chốt, 24 case pending nhóm review, không phải 0% pass. Sau khi chấm, copy số thật trong run_results.md vào form. Không dùng action accuracy hoặc citation validity thay full pass rate. Không điền 20/24 hay 80% vì đó chỉ là quality bar.
