# Kiểm tra kỹ thuật local

Thời điểm kiểm tra UTC: 2026-09-18T09:03:06.182361+00:00

Không gọi provider live. Fixture HTTP/model chỉ nằm trong test; không là kết quả chất lượng CP3.

| Lệnh | Exit code | Kết quả |
|---|---|---|
| python -X utf8 -m unittest discover -s codebase/tests -v | 0 | 38 test passed |
| python -X utf8 -m unittest discover -s eval -p test_eval.py -v | 0 | 7 test passed |
| node --check codebase/web/app.js | 0 | JS syntax OK |
| python -X utf8 tools/verify_golden.py | 0 | Slide golden set OK: 24 cases, 12 derived cases. Retrieval any 15/15, complete 15/15 (not AI quality). |

Tổng 45 test kỹ thuật pass. Kết quả model live báo riêng trong run_results.md; report này không chấm chất lượng AI, video hoặc user validation.

Báo cáo này chỉ xác minh offline. Kiểm UI/browser và lượt AI thật riêng xem docs/ui-verification.md; lệnh này không xác minh lại browser hoặc PDF.
