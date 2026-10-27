#!/usr/bin/env python3
"""Grade synthetic review report contracts, never app correctness or prose truth."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUBRICS = ROOT / 'evals' / 'rubrics.json'
STATUSES = {'verified', 'to do', 'needs device', 'not applicable'}


def grade(case, report):
    rubric = json.loads(RUBRICS.read_text())[case]
    problems = []
    if not isinstance(report, dict):
        return ['report must be an object']
    scope = report.get('scope', {})
    if not isinstance(scope, dict):
        return ['scope must be an object']
    for field in ('mode', 'framework', 'platforms', 'channels'):
        actual, expected = scope.get(field), rubric[field]
        if field == 'framework':
            equal = isinstance(actual, str) and bool(re.match(re.escape(expected) + r'\b', actual, re.I))
        elif field == 'channels':
            # Descriptive labels may add package details or reorder words.
            remaining = list(actual) if isinstance(actual, list) else []
            equal = len(remaining) == len(expected) and all(isinstance(v, str) for v in remaining)
            if equal:
                for channel in expected:
                    tokens = set(re.findall(r'\w+', channel.casefold()))
                    match = next((v for v in remaining if tokens <= set(re.findall(r'\w+', v.casefold()))), None)
                    if match is None:
                        equal = False
                        break
                    remaining.remove(match)
        elif isinstance(expected, list):
            equal = (isinstance(actual, list) and all(isinstance(v, str) for v in actual)
                     and sorted(actual) == sorted(expected))
        else:
            equal = actual == expected
        if not equal:
            problems.append(f'scope mismatch: {field}')
    for field in ('project', 'change'):
        if not isinstance(scope.get(field), str) or not scope[field].strip():
            problems.append(f'missing scope {field}')
    selected = report.get('selected_ids', [])
    if not isinstance(selected, list) or any(not isinstance(i, str) for i in selected):
        return problems + ['selected_ids must be a string array']
    known = json.loads(RUBRICS.read_text())['release-review']['required_ids']
    if len(selected) != len(set(selected)) or set(selected) - set(known):
        problems.append('unknown or duplicate selected ID')
    for ident in rubric['required_ids']:
        if ident not in selected:
            problems.append(f'missing required ID {ident}')
    if len(selected) > rubric['max_ids']:
        problems.append('too many IDs for change mode')
    refs = report.get('references_loaded', [])
    if not isinstance(refs, list) or any(not isinstance(r, str) for r in refs):
        return problems + ['references_loaded must be a string array']
    for ref in rubric['required_refs']:
        if f'references/{ref}.md' not in refs:
            problems.append(f'missing reference {ref}')
    if rubric['framework'] != 'Flutter' and 'references/flutter.md' in refs:
        problems.append('Flutter reference in non-Flutter case')
    for field in ('device_plan', 'release_blockers', 'limitations'):
        value = report.get(field)
        # Plans/blockers may be readable strings or structured records; semantic
        # completeness is assessed separately, not inferred from their encoding.
        def meaningful(v):
            return (isinstance(v, str) and bool(v.strip())) or (
                field != 'limitations' and isinstance(v, dict)
                and any(isinstance(s, str) and s.strip() for s in v.values()))
        if not isinstance(value, list) or not value or not all(meaningful(v) for v in value):
            problems.append(f'missing {field}')
    excluded = report.get('excluded_areas')
    if not isinstance(excluded, list) or any(not isinstance(v, dict) or not v.get('area') or not v.get('reason') for v in excluded):
        problems.append('invalid excluded_areas')
    rows = report.get('rows')
    if not isinstance(rows, list):
        return problems + ['rows must be an array']
    pairs = set()
    na = 0
    for row in rows:
        if not isinstance(row, dict):
            problems.append('row must be an object')
            continue
        ident, platform, status = row.get('id'), row.get('platform'), row.get('status')
        if not isinstance(ident, str) or not isinstance(platform, str):
            problems.append('row id/platform must be strings')
            continue
        pair = (ident, platform)
        if pair in pairs:
            problems.append(f'duplicate row {ident}/{platform}')
        pairs.add(pair)
        if ident not in selected or platform not in rubric['platforms']:
            problems.append(f'out-of-scope row {ident}/{platform}')
        if not isinstance(status, str) or status not in STATUSES:
            problems.append(f'invalid status {ident}/{platform}')
        if row.get('priority') not in ('P0', 'P1', 'P2'):
            problems.append(f'invalid priority {ident}/{platform}')
        for field in ('evidence', 'next_step'):
            if not isinstance(row.get(field), str) or not row[field].strip():
                problems.append(f'missing {field} {ident}/{platform}')
        if not isinstance(row.get('release_blocker'), bool) or not isinstance(row.get('reason'), str):
            problems.append(f'invalid blocker/reason {ident}/{platform}')
        if status == 'verified' and not rubric['verified_allowed']:
            problems.append(f'unsupported verified {ident}/{platform}')
        if status == 'not applicable':
            na += 1
            if not isinstance(row.get('reason'), str) or not row['reason'].strip():
                problems.append(f'N/A without reason {ident}/{platform}')
            if ident in rubric['must_apply']:
                problems.append(f'applicable item marked N/A {ident}/{platform}')
    for ident in selected:
        for platform in rubric['platforms']:
            if (ident, platform) not in pairs:
                problems.append(f'missing row {ident}/{platform}')
    # Also name omitted required pairs, even if their selected ID was omitted.
    for ident in rubric['required_ids']:
        for platform in rubric['platforms']:
            if (ident, platform) not in pairs and ident not in selected:
                problems.append(f'missing row {ident}/{platform}')
    if rows and na / len(rows) > rubric['max_na_fraction']:
        problems.append('excessive N/A')
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case', nargs='?', choices=json.loads(RUBRICS.read_text()))
    parser.add_argument('report', nargs='?', type=Path)
    parser.add_argument('--examples', action='store_true')
    args = parser.parse_args()
    if not args.examples and (args.case is None or args.report is None):
        parser.error('provide CASE REPORT.json or --examples')
    reports = [(case, ROOT / 'evals' / 'examples' / f'{case}.json') for case in json.loads(RUBRICS.read_text())] if args.examples else [(args.case, args.report)]
    count = 0
    for case, path in reports:
        try:
            problems = grade(case, json.loads(path.read_text()))
        except (OSError, ValueError) as error:
            problems = [str(error)]
        for problem in problems:
            print(f'{case}: {problem}')
        print(f'{case}: {len(problems)} contract problem(s)')
        count += len(problems)
    return int(count > 0)


if __name__ == '__main__':
    raise SystemExit(main())
