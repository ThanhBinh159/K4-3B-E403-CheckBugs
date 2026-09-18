import argparse
import csv
import json
import os
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'codebase'))
from core import SourceStore, retrieve, validate_request
from server import load_env


def main():
    load_env()
    cases = json.loads((ROOT / 'eval' / 'golden_set.json').read_text(encoding='utf-8'))
    assert len(cases) == 24 and len({c['case_id'] for c in cases}) == 24
    assert Counter(c['category'] for c in cases) == {'normal': 10, 'hard': 10, 'edge': 4}
    for layer in ['1', '2', '3', '4']:
        assert sum(c['category'] == 'hard' and c['difficulty_layer'] == layer for c in cases) >= 2
    assert sum(bool(c['turn_id']) for c in cases) >= 10
    data = Path(os.getenv('VLEARN_DATA_DIR', '../K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/transcript'))
    store = SourceStore(data if data.is_absolute() else ROOT / data)
    parser = argparse.ArgumentParser()
    parser.add_argument('--chatlog', type=Path)
    args = parser.parse_args()
    turns = None
    if args.chatlog:
        with args.chatlog.open(encoding='utf-8-sig') as stream:
            turns = {r['turn_id'] for r in csv.DictReader(stream)}
    lines = ['# Retrieval diagnostics - không phải chất lượng AI', '',
             'Chỉ kiểm tra có truy xuất ít nhất một mã đoạn hỗ trợ được thiết kế hay không. Không chấm claim/model output. Missing supporting ID là tín hiệu retrieval cần xem lại, không kết luận toàn file thiếu đáp án.', '',
             '| Case | Expected | Context IDs | Có ít nhất một supporting ID? |', '|---|---|---|---|']
    hit = eligible = 0
    for c in cases:
        validate_request(c, store)
        for sid in c['supporting_segment_ids']:
            store.segment(c['source_id'], sid)
        if turns is not None and c['turn_id']:
            assert c['turn_id'] in turns, c['case_id']
        context = retrieve(store.sources[c['source_id']]['segments'], c['question'], c['selected_segment_ids'])
        ids = [s['id'] for s in context]
        matched = bool(set(ids) & set(c['supporting_segment_ids']))
        if c['expected_action'] == 'answer':
            eligible += 1
            hit += matched
        lines.append('| ' + ' | '.join([c['case_id'], c['expected_action'], ', '.join(ids), str(matched) if c['expected_action'] == 'answer' else 'N/A']) + ' |')
    lines += ['', f'Trên {eligible} case expected answer: {hit} case có ít nhất một supporting ID trong context. Đây là phép đo retrieval local, không là grounded answer rate hoặc tỷ lệ CP3.', '']
    (ROOT / 'eval' / 'retrieval_diagnostics.md').write_text('\n'.join(lines), encoding='utf-8')
    print(f'Golden structure/source IDs OK: 24 cases, 12 derived cases. Retrieval supporting-ID overlap {hit}/{eligible} (not AI quality).')


if __name__ == '__main__':
    main()
