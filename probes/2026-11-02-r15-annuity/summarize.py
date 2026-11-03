"""Audit the unchanged R15 packet and score its frozen predictions before relations."""
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
import struct

root = Path(__file__).resolve().parent
packet = root / 'packet'
original = Path(r'C:\Work\DnaCalc\codex-runs\excel-questions-r15-annuity\round15-annuity')
manifest = json.loads((packet / 'manifest.json').read_text())
hashes = {}
for name, want in manifest['files_sha256'].items():
    data = (packet / name).read_bytes()
    assert data == (original / name).read_bytes(), name
    got = hashlib.sha256(data).hexdigest()
    assert got == want, (name, got, want)
    hashes[name] = got

counts, records, scored = [], {}, []
for batch in json.loads((packet / 'batches.json').read_text()):
    f = batch['function']
    requested = json.loads((packet / batch['path']).read_text())['witnesses']
    predictions = {r['id']: r for r in map(json.loads, (packet / f'application-predictions-{f}.jsonl').read_text().splitlines())}
    answers = list((root / 'OxFunc-Evidence/readings').glob(f'*/{f}.json'))
    assert len(answers) == 1, (f, answers)
    answer = json.loads(answers[0].read_text(encoding='utf-8-sig'))
    observed = {r['id']: r for r in answer['witnesses']}
    assert len(observed) == len(answer['witnesses'])
    assert set(observed) <= {r['id'] for r in requested}
    provenance = answer['capture_provenance']
    frozen = provenance['frozen_model_predictions']
    assert hashlib.sha256(Path(frozen['frozen_path']).read_bytes()).hexdigest() == frozen['frozen_sha256']
    assert hashlib.sha256(Path(frozen['inputs_path']).read_bytes()).hexdigest() == frozen['inputs_sha256']
    for req in requested:
        rid = req['id']
        assert predictions[rid]['args'] == req['args']
        row = observed.get(rid)
        if row:
            assert row['args'] == req['args']
            records[rid] = row
        scored.append(dict(id=rid, function=f, args=req['args'],
            packet_prediction=predictions[rid]['calc_func_prediction'],
            reader_prediction=row.get('calc_func_prediction') if row else None,
            excel=row['expected_bits'] if row else None,
            matched=bool(row and row['expected_bits'] == predictions[rid]['calc_func_prediction'])))
    counts.append(dict(function=f, requested=len(requested), read=len(observed), unread=answer['unread'],
        missing_ids=[r['id'] for r in requested if r['id'] not in observed],
        packet_prediction_matches=sum(r['matched'] for r in scored if r['function'] == f),
        reader_prediction_matches=sum(r['expected_bits'] == r['calc_func_prediction'] for r in observed.values()),
        settings=provenance['calculation_settings'], environment=provenance['environment'],
        automation_security_before=provenance['automation_security_before'],
        automation_security_after=provenance['automation_security_after']))

# Save prediction scores before inspecting any relation. These files are model output,
# not evidence of hidden Excel operands or a complete annuity implementation.
(root / 'prediction-scores.json').write_text(json.dumps(scored, indent=2) + '\n')
summary = dict(format='dnacalc-r15-reading-summary/1', requested=manifest['calls'],
    read=sum(c['read'] for c in counts),
    failed_read_obligations=sum(len(c['missing_ids']) for c in counts),
    unread_records=sum(len(c['unread']) for c in counts),
    frozen_packet_prediction_matches=sum(r['matched'] for r in scored),
    frozen_packet_prediction_nonpasses=sum(not r['matched'] for r in scored),
    functions=counts,
    limits='Direct numeric Value2 arguments with requested/submitted/read-back audits retained. Effective private callee inputs are not observable. Frozen predictions are never Excel answers.')
(root / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
(root / 'packet-sha256.json').write_text(json.dumps(hashes, indent=2) + '\n')
(root / 'path-relocations.json').write_text(json.dumps({'target/witness': str(root / 'worker')}, indent=2) + '\n')

def number(rid):
    text = records[rid]['expected_bits']
    assert text.startswith('0x') and len(text) == 18, (rid, text)
    return struct.unpack('>d', bytes.fromhex(text[2:]))[0]

def bits(value):
    return '0x' + struct.pack('>d', value).hex()

relations = []
for relation in json.loads((packet / 'conditional-relations.json').read_text()):
    r = dict(relation)
    ids = {k: v for k, v in r.items() if isinstance(v, str) and v.startswith('r15-')}
    r['observed_bits'] = {k: records[v]['expected_bits'] for k, v in ids.items() if v in records}
    missing = [v for v in ids.values() if v not in records]
    if missing:
        r.update(status='failed: missing Excel reading', missing=missing)
    elif r['kind'] == 'singleton surface audit':
        r.update(status='publications compared', principal_equal=number(r['CUMPRINC']) == number(r['PPMT']),
                 interest_equal=number(r['CUMIPMT']) == number(r['IPMT']),
                 principal_bits_equal=records[r['CUMPRINC']]['expected_bits'] == records[r['PPMT']]['expected_bits'],
                 interest_bits_equal=records[r['CUMIPMT']]['expected_bits'] == records[r['IPMT']]['expected_bits'])
    else:
        payment = Fraction(number(r['PMT']))
        if r['kind'] == 'published payment partition audit':
            principal, interest = number(r['PPMT']), number(r['IPMT'])
            count = 1
        else:
            assert r['kind'] == 'coupled payment/principal/interest preimages'
            principal, interest, count = number(r['CUMPRINC']), number(r['CUMIPMT']), r['count']
            r['preimage_status'] = 'No latent preimage solver or fixed precision/store profiles supplied in this packet; public residual only. No hidden helper or complete program inferred.'
        residual = count * payment - Fraction(principal) - Fraction(interest)
        r.update(status='publications compared', exact_rational_residual=str(residual),
                 exact_published_identity=residual == 0,
                 rounded_binary64_component_sum=bits(principal + interest),
                 rounded_binary64_payment_multiple=bits(float(count * payment)),
                 rounded_binary64_identity=(principal + interest) == float(count * payment))
    relations.append(r)
(root / 'conditional-relation-results.json').write_text(json.dumps(dict(
    kinds=dict(Counter(r['kind'] for r in relations)), relations=relations,
    limits='Finite public output checks only. Equal components or nonempty necessary domains never identify a complete program. A failed publication identity does not exclude shared unrounded components.'), indent=2) + '\n')
print(json.dumps({k: v for k, v in summary.items() if k != 'functions'}, indent=2))
print(json.dumps(dict(relation_counts=dict(Counter(r['kind'] for r in relations))), indent=2))
