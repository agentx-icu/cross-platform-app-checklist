"""Contract examples and deliberately invalid review reports; no agent is run."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent


class ReviewContractTest(unittest.TestCase):
    def grade(self, case, mutate=None):
        data = json.loads((ROOT / 'evals' / 'examples' / f'{case}.json').read_text())
        if mutate:
            mutate(data)
        with tempfile.TemporaryDirectory(prefix='review-contract-') as temp:
            report = Path(temp) / 'report.json'
            report.write_text(json.dumps(data))
            return subprocess.run([sys.executable, str(ROOT / 'tools' / 'evaluate_review.py'), case, str(report)], text=True, capture_output=True)

    def test_three_positive_contract_examples(self):
        for case in ('flutter-change', 'electron-change', 'release-review'):
            with self.subTest(case=case):
                result = self.grade(case)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def reject(self, case, mutate, message):
        result = self.grade(case, mutate)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)

    def test_missing_release_item(self):
        self.reject('release-review', lambda d: d['selected_ids'].remove('X9'), 'missing required ID X9')

    def test_missing_shared_platform(self):
        self.reject('flutter-change', lambda d: d.update(rows=[r for r in d['rows'] if r['platform'] != 'Windows']), 'missing row L2/Windows')

    def test_fabricated_verified(self):
        self.reject('flutter-change', lambda d: d['rows'][0].update(status='verified', evidence='All device tests passed'), 'unsupported verified')

    def test_applicable_item_cannot_be_na(self):
        self.reject('electron-change', lambda d: d['rows'][0].update(status='not applicable', reason='desktop only'), 'applicable item marked N/A')

    def test_excessive_na(self):
        def mutate(d):
            for row in d['rows']:
                row.update(status='not applicable', reason='Not checked')
        self.reject('release-review', mutate, 'excessive N/A')

    def test_full_sweep_in_daily_mode(self):
        all_ids = json.loads((ROOT / 'evals' / 'rubrics.json').read_text())['release-review']['required_ids']
        self.reject('flutter-change', lambda d: d.update(selected_ids=all_ids), 'too many IDs for change mode')

    def test_flutter_reference_in_non_flutter_case(self):
        self.reject('electron-change', lambda d: d['references_loaded'].append('references/flutter.md'), 'Flutter reference in non-Flutter case')

    def test_missing_device_plan(self):
        self.reject('flutter-change', lambda d: d.update(device_plan=[]), 'missing device_plan')

    def test_structured_device_plan_is_accepted(self):
        result = self.grade('flutter-change', lambda d: d.update(device_plan=[{
            'platform': 'Android', 'scenario': 'Disconnect headset while recording',
            'expected': 'Recorder reports route change and retains draft',
        }]))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_release_blockers(self):
        self.reject('release-review', lambda d: d.update(release_blockers=[]), 'missing release_blockers')

    def test_invalid_report_shape(self):
        self.reject('release-review', lambda d: d.update(rows='bad'), 'rows must be an array')

    def test_duplicate_padding_cannot_hide_excessive_na(self):
        def mutate(d):
            must_apply = json.loads((ROOT / 'evals' / 'rubrics.json').read_text())['release-review']['must_apply']
            for row in d['rows']:
                if row['id'] not in must_apply:
                    row.update(status='not applicable', reason='Not checked')
            d['rows'].extend([dict(d['rows'][-1])] * 500)
        self.reject('release-review', mutate, 'duplicate row')

    def test_malformed_status_is_reported(self):
        self.reject('flutter-change', lambda d: d['rows'][0].update(status=[]), 'invalid status')

    def test_malformed_na_reason_is_reported(self):
        self.reject('flutter-change', lambda d: d['rows'][0].update(status='not applicable', reason=123), 'invalid blocker/reason')

    def test_malformed_platform_array_is_reported(self):
        self.reject('flutter-change', lambda d: d['scope'].update(platforms=['Android', 123]), 'scope mismatch')

    def test_descriptive_scope_labels_are_accepted(self):
        result = self.grade('electron-change', lambda d: d['scope'].update(
            framework='Electron; exact version unknown',
            channels=['Windows direct MSI', 'Linux Flathub (Flatpak)']))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
