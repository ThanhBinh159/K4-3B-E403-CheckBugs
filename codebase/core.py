"""Source-bound retrieval and structural validation. No model simulation."""
import math
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

SOURCE_FILES = {'transcript-04': 'transcript-04-clean.md', 'transcript-06': 'transcript-06-clean.md'}
SLIDE_FILES = {'slides-d1': 'd1-slide-hackathon.pdf', 'slides-d2': 'd2-slide-hackathon.pdf'}
STOP = set('la gi cua va trong mot cac cho co the nhu nao toi ban hay ve duoc voi nay khong nhung khi de bai hoc giai thich'.split())
RETRIEVAL_VERSION = 'bm25-concept-continuation-v3'
ALIASES = {'llm': ['large language model', 'mo hinh ngon ngu lon'],
           'ml': ['machine learning'], 'dl': ['deep learning'],
           'ai': ['artificial intelligence', 'tri tue nhan tao']}


def parse_model_output(output):
    """Accept plain JSON or one complete JSON Markdown fence; never hidden prose."""
    if not isinstance(output, str):
        raise ValueError('Output AI phải là chuỗi JSON.')
    text = output.strip()
    fence = re.fullmatch(r'```(?:json)?[ \t]*\r?\n([\s\S]*?)\r?\n```', text, re.I)
    return json.loads(fence[1] if fence else text)


class SourceStore:
    def __init__(self, root, kind='transcript'):
        self.sources = {}
        self.kind = kind
        self.files = {}
        if kind == 'slides':
            self.load_slides(root)
            return
        if kind != 'transcript':
            raise ValueError('VLEARN_SOURCE_KIND phải là transcript hoặc slides.')
        for source_id, filename in SOURCE_FILES.items():
            path = Path(root) / filename
            if not path.is_file():
                raise ValueError(f'Không tải được nguồn {filename}. Kiểm tra VLEARN_DATA_DIR.')
            content = path.read_text(encoding='utf-8-sig')
            matches = list(re.finditer(r'\*\*\[(T\d{2}-\d{3})\]\*\*\s*', content))
            segments = []
            for i, match in enumerate(matches):
                heading = re.findall(r'^#{1,3}\s+(.+)$', content[:match.start()], re.M)
                end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
                text = re.split(r'\n#{1,3}\s', content[match.end():end], maxsplit=1)[0].strip()
                if not match[1].startswith('T' + source_id[-2:] + '-'):
                    raise ValueError('Mã đoạn không thuộc file nguồn.')
                segments.append(dict(id=match[1], text=text, heading=heading[-1] if heading else ''))
            if not segments or len({s['id'] for s in segments}) != len(segments):
                raise ValueError(f'Nguồn {filename} thiếu mã đoạn hoặc có mã trùng.')
            self.sources[source_id] = dict(id=source_id, name=filename, segments=segments)

    def load_slides(self, root):
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ValueError('Cần cài pypdf: python -m pip install -r requirements.txt.') from None
        for source_id, filename in SLIDE_FILES.items():
            path = Path(root) / filename
            if not path.is_file():
                raise ValueError(f'Không tải được {filename}. Kiểm tra VLEARN_SLIDES_DIR.')
            try:
                reader = PdfReader(path)
                segments, blank = [], []
                for number, page in enumerate(reader.pages, 1):
                    text = (page.extract_text() or '').strip()
                    if not text:
                        blank.append(number)
                        continue
                    glyph_warning = bool(re.search(r'[\ue000-\uf8ff]', text))
                    text = re.sub(r'[\ue000-\uf8ff]', '\ufffd', text)
                    heading = next((line.strip() for line in text.splitlines() if line.strip()), '')[:160]
                    segments.append(dict(id=f'S{int(source_id[-1]):02d}-{number:03d}', text=text,
                                         heading=heading, page_number=number, extraction_warning=glyph_warning))
            except Exception:
                raise ValueError(f'Không đọc được PDF {filename}; kiểm tra file hoặc mật khẩu.') from None
            if not segments:
                raise ValueError(f'{filename} không có chữ trích xuất được; bản này chưa hỗ trợ OCR.')
            self.sources[source_id] = dict(id=source_id, name=filename, kind='slides', segments=segments,
                                           page_count=len(reader.pages), unindexed_pages=blank)
            self.files[source_id] = path

    def source_file(self, source_id):
        if source_id not in self.files:
            raise ValueError('Nguồn PDF không hợp lệ.')
        return self.files[source_id]

    def segment(self, source_id, segment_id):
        if source_id not in self.sources:
            raise ValueError('Nguồn không hợp lệ.')
        for segment in self.sources[source_id]['segments']:
            if segment['id'] == segment_id:
                return segment
        raise ValueError('Mã đoạn không thuộc nguồn đã chọn.')


def terms(text):
    normalized = unicodedata.normalize('NFD', text.casefold().replace('đ', 'd'))
    normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
    return [w for w in re.findall(r'[a-z0-9]+', normalized) if w not in STOP]


def retrieval_terms(text):
    words = terms(text)
    # Canonical concept tokens connect acronyms to full names, not to guessed facts.
    normalized = ' '.join(words)
    for acronym, names in ALIASES.items():
        if any(' '.join(terms(name)) in normalized for name in names):
            words.append(acronym)
    return words


