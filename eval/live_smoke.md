# Kiểm tra AI thật qua CLIProxyAPI

Provider protocol: Gemini native. Base URL: http://localhost:8317/v1beta.
Model alias thực gửi: gemini-3.6-flash-high. Key lấy từ .env local, không công khai.

Câu thử: “Token có luôn bằng một từ không?”; nguồn transcript-04, chọn T04-049.

Lượt đầu nhận output có JSON bọc Markdown nên parser cũ báo lỗi. Raw output được lưu local. Đã thêm parser chỉ nhận JSON thuần hoặc đúng một khối JSON hoàn chỉnh, vẫn kiểm schema/citation và không nhận prose ngoài khối. Hai regression test pass; không thay quality bar.

Lượt thử lại: action=answer; citations T04-049 và T04-050 đều thuộc context đã gửi; latency 14.246 ms. Trace ID d25bbfed52f548e286b13b3606720bd1, raw context/output ở logs/ local bị ignore. Không coi một lượt thử là tỷ lệ pass golden set hoặc kết quả chấm grounding bởi người thật.

Đây là kiểm tra backend/Tutor API thật, chưa là video UI hoặc biên nhận nộp CP3. Sau đó chạy bộ 24 golden case để đo action/citation và chuẩn bị người chấm grounding/UX/risk.
