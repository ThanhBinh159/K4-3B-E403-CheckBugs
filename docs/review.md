# Review trước bàn giao

Review đọc source độc lập, không có lượt provider live. Hai lỗi quan trọng được tái hiện bằng local fixture:

1. HTTP redirect có thể chuyển tiếp Authorization tới đích redirect. Adapter và script kiểm proxy hiện không theo redirect.
2. Server bind loopback nhưng chấp nhận Host bất kỳ. Mỗi GET/POST hiện chỉ chấp nhận localhost hoặc 127.0.0.1 với đúng port server; Origin dùng danh sách loopback cụ thể.

Test regression cả hai thất bại trước sửa và pass sau sửa. Sau lượt AI live nhận JSON bọc Markdown, thêm hai test parser (nhận đúng một khối JSON; từ chối prose ngoài khối), nâng tổng lên 27 test kỹ thuật. Không dùng các kết quả này thay chất lượng AI hoặc user validation. Vấn đề retrieval G06 đã được khai trong eval/retrieval_diagnostics.md và slide 5; chưa tuyên bố được sửa.
