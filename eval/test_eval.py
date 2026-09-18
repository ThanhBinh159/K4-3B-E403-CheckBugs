import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch
from run import export_report
from run import summarize, technical_metrics


class EvalTests(unittest.TestCase):
    def test_historical_transcript_export_preserves_primary_slide_report(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'eval').mkdir()
            primary = root / 'eval/run_results.md'; primary.write_text('primary slide report')
            run_dir = root / 'historical'; run_dir.mkdir()
            (run_dir / 'results.json').write_text(json.dumps([dict(case_id='G01', model='test', provider='test',
                source_id='transcript-04', expected='answer', actual='answer', status='validated', action_match=True,
                response={'citations':['T04-001']})]))
            (run_dir / 'review.csv').write_text('case_id,grounding,ux,risk,reviewer,notes\nG01,,,,,\n')
            with patch('run.ROOT', root):
                export_report(run_dir)
            self.assertEqual(primary.read_text(), 'primary slide report')
            self.assertTrue((root / 'eval/archive/transcript-run-results.md').is_file())

    def test_slide_export_does_not_overwrite_existing_transcript_results(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); (root / 'eval').mkdir()
            old = root / 'eval/run_results.md'; old.write_text('original transcript report')
            run_dir = root / 'trial'; run_dir.mkdir()
            (run_dir / 'results.json').write_text(json.dumps([dict(case_id='SL01', model='test', provider='test',
                source_id='slides-d1', expected='answer', actual='answer', status='validated', action_match=True,
                response={'citations':['S01-013']})]))
            (run_dir / 'review.csv').write_text('case_id,grounding,ux,risk,reviewer,notes\nSL01,,,,,\n')
            with patch('run.ROOT', root):
                export_report(run_dir)
            self.assertEqual(old.read_text(), 'original transcript report')
            self.assertTrue((root / 'eval/slide_run_results.md').is_file())

    def test_pending_human_reviews_never_become_quality_passes(self):
        summary = summarize([{'case_id': 'A', 'status': 'validated', 'action_match': True}], {})
        self.assertEqual(summary['pending'], 1)
        self.assertIsNone(summary['pass_rate'])

    def test_timeout_stays_in_denominator(self):
        summary = summarize([
            {'case_id': 'A', 'status': 'validated', 'action_match': True},
            {'case_id': 'B', 'status': 'error', 'action_match': False}],
            {'A': {'grounding': 'pass', 'ux': 'pass', 'risk': 'pass'}})
        self.assertEqual(summary['total'], 2)
        self.assertEqual(summary['pass'], 1)
        self.assertEqual(summary['fail'], 1)
        self.assertEqual(summary['pass_rate'], 50.0)

    def test_failing_claim_cannot_pass_with_valid_citation(self):
        summary = summarize([{'case_id': 'A', 'status': 'validated', 'action_match': True}],
                            {'A': {'grounding': 'fail', 'ux': 'pass', 'risk': 'pass'}})
        self.assertEqual(summary['pass'], 0)
        self.assertEqual(summary['fail'], 1)

    def test_action_metrics_include_api_failure_in_denominator(self):
        metrics = technical_metrics([
            {'status':'validated','action_match':True,'response':{'citations':['T04-001']}},
            {'status':'error','action_match':False}])
        self.assertEqual(metrics['action_correct'], 1)
        self.assertEqual(metrics['action_accuracy'], 50.0)
        self.assertEqual(metrics['displayed_citations'], 1)

    def test_zero_displayed_citations_is_not_reported_as_perfect(self):
        metrics = technical_metrics([{'status':'error','action_match':False}])
        self.assertIsNone(metrics['displayed_citation_validity'])


if __name__ == '__main__':
    unittest.main()
