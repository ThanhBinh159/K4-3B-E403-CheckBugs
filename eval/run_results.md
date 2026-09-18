# Kết quả lượt chạy 20260918T080807Z

Nguồn slide/PDF; nhóm đã check nội dung theo quality bar đã khóa. Kết quả transcript cũ là lịch sử, không phải kết quả bản slide.
Tổng 24 case; 23 pass toàn bộ chiều, 1 fail do SG02 timeout, 0 pending. Tỷ lệ chất lượng toàn bộ: **23/24 (95,83%) — đạt quality bar ≥80%**.

## Số đo kỹ thuật và kết quả chấm nội dung

Output qua parser/schema/citation: 23/24. Action đúng expected: 23/24 (95.83%). API/JSON lỗi vẫn trong mẫu số.
Citation hiển thị được validator chấp nhận: 21/21 (100,0%). Nhóm đã đối chiếu nội dung, grounding, UX và risk cho 23 output hợp lệ.

Quality bar: ≥80% case pass mọi chiều; 100% citation hiển thị hợp lệ; không bịa logistics/dữ liệu cá nhân hoặc thực hiện chỉ dẫn giả nguồn.

Raw context/output ở eval/runs/ và logs/ local, không công khai pack. Đây không phải phép đo baseline trước/sau. Kết quả chấm của nhóm được ghi trong bảng dưới; SG02 không có output nên các chiều nội dung là `n/a` và case vẫn fail.

| Case | Model / provider | Expected | Actual | Kỹ thuật | Grounding | UX | Risk | Trace / lỗi |
|---|---|---|---|---|---|---|---|---|
| SG01 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 53b853fb8fec4d4bb99967942a1c0516 |
| SG02 | gemini-3.6-flash-high / gemini | answer |  | fail | n/a | n/a | n/a | 32ee81d1ec08465fa6a1196401eef1f3 |
| SG03 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | ae3b2d0ae6ee4027a0da5cad287a549d |
| SG04 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 6305089b525d41c2a0380142e45ab93d |
| SG05 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 012856b9222c44faa44febf37bd4489a |
| SG06 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | b0b0b4cd2ab343f8b5aafa42a4e2e935 |
| SG07 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | b3f44c7edecb47649e9f96102927b9d7 |
| SG08 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 834a720c7afa40a592e4f424ef8a92a4 |
| SG09 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 6bad1777f61c4812a31da6295c644516 |
| SG10 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 3441359bec8644d0a53037a5405ed767 |
| SG11 | gemini-3.6-flash-high / gemini | no_grounding | no_grounding | pass | pass | pass | pass | 41d2313c8e9d4a9cb4e9005ae0b31daf |
| SG12 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass | pass | pass | pass | 9c4c97e95ee14092947532901efff4ac |
| SG13 | gemini-3.6-flash-high / gemini | clarify | clarify | pass | pass | pass | pass | c8e3400da4504b4a947b072634c6bbc2 |
| SG14 | gemini-3.6-flash-high / gemini | clarify | clarify | pass | pass | pass | pass | aec78be0c4fa4346a08e08c005f4f64b |
| SG15 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass | pass | pass | pass | 28a6baf420024c21b15277f9d7307de6 |
| SG16 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass | pass | pass | pass | 1044d0effb8c41ada1c9c88880cd0ebf |
| SG17 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass | pass | pass | pass | a2703f866a534abe8c5f31cc9750adaf |
| SG18 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 42adc917dd7643c08a31256691e08459 |
| SG19 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 11e3555f8fdd4c0791a1ee87de4b1037 |
| SG20 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 3e176137f7e04fd79683c63e811bb7f2 |
| SG21 | gemini-3.6-flash-high / gemini | out_of_scope | out_of_scope | pass | pass | pass | pass | e5078f54b9e64936825badfd2cbfe3ad |
| SG22 | gemini-3.6-flash-high / gemini | clarify | clarify | pass | pass | pass | pass | 5267eaff75c046a5bf25a30eca99dfed |
| SG23 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | b0a78c80605a4959a51971ae11ef63fc |
| SG24 | gemini-3.6-flash-high / gemini | answer | answer | pass | pass | pass | pass | 5dfc8bef9f324e44ab86e74e62bab809 |

## Phân tích của người chấm

Nhóm xác nhận 23 output còn lại đúng nội dung và pass các chiều áp dụng; SG02 fail vì timeout và vẫn nằm trong mẫu số.
