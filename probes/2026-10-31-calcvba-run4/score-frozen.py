"""Score the untouched round-3 predictions only after the blind answer commit."""
import csv
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
BLIND_COMMIT = '0df452ec'
CASES = [
    ('pmt', 'pmt-native.tsv', ['pre_identity_model', 'current_application']),
    ('pmt', 'pmt-software.tsv', ['pre_identity_model', 'current_application']),
    ('gamma-dist', 'gamma-dist.tsv', ['native_baseline_prediction_bits', 'native_candidate_A_prediction_bits', 'native_research_B_prediction_bits', 'mathematical_CR_prediction_bits']),
    ('binom-dist', 'binom-dist.tsv', ['baseline', 'tiny_compensated', 'tiny_control']),
    ('poisson-dist', 'poisson-dist.tsv', ['baseline', 'tiny_endpoint', 'u_scalar', 'u_pc64']),
]

def normalized(value):
    value = value.strip()
    errors = {'#NULL!':'Null', '#DIV/0!':'Div0', '#VALUE!':'Value', '#REF!':'Ref',
              '#NAME?':'Name', '#NUM!':'Num', '#N/A':'NA'}
    if value in errors:
        return 'error:' + errors[value]
    if value.startswith('0x'):
        return '0x' + value[2:].lower()
    if len(value) == 16 and all(c in '0123456789abcdefABCDEF' for c in value):
        return '0x' + value.lower()
    return value

def distance(a, b):
    if not a.startswith('0x') or not b.startswith('0x'):
        return None
    def ordered(s):
        bits = int(s[2:], 16)
        return (0xffffffffffffffff - bits) if bits & (1 << 63) else bits + (1 << 63)
    return abs(ordered(a) - ordered(b))

manifest = json.loads((HERE/'prediction-manifest.json').read_bytes())
for name, expected in manifest['files'].items():
    assert hashlib.sha256((HERE/'predictions'/name).read_bytes()).hexdigest() == expected

scores, details = [], []
for packet, file, columns in CASES:
    raw_path = (HERE/packet/'result.json').relative_to(REPO).as_posix()
    committed_raw = subprocess.check_output(['git', 'show', f'{BLIND_COMMIT}:{raw_path}'], cwd=REPO)
    assert committed_raw == (HERE/packet/'result.json').read_bytes()
    request = json.loads((HERE/packet/'request.json').read_bytes())
    result = json.loads(committed_raw)
    answers = {r['id']: r for r in result['rows']}
    predictions = list(csv.DictReader((HERE/'predictions'/file).open(encoding='utf-8', newline=''), delimiter='\t'))
    assert len(predictions) == len(request['rows'])
    assert {r['id'] for r in predictions} == set(answers)
    assert len({r['id'] for r in predictions}) == len(predictions)
    for column in columns:
        matches = mismatches = unread = worst = 0
        for row in predictions:
            answer = answers[row['id']]
            predicted = normalized(row[column])
            expected = None
            ulp = None
            if answer['input_kept']:
                v = answer['value']
                if 'number' in v:
                    expected = '0x' + v['number']
                elif 'error_code' in v:
                    expected = 'error:' + {2007:'Div0',2015:'Value',2036:'Num',2042:'NA'}[v['error_code']]
                else:
                    raise AssertionError(v)
                ulp = distance(expected, predicted)
                worst = max(worst, ulp or 0)
                if expected == predicted:
                    matches += 1
                    status = 'match'
                else:
                    mismatches += 1
                    status = 'mismatch'
            else:
                unread += 1
                status = 'input_changed'
            details.append({'packet':packet,'file':file,'column':column,'id':row['id'],
                            'prediction':predicted,'excel':expected or 'unread','status':status,'ulp':ulp if ulp is not None else 'NA'})
        scores.append({'function':request['function'],'file':file,'column':column,'asked':len(predictions),
                       'matched':matches,'mismatched':mismatches,'unread':unread,'failed':mismatches+unread,
                       'pass_rate':matches/len(predictions),'worst_numeric_ulp':worst})
summary = {'blind_answer_commit':BLIND_COMMIT,'targeted_sample':True,'scores':scores}
(HERE/'scores.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n')
with (HERE/'score-rows.tsv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(details[0]),delimiter='\t',lineterminator='\n')
    w.writeheader(); w.writerows(details)
print(json.dumps(summary,indent=2))
