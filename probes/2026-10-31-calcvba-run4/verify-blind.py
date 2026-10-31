"""Validate raw worker answers and their standard witness-reading files; never open predictions."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def encode_argument(arg):
    if 'number' in arg:
        return '0x' + arg['number']
    if 'logical' in arg:
        return arg['logical']
    return arg['text']

def encode_result(value):
    if set(value) == {'number'}:
        assert len(value['number']) == 16
        int(value['number'], 16)
        return '0x' + value['number']
    if set(value) == {'error_code'}:
        return 'error:' + {2000:'Null', 2007:'Div0', 2015:'Value', 2023:'Ref', 2029:'Name', 2036:'Num', 2042:'NA', 2043:'GettingData'}[value['error_code']]
    raise AssertionError(f'unexpected result kind: {list(value)}')

manifest = json.loads((HERE/'blind-manifest.json').read_bytes())
for name, expected in manifest['worker_hashes'].items():
    assert digest(HERE/'reader'/name) == expected
summary = []
for packet in manifest['packets']:
    folder = HERE/packet['label']
    assert digest(folder/'request.json') == packet['request_sha256']
    request = json.loads((folder/'request.json').read_bytes())
    result = json.loads((folder/'result.json').read_bytes())
    assert result['fatal'] is None and result['failures'] == []
    assert result['automation_security_before'] == result['automation_security_after']
    assert result['format'] == 'dnacalc-witness-worker-result' and result['version'] == 1
    assert result['excel_machine'] == 'x86-64'
    assert len(result['rows']) == len(request['rows']) == packet['count']
    assert all(result[k] for k in ['excel_version', 'excel_build', 'excel_file_version', 'os_version', 'cpu'])
    isolation = (folder/'isolation.txt').read_text()
    assert 'excel: Exited' in isolation and 'done: true' in isolation and 'stderr: ""' in isolation
    rows, unread = [], []
    for asked, answer in zip(request['rows'], result['rows']):
        assert asked['id'] == answer['id']
        if answer['input_kept'] is not True:
            unread.append({'id': asked['id'], 'reason': 'Excel changed an input through Value2; raw result is not an answer to the requested tuple'})
            continue
        rows.append({'id': asked['id'], 'args': list(map(encode_argument, asked['args'])),
                     'expected_bits': encode_result(answer['value'])})
    path = REPO/'readings'/f"excel-{result['excel_build']}"/f"{packet['function']}-calcvba4.json"
    provenance = {
        'schema_version': 'dnacalc-witness-reading/1',
        'captured_utc': packet['result_completed_utc'],
        'capture_clock_note': 'raw worker result file completion time',
        'reader': 'calc-oracle-excel witness-worker/1 at DnaCalc b952767; existing run_isolated supervisor',
        'worker_sha256': manifest['worker_hashes'],
        'inputs': (folder/'request.json').relative_to(REPO).as_posix(),
        'inputs_sha256': packet['request_sha256'],
        'raw_result': (folder/'result.json').relative_to(REPO).as_posix(),
        'raw_result_sha256': digest(folder/'result.json'),
        'blind': True,
        'automation_security_before': result['automation_security_before'],
        'automation_security_after': result['automation_security_after'],
        'environment': {'excel_version': result['excel_version'], 'excel_build': result['excel_build'],
            'excel_file_version': result['excel_file_version'], 'excel_bitness': '64-bit',
            'platform': 'Windows', 'excel_operating_system': result['os_version'],
            'cpu_id': result['cpu'], 'excel_input_plumbing': 'cell_value2_bulk'},
    }
    doc = {'function': packet['function'], 'capture_provenance': provenance, 'witnesses': rows,
           'unread': unread}
    if '--write' in sys.argv and not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(doc, indent=2)+'\n', encoding='utf-8', newline='\n')
    existing = json.loads(path.read_bytes())
    if 'unread' not in existing and not unread:
        existing['unread'] = []
    assert existing == doc
    summary.append({'function': packet['function'], 'asked': packet['count'], 'valid': len(rows), 'unread': len(unread), 'changed': len(unread),
                    'excel_pid': result['excel_pid'], 'path': path.relative_to(REPO).as_posix()})
assert sum(p['asked'] for p in summary) == 541
assert sum(p['valid'] for p in summary) == 537
print(json.dumps(summary, indent=2))
