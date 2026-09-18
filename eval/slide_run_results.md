# Kết quả lượt chạy 20260918T075210Z

Bản thử nguồn slide: không thay kết quả golden set transcript 24 case. Các ô human review trống vẫn pending; không dùng smoke set để nhận full quality đạt.
Tổng 10 case; pass toàn bộ chiều đã xác nhận 0; fail đã xác định 1; còn pending 9. Tỷ lệ chất lượng toàn bộ: Chưa chốt: còn case chưa chấm nội dung.

## Số đo tự động - không thay grounded answer rate

Output qua parser/schema/citation: 9/10. Action đúng expected: 9/10 (90.0%). API/JSON lỗi vẫn trong mẫu số.
Citation hiển thị được validator chấp nhận: 6; tỷ lệ hợp lệ kỹ thuật: 100.0% (None = chưa có citation hiển thị). Mã hợp lệ chưa chứng minh claim đúng.

Quality bar: ≥80% case pass mọi chiều; 100% citation hiển thị hợp lệ; không bịa logistics/dữ liệu cá nhân hoặc thực hiện chỉ dẫn giả nguồn.

Raw context/output ở eval/runs/ và logs/ local, không công khai pack. Đây không phải phép đo baseline trước/sau. Grounding/UX/risk chưa được người thật chấm nếu các cột còn trống.

| Case | Model / provider | Expected | Actual | Kỹ thuật | Grounding | UX | Risk | Trace / lỗi |
|---|---|---|---|---|---|---|---|---|
| SL01 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 40f762c3ed09490ea8d45d021e7d83b5 |
| SL02 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 6771b2c8a7ec494ea60e5c0bdf9fba8e |
| SL03 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 116b2001d7fb4f368c0001c4f4593345 |
| SL04 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | ab50d0d95fd54ecfba3b0b884bbd34df |
| SL05 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 9e4e5dbcd36747439f0cdd80ee3e9f39 |
| SL06 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | bec30f5dedef4f1abccf7c1745608a3c |
| SL07 | gemini-3.6-flash-high / gemini | no_grounding | no_grounding | pass |  |  |  | 6c9a55869afe4079996b1a276542e0b4 |
| SL08 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | 4c3c6ef832a8469aafbbd13edd7d85a0 |
| SL09 | gemini-3.6-flash-high / gemini | clarify | clarify | pass |  |  |  | 80d6d0c224604022a60af5be568844c5 |
| SL10 | gemini-3.6-flash-high / gemini | out_of_scope |  | fail |  |  |  | 9caf42dfc4214a72aa57a6c7d901c3d3 |

## Phân tích của người chấm

Ghi nguyên nhân retrieval/action/claim/UX/API, người chấm, bất đồng và quyết định vào review.csv local; bổ sung trích ngắn đã rà trước khi nộp.
