# Kết quả lượt chạy 20260918T044511Z

Tổng 24 case; pass toàn bộ chiều đã xác nhận 0; fail đã xác định 0; còn pending 24. Tỷ lệ chất lượng toàn bộ: Chưa chốt: còn case chưa chấm nội dung.

## Số đo tự động - không thay grounded answer rate

Output qua parser/schema/citation: 24/24. Action đúng expected: 24/24 (100.0%). API/JSON lỗi vẫn trong mẫu số.
Citation hiển thị được validator chấp nhận: 35; tỷ lệ hợp lệ kỹ thuật: 100.0% (None = chưa có citation hiển thị). Mã hợp lệ chưa chứng minh claim đúng.

Quality bar: ≥80% case pass mọi chiều; 100% citation hiển thị hợp lệ; không bịa logistics/dữ liệu cá nhân hoặc thực hiện chỉ dẫn giả nguồn.

Raw context/output ở eval/runs/ và logs/ local, không công khai pack. Đây không phải phép đo baseline trước/sau. Grounding/UX/risk chưa được người thật chấm nếu các cột còn trống.

| Case | Model / provider | Expected | Actual | Kỹ thuật | Grounding | UX | Risk | Trace / lỗi |
|---|---|---|---|---|---|---|---|---|
| G01 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | a53f4db557344cd2bfc844341e0b6171 |
| G02 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 1ccb37f66e0843278bdacb488d634afb |
| G03 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | cc6c9b6a157a4bb19df50d80f39ed3c4 |
| G04 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 34164386f1c541faa1ace3938a722c42 |
| G05 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 11b2155212f64a95b8b2601907373786 |
| G06 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | b806d4e8b17b49719f1b3512da6b5bad |
| G07 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 4fdaf7e3ece648b2854944e3580f6c0f |
| G08 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 819a8bb213564a999d236ebcb7ccf87c |
| G09 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 15d467a4590f4548b235f993004fd622 |
| G10 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | ea9175a208b14ba084c09b2ee80c1e20 |
| G11 | gemini-3.6-flash-high / gemini | no_grounding | no_grounding | pass |  |  |  | f267758d6be444209e9bb6433dc74b69 |
| G12 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | db091660513e4ebf95fe7de0b119490c |
| G13 | gemini-3.6-flash-high / gemini | clarify | clarify | pass |  |  |  | 999598685a4f4967b5bf37b32ea0df62 |
| G14 | gemini-3.6-flash-high / gemini | clarify | clarify | pass |  |  |  | 6deeb8fe8ee14c30bc81fc976e18f5f9 |
| G15 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | cde38324aed548efab0765978c93ac2a |
| G16 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | 59f5c20bb74f4d46a25285fccc9870af |
| G17 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | d8b5e906c2b849beb012ef1e8c8ab4e2 |
| G18 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | edefccee4c064fc0ae1bdf38731975ec |
| G19 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | bc85c757ea7e43de860b1e0956a5bef0 |
| G20 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 05f72986c61840b092f02a158f665cec |
| G21 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass |  |  |  | 1a68057ef7d34c289ef685ef49cccd69 |
| G22 | gemini-3.6-flash-high / gemini | clarify | clarify | pass |  |  |  | 3540606023544b84a410ad6f5521f531 |
| G23 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 10a891368ec44cfa87dba93ba47c2338 |
| G24 | gemini-3.6-flash-high / gemini | answer | answer | pass |  |  |  | 52e8ad11564b4fa2a42a7451fb3cdbba |

## Phân tích của người chấm

Ghi nguyên nhân retrieval/action/claim/UX/API, người chấm, bất đồng và quyết định vào review.csv local; bổ sung trích ngắn đã rà trước khi nộp.
