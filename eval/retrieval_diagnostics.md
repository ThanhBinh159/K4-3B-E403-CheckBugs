# Retrieval diagnostics - không phải chất lượng AI

Chỉ kiểm tra có truy xuất ít nhất một mã đoạn hỗ trợ được thiết kế hay không. Không chấm claim/model output. Missing supporting ID là tín hiệu retrieval cần xem lại, không kết luận toàn file thiếu đáp án.

| Case | Expected | Context IDs | Có ít nhất một supporting ID? |
|---|---|---|---|
| G01 | answer | T04-049, T04-050, T04-051, T04-006, T04-096, T04-094 | True |
| G02 | answer | T04-051, T04-052, T04-053, T04-057, T04-074, T04-088 | True |
| G03 | answer | T04-040, T04-041, T04-054, T04-055, T04-056, T04-096 | True |
| G04 | answer | T06-086, T06-087, T06-160, T06-162, T06-130, T06-161 | True |
| G05 | answer | T04-016, T04-017, T04-032, T04-033, T04-015, T04-031 | True |
| G06 | answer | T04-046, T04-047, T04-090, T04-091, T04-087, T04-003 | True |
| G07 | answer | T04-032, T04-033, T04-015, T04-030, T04-031, T04-026 | True |
| G08 | answer | T06-051, T06-052, T06-079, T06-148, T06-040, T06-044 | True |
| G09 | answer | T04-046, T04-047, T04-032, T04-033, T04-015, T04-030 | True |
| G10 | answer | T04-096, T04-097, T04-050, T04-051, T04-072, T04-071 | True |
| G11 | no_grounding | T04-089, T04-090, T04-036, T04-037, T04-096, T04-001 | N/A |
| G12 | out_of_scope | T04-061, T04-062, T04-046, T04-047, T04-091, T04-020 | N/A |
| G13 | clarify | T04-052, T04-053, T04-023, T04-024, T04-054, T04-028 | N/A |
| G14 | clarify | T04-040, T04-041, T04-014, T04-015, T04-054, T04-029 | N/A |
| G15 | out_of_scope | T04-058, T04-059, T04-050, T04-051, T04-068, T04-077 | N/A |
| G16 | out_of_scope | T04-006, T04-007, T04-094, T04-095, T04-003, T04-011 | N/A |
| G17 | out_of_scope | T04-064, T04-065, T04-089, T04-090, T04-067, T04-072 | N/A |
| G18 | answer | T04-049, T04-050, T04-096, T04-029, T04-015, T04-055 | True |
| G19 | answer | T04-047, T04-072, T04-048, T04-071, T04-096, T04-049 | True |
| G20 | answer | T04-046, T04-047, T04-032, T04-033, T04-015, T04-063 | True |
| G21 | out_of_scope | T04-086, T04-087, T04-089, T04-090, T04-029, T04-054 | N/A |
| G22 | clarify | T04-052, T04-053, T04-051, T04-057, T04-074, T04-088 | N/A |
| G23 | answer | T04-049, T04-050, T04-051, T04-006, T04-096, T04-094 | True |
| G24 | answer | T04-051, T04-052, T04-064, T04-023, T04-054, T04-024 | True |

Trên 15 case expected answer: 15 case có ít nhất một supporting ID trong context. Đây là phép đo retrieval local, không là grounded answer rate hoặc tỷ lệ CP3.
