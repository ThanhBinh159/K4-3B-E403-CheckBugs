# Retrieval diagnostics - không phải chất lượng AI

Chỉ kiểm tra có truy xuất ít nhất một mã đoạn hỗ trợ được thiết kế hay không. Không chấm claim/model output. Missing supporting ID là tín hiệu retrieval cần xem lại, không kết luận toàn file thiếu đáp án.

| Case | Expected | Context IDs | Có ít nhất một trang hỗ trợ? | Đủ trang thiết kế? |
|---|---|---|---|---|
| SG01 | answer | S01-013, S01-014, S01-015, S01-016, S01-019, S01-012 | True | True |
| SG02 | answer | S01-016, S01-017, S01-014, S01-015, S01-020, S01-028 | True | True |
| SG03 | answer | S01-015, S01-016, S01-017, S01-028, S01-020, S01-023 | True | True |
| SG04 | answer | S02-003, S02-004, S02-002, S02-009, S02-027, S02-013 | True | True |
| SG05 | answer | S01-002, S01-003, S01-004, S01-015, S01-008, S01-007 | True | True |
| SG06 | answer | S01-002, S01-003, S01-004, S01-005, S01-012, S01-029 | True | True |
| SG07 | answer | S01-003, S01-004, S01-020, S01-016, S01-015, S01-023 | True | True |
| SG08 | answer | S01-004, S01-005, S01-026, S01-027, S01-008, S01-021 | True | True |
| SG09 | answer | S01-003, S01-004, S01-001, S01-010, S01-018, S01-014 | True | True |
| SG10 | answer | S01-029, S01-013, S01-014, S01-026, S01-006, S01-011 | True | True |
| SG11 | no_grounding | S01-017, S01-018, S01-022, S01-023, S01-028, S01-004 | N/A | N/A |
| SG12 | out_of_scope | S01-010, S01-011, S01-021, S01-022, S01-014, S01-028 | N/A | N/A |
| SG13 | clarify | S01-005, S01-006 | N/A | N/A |
| SG14 | clarify | S01-015, S01-016, S01-017, S01-014, S01-028, S01-018 | N/A | N/A |
| SG15 | out_of_scope | S01-014, S01-015, S01-028, S01-029, S01-006, S01-022 | N/A | N/A |
| SG16 | out_of_scope | S01-010, S01-011, S01-029, S01-015, S01-021, S01-014 | N/A | N/A |
| SG17 | out_of_scope | S01-026, S01-027, S01-010, S01-011, S01-019, S01-009 | N/A | N/A |
| SG18 | answer | S01-013, S01-014, S01-028, S01-020, S01-021, S01-029 | True | True |
| SG19 | answer | S01-011, S01-029, S01-012, S01-021, S01-019, S01-016 | True | True |
| SG20 | answer | S01-003, S01-004, S01-010, S01-008, S01-018, S01-012 | True | True |
| SG21 | out_of_scope | S01-007, S01-008, S01-020, S01-021, S01-023, S01-014 | N/A | N/A |
| SG22 | clarify | S01-016, S01-017, S01-014, S01-015, S01-020, S01-028 | N/A | N/A |
| SG23 | answer | S01-013, S01-014, S01-015, S01-016, S01-019, S01-012 | True | True |
| SG24 | answer | S01-014, S01-015, S01-029, S01-021, S01-005, S01-008 | True | True |

Trên 15 case expected answer: 15 case có ít nhất một supporting ID trong context. Đây là phép đo retrieval local, không là grounded answer rate hoặc tỷ lệ CP3.

15/15 case có đủ mọi trang hỗ trợ đã thiết kế. Citation tồn tại không chứng minh claim đúng.
