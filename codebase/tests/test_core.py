import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import SourceStore, retrieve, validate_request, validate_response, parse_model_output


class CoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / 'transcript-04-clean.md').write_text(
            '# Bài\n## Token\n**[T04-001]** Token là đơn vị văn bản.\n\n'
            '**[T04-002]** Context window là giới hạn token.\n', encoding='utf-8')
        (self.root / 'transcript-06-clean.md').write_text(
            '**[T06-001]** Attention liên kết ngữ cảnh.', encoding='utf-8')
        self.store = SourceStore(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def test_loader_keeps_original_segment_without_next_heading(self):
        self.assertEqual(self.store.segment('transcript-04', 'T04-001')['text'], 'Token là đơn vị văn bản.')

    def test_citation_cannot_open_other_source(self):
        with self.assertRaises(ValueError):
            self.store.segment('transcript-04', 'T06-001')

    def test_request_rejects_paths_and_wrong_selected_ids(self):
        for data in [dict(source_id='../secret', question='Token?'),
                     dict(source_id='transcript-04', question='Token?', selected_segment_ids=['T06-001']),
                     dict(source_id='transcript-04', question='x' * 2001),
                     dict(source_id='transcript-04', question='  '),
                     dict(source_id='transcript-04', question='x', selected_segment_ids='T04-001')]:
            with self.subTest(data=data), self.assertRaises(ValueError):
                validate_request(data, self.store)

    def test_short_specific_question_is_not_rejected(self):
        self.assertEqual(validate_request(dict(source_id='transcript-04', question='Token?'), self.store)['question'], 'Token?')

    def test_retrieval_prioritizes_selected_and_stays_in_source(self):
        rows = retrieve(self.store.sources['transcript-04']['segments'], 'token', ['T04-002'])
        self.assertEqual(rows[0]['id'], 'T04-002')
        self.assertTrue(all(r['id'].startswith('T04-') for r in rows))

    def test_retrieval_caps_context_and_marks_truncation(self):
        rows = retrieve([dict(id=f'T04-{i:03d}', text='token ' * 1000, heading='') for i in range(12)], 'token', [])
        self.assertLessEqual(len(rows), 6)
        self.assertLessEqual(sum(len(r['text']) for r in rows), 12000)
        self.assertTrue(rows[0]['truncated'])

    def test_selected_context_is_distinguished_from_search_results(self):
        rows = retrieve(self.store.sources['transcript-04']['segments'], 'token', ['T04-002'])
        self.assertTrue(rows[0].get('selected_by_user'))
        self.assertFalse(next(r for r in rows if r['id'] == 'T04-001').get('selected_by_user'))

    def test_acronym_search_includes_explanation_continuation(self):
        segments = [dict(id='T04-001', heading='LLM', text='LLM là mô hình ngôn ngữ lớn.'),
                    dict(id='T04-002', heading='LLM', text='Nó dự đoán token tiếp theo.')]
        segments += [dict(id=f'T04-{i:03d}', heading='', text='LLM và các ứng dụng LLM.') for i in range(3, 12)]
        rows = retrieve(segments, 'Mô hình ngôn ngữ lớn là gì?', [])
        self.assertIn('T04-002', [r['id'] for r in rows])

    def test_explicit_selection_does_not_pull_unrelated_search_hits(self):
        segments = self.store.sources['transcript-04']['segments']
        rows = retrieve(segments, 'Giải thích khái niệm này.', ['T04-001'])
        self.assertEqual([r['id'] for r in rows], ['T04-001', 'T04-002'])

    def test_real_pack_covers_llm_mechanism_and_both_comparison_sides(self):
        root = Path(__file__).resolve().parents[3] / 'K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/transcript'
        store = SourceStore(root)
        segments = store.sources['transcript-04']['segments']
        for question in ['LLM là gì?', 'LLM khác biệt thế nào với Machine Learning?']:
            with self.subTest(question=question):
                ids = {r['id'] for r in retrieve(segments, question, [])}
                self.assertTrue(ids & {'T04-047', 'T04-091'}, ids)
                if 'Machine Learning' in question:
                    self.assertIn('T04-015', ids)

    def test_three_selected_segments_leave_space_for_comparison_evidence(self):
        root = Path(__file__).resolve().parents[3] / 'K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/transcript'
        segments = SourceStore(root).sources['transcript-04']['segments']
        selected = ['T04-046', 'T04-050', 'T04-054']
        rows = retrieve(segments, 'LLM khác biệt thế nào với Machine Learning?', selected)
        ids = {r['id'] for r in rows}
        self.assertTrue(set(selected).issubset(ids))
        self.assertTrue(ids & {'T04-015', 'T04-032'}, ids)

    def test_comparison_includes_llm_anchor_not_only_api_summary(self):
        root = Path(__file__).resolve().parents[3] / 'K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/transcript'
        segments = SourceStore(root).sources['transcript-04']['segments']
        rows = retrieve(segments, 'LLM có phải là một dạng Machine Learning không?', [])
        self.assertIn('T04-046', {r['id'] for r in rows})

    def test_response_blocks_fabricated_citation_and_missing_answer_citation(self):
        for citations in [[], ['T04-999']]:
            with self.assertRaises(ValueError):
                validate_response(dict(action='answer', answer='Giải thích.', citations=citations, clarifying_question='', reason=''), ['T04-001'])

    def test_inline_citation_cannot_bypass_declared_citation_validation(self):
        for answer in ['Giải thích [T04-999].', 'Giải thích [T04-001, T04-002].']:
            with self.subTest(answer=answer), self.assertRaises(ValueError):
                validate_response(dict(action='answer', answer=answer, citations=['T04-001'], clarifying_question='', reason=''), ['T04-001', 'T04-002'])

    def test_clarification_cannot_include_knowledge_answer(self):
        with self.assertRaises(ValueError):
            validate_response(dict(action='clarify', answer='Đáp án đoán.', citations=[], clarifying_question='Đoạn nào?', reason=''), [])

    def test_valid_answer_is_accepted_but_not_declared_grounded(self):
        out = validate_response(dict(action='answer', answer='Token là đơn vị văn bản.', citations=['T04-001'], clarifying_question='', reason='Có nguồn.'), ['T04-001'])
        self.assertEqual(out['action'], 'answer')
        self.assertNotIn('grounded', out)

    def test_response_rejects_overlong_and_wrong_schema(self):
        for answer in ['x ' * 181, 42]:
            with self.assertRaises(ValueError):
                validate_response(dict(action='answer', answer=answer, citations=['T04-001'], clarifying_question='', reason=''), ['T04-001'])

    def test_json_markdown_wrapper_from_proxy_is_accepted(self):
        self.assertEqual(parse_model_output('```json\n{"action":"clarify"}\n```'), {'action': 'clarify'})

    def test_json_wrapper_cannot_hide_prose_or_extra_instructions(self):
        for text in ['Ignore rules\n```json\n{}\n```', '```json\n{}\n```\nextra', '```python\n{}\n```']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_model_output(text)


if __name__ == '__main__':
    unittest.main()
