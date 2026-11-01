"""Score immutable supplied predictions against readings, never as Excel evidence."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
packet = root / 'packet'
readings = list((root / 'OxFunc-Evidence/readings').rglob('*.json'))
by_input = {}
for path in readings:
    doc = json.loads(path.read_text(encoding='utf-8-sig'))
    source = Path(doc['capture_provenance']['inputs']).resolve()
    by_input[source] = (path, doc)

summary = []
details = []
for path in sorted((packet / 'prior').rglob('*.jsonl')):
    if 'prediction' not in path.name:
        continue
    rows = [json.loads(line) for line in path.read_text().splitlines() if line]
    counts = dict(matched=0, mismatched=0, failed_or_missing=0)
    for row in rows:
        if 'calc_func_prediction' not in row:
            raise ValueError(f'Unsupported frozen prediction schema: {path}')
        candidates = [(source, p, d) for source, (p, d) in by_input.items()
                      if source.parent == path.parent and source.name.startswith('requests-')
                      and any(x['id'] == row['id'] for x in d['input_audits'])]
        if len(candidates) != 1:
            raise ValueError(f'Expected one batch for {path}:{row["id"]}')
        source, reading_path, doc = candidates[0]
        observed = next((x for x in doc['witnesses'] if x['id'] == row['id']), None)
        if observed is None:
            status = 'failed_or_missing'
        elif observed['args'] != row['args']:
            raise ValueError('Prediction input identity differs')
        else:
            status = 'matched' if observed['expected_bits'] == row['calc_func_prediction'] else 'mismatched'
        counts[status] += 1
        details.append(dict(prediction_file=str(path.relative_to(root)), id=row['id'],
                            requested_args=row['args'], prediction=row['calc_func_prediction'],
                            actual=observed['expected_bits'] if observed else None,
                            status=status, reading_file=str(reading_path.relative_to(root))))
    summary.append(dict(file=str(path.relative_to(root)), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                        total=len(rows), **counts))

totals = []
for source, (path, doc) in sorted(by_input.items()):
    request = json.loads(source.read_text())
    totals.append(dict(batch=str(source.relative_to(packet)), requested=len(request['witnesses']),
                       read=len(doc['witnesses']), unread=doc['unread'],
                       transport_audits=len(doc['transport_audit_readings']),
                       calculation_settings=doc['capture_provenance']['calculation_settings'],
                       environment=doc['capture_provenance']['environment']))
(root / 'prior-score.json').write_text(json.dumps(dict(predictions=summary, batches=totals,
    note='Scores supplied immutable prior predictions before any elimination. Predictions are not readings.'), indent=2))
(root / 'prior-score-rows.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in details))
print(json.dumps(summary, indent=2))
print('Batches:', len(totals), 'requested:', sum(x['requested'] for x in totals),
      'read:', sum(x['read'] for x in totals), 'unread:', sum(len(x['unread']) for x in totals))