def retrieve(segments, question, selected):
    query = set(retrieval_terms(question))
    counts = [Counter(retrieval_terms(s.get('heading', '') + ' ' + s['text'])) for s in segments]
    avg = sum(sum(c.values()) for c in counts) / max(1, len(counts))
    frequency = {w: sum(w in c for c in counts) for w in query}
    ranked = []
    for segment, count in zip(segments, counts):
        score = 0
        for word in query:
            n = count[word]
            if n:
                idf = math.log(1 + (len(segments) - frequency[word] + .5) / (frequency[word] + .5))
                score += idf * n * 2.2 / (n + 1.2 * (.25 + .75 * sum(count.values()) / max(avg, 1)))
        ranked.append((score, segment))
    by_id = {s['id']: s for s in segments}
    hits = [s for score, s in sorted(ranked, key=lambda x: x[0], reverse=True) if score > 0 and s['id'] not in selected]
    ordered = [by_id[sid] for sid in selected]
    positions = {s['id']: i for i, s in enumerate(segments)}
    # Reserve space for continuations: transcripts often define a concept in the next segment.
    seeds = list(ordered)
    if not selected:
        # A comparison needs evidence for each named concept, not just the most frequent one.
        for concept in sorted(query & ALIASES.keys()):
            candidates = [(count[concept] / (count[concept] + 1.2 * (.25 + .75 * sum(count.values()) / max(avg, 1))), segment)
                          for count, segment in zip(counts, segments) if count[concept]]
            if candidates:
                # Named section headings identify conceptual explanations better than short API mentions.
                preferred = [(score, s) for score, s in candidates
                             if any(' '.join(terms(name)) in ' '.join(terms(s.get('heading', '')))
                                    for name in ALIASES[concept])]
                if len(query & ALIASES.keys()) == 1 and not preferred:
                    continue
                candidates = preferred or candidates
                seed = max(candidates, key=lambda x: x[0])[1]
                if seed not in seeds:
                    seeds.append(seed)
        if len(query & ALIASES.keys()) == 1:
            seeds += [s for s in hits if s not in seeds][:2 - len(seeds)]
        seeds = seeds[:2]
        seeds = seeds or hits[:2]
    neighbors_added = 0
    neighbor_limit = 1 if selected else 2
    for seed in list(seeds):
        if seed not in ordered:
            ordered.append(seed)
        index = positions[seed['id']] + 1
        if index < len(segments) and neighbors_added < neighbor_limit:
            neighbor = segments[index]
            if neighbor not in ordered:
                ordered.append(neighbor)
                neighbors_added += 1
    ordered += [s for s in hits if s not in ordered]
    context, budget = [], 12000
    for segment in ordered[:6]:
        if budget <= 0:
            break
        text = segment['text'][:min(3000, budget)]
        context.append(dict(segment, text=text, truncated=len(text) < len(segment['text']),
                            selected_by_user=segment['id'] in selected))
        budget -= len(text)
    return context


def validate_request(data, store):
    if not isinstance(data, dict):
        raise ValueError('Request phải là JSON object.')
    source_id, question = data.get('source_id'), data.get('question')
    if not isinstance(source_id, str) or source_id not in store.sources:
        raise ValueError('Hãy chọn một nguồn hợp lệ.')
    if not isinstance(question, str) or not question.strip() or len(question) > 2000:
        raise ValueError('Câu hỏi cần 1-2.000 ký tự.')
    selected = data.get('selected_segment_ids', [])
    if not isinstance(selected, list) or len(selected) > 3 or any(not isinstance(x, str) for x in selected):
        raise ValueError('Chọn tối đa 3 mã đoạn.')
    if len(set(selected)) != len(selected):
        raise ValueError('Mã đoạn được chọn bị trùng.')
    for sid in selected:
        store.segment(source_id, sid)
    return dict(source_id=source_id, question=question.strip(), selected_segment_ids=selected)


def validate_response(data, context_ids):
    keys = {'action', 'answer', 'citations', 'clarifying_question', 'reason'}
    if not isinstance(data, dict) or set(data) != keys:
        raise ValueError('AI trả JSON thiếu trường hoặc có trường không hợp lệ.')
    if any(not isinstance(data[k], str) for k in keys - {'citations'}):
        raise ValueError('Các trường văn bản phải là chuỗi.')
    if data['action'] not in {'answer', 'clarify', 'no_grounding', 'out_of_scope'}:
        raise ValueError('Action không hợp lệ.')
    citations = data['citations']
    if not isinstance(citations, list) or any(not isinstance(s, str) or s not in context_ids for s in citations):
        raise ValueError('Không xác minh được citation trong context đã gửi.')
    if len(set(citations)) != len(citations):
        raise ValueError('Citation trùng lặp.')
    if data['action'] == 'answer':
        if not data['answer'].strip() or not citations or len(data['answer'].split()) > 180 or data['clarifying_question'].strip():
            raise ValueError('Answer cần nội dung tối đa 180 từ, citation và không có câu hỏi làm rõ.')
        inline_ids = set(re.findall(r'\b[TS]\d{2}-\d{3}\b', data['answer']))
        if not inline_ids.issubset(set(citations)):
            raise ValueError('Citation trong câu trả lời không khớp danh sách citation đã xác minh.')
    else:
        if data['answer'].strip() or citations:
            raise ValueError('Action không trả lời phải để answer/citations rỗng.')
        if data['action'] == 'clarify' and not data['clarifying_question'].strip():
            raise ValueError('Thiếu câu hỏi làm rõ.')
        if data['action'] != 'clarify' and not data['reason'].strip():
            raise ValueError('Cần nêu giới hạn và bước tiếp theo.')
    return data
