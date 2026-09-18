import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import SourceStore, retrieve, validate_request, validate_response


class SlideTests(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[3] / 'K4-3B-Day05-06-AI-Product-Hackathon/data/vlearn-pack/slides'

    def test_real_slides_preserve_page_citation_and_original_file(self):
        store = SourceStore(self.root, kind='slides')
        source = store.sources['slides-d1']
        self.assertEqual(source['page_count'], 29)
        page = store.segment('slides-d1', 'S01-013')
        self.assertEqual(page['page_number'], 13)
        self.assertIn('Token', page['text'])
        self.assertEqual(store.source_file('slides-d1'), self.root / 'd1-slide-hackathon.pdf')

    def test_slide_retrieval_and_request_do_not_use_transcript_ids(self):
        store = SourceStore(self.root, kind='slides')
        request = validate_request(dict(source_id='slides-d1', question='Token là gì?', selected_segment_ids=['S01-013']), store)
        rows = retrieve(store.sources['slides-d1']['segments'], request['question'], request['selected_segment_ids'])
        self.assertEqual(rows[0]['id'], 'S01-013')
        self.assertTrue(all(r['id'].startswith('S01-') for r in rows))
        with self.assertRaises(ValueError):
            validate_request(dict(source_id='slides-d1', question='Token?', selected_segment_ids=['S02-013']), store)
        with self.assertRaises(ValueError):
            store.source_file('../../.env')

    def test_inline_slide_citation_cannot_be_fabricated(self):
        with self.assertRaises(ValueError):
            validate_response(dict(action='answer', answer='Token [S01-999].', citations=['S01-013'], clarifying_question='', reason=''), ['S01-013'])

    def test_image_only_pdf_has_no_fake_text_grounding(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as directory:
            for name in ['d1-slide-hackathon.pdf', 'd2-slide-hackathon.pdf']:
                writer = PdfWriter(); writer.add_blank_page(width=200, height=100)
                writer.write(Path(directory) / name)
            with self.assertRaises(ValueError):
                SourceStore(directory, kind='slides')


if __name__ == '__main__':
    unittest.main()
