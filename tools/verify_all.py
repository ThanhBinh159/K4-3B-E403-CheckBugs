"""Offline checks only. Does not call a live provider."""
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
commands = [
    [sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'codebase/tests', '-v'],
    [sys.executable, '-X', 'utf8', '-m', 'unittest', 'discover', '-s', 'eval', '-p', 'test_eval.py', '-v'],
    ['node', '--check', 'codebase/web/app.js'],
    [sys.executable, '-X', 'utf8', 'tools/verify_golden.py'],
]


def main():
    total_tests = 0
    lines = ['# Kiểm tra kỹ thuật local', '',
             'Thời điểm kiểm tra UTC: ' + datetime.now(timezone.utc).isoformat(), '',
             'Không gọi provider live. Fixture HTTP/model chỉ nằm trong test; không là kết quả chất lượng CP3.', '',
             '| Lệnh | Exit code | Kết quả |', '|---|---|---|']
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
        output = result.stdout + result.stderr
        count = re.search(r'Ran (\d+) tests?', output)
        if count:
            total_tests += int(count[1])
        if result.returncode:
            print(output)
            sys.exit(result.returncode)
        summary = f'{count[1]} test passed' if count else ('JS syntax OK' if command[0] == 'node' else output.strip())
        display = ('python ' + ' '.join(command[1:])) if command[0] == sys.executable else ' '.join(command)
        lines.append('| ' + ' | '.join([display, str(result.returncode), summary.replace('|', '/')]) + ' |')
    lines += ['', f'Tổng {total_tests} test kỹ thuật pass. Kết quả model live báo riêng trong run_results.md; report này không chấm chất lượng AI, video hoặc user validation.', '',
              'Báo cáo này chỉ xác minh offline. Kiểm UI/browser và lượt AI thật riêng xem docs/ui-verification.md; lệnh này không xác minh lại browser hoặc PDF.', '']
    (ROOT / 'eval' / 'technical_results.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Offline verification OK: {total_tests} tests; JS syntax and golden source IDs valid.')


if __name__ == '__main__':
    main()
