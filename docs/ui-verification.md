# UI hỏi bài theo slide

Giao diện mới: nền sáng/xanh, hai cột desktop và một cột mobile. Thanh 4 bước hiển thị chọn slide → đặt câu hỏi → nhận kết quả → đối chiếu nguồn. Danh sách trang có tìm kiếm không dấu, checkbox tối đa 3 trang và preview. Answer, clarify, no_grounding, out_of_scope có trạng thái/bước tiếp riêng; lỗi giữ input và nút thử lại. Citation mở chữ trích xuất và PDF đúng trang vật lý, có cảnh báo font lỗi. Thông tin model/latency/request nằm trong phần mở rộng; key không vào frontend.

## Kiểm tra ngày 18/09/2026

- Chrome headless desktop 1440px và mobile 390px: đã xem ảnh render.
- Kiểm bằng browser: thiếu nguồn/câu hỏi, giới hạn 3 trang, giữ lựa chọn khi lọc, preview/PDF thật, khóa input khi chờ, cả 4 action, lỗi/thử lại giữ input, đổi nguồn và không tràn ngang mobile. Phản hồi /api/ask trong bộ kiểm tra nhánh là fixture riêng trong tab test, không là evidence AI thật hoặc chất lượng.
- Một lượt UI riêng dùng API thật: “Token là gì?” → answer, alias gemini-3.6-flash-high, 17,1 giây, request b8249dfb004a4764a91c6e892b9a6312 → citation S01-013 mở PDF trang 13. Đã xem render của lượt này. Không đưa raw trace hoặc key lên Git.
- 45 test kỹ thuật backend/eval và JS syntax đạt. Review code UI không tìm thấy lỗi material còn lại.

Đã sửa lỗi fieldset có chiều rộng tối thiểu theo nội dung gây tràn danh sách trang. Bộ kiểm tra browser tái chạy đạt sau sửa. Render dùng textContent để không thực thi HTML từ nguồn/model; race tải nguồn và preview có version guard.

## Tái kiểm tra

Khởi động server tại http://127.0.0.1:8765, cần Node 24 và Chrome cài trên Windows:

```powershell
node tools/verify_ui.mjs
# Tùy chọn gọi thêm một lượt API thật, có thể phát sinh phí của provider:
node tools/verify_ui.mjs --live
```

Ảnh/profile browser test nằm trong tmp/ui-review (không commit). Test không sửa golden/results/review.csv và không cài fixture vào production. Nếu thay đổi UI, xem ảnh mới; fixture pass không thay kiểm API thật. Chưa quay video hoặc có user validation/điểm nội dung nhóm chấm. Chưa kiểm tất cả kích thước/browser hoặc accessibility bằng người dùng thật.
