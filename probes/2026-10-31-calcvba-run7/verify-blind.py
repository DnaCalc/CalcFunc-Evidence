"""Check the frozen requests against raw Excel readings. Never reads predictions."""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifest = json.loads((HERE / 'blind-manifest.json').read_bytes())
for name, expected in manifest['sha256'].items():
    assert digest(HERE / name) == expected, name
packet = json.loads((HERE / 'requests.json').read_bytes())
request = json.loads((HERE / 'poisson-dist/request.json').read_bytes())
result = json.loads((HERE / 'poisson-dist/result.json').read_bytes())
assert packet['function'] == request['function'] == 'POISSON.DIST'
assert len(packet['witnesses']) == len(request['rows']) == len(result['rows']) == 38
assert result['format'] == 'dnacalc-witness-worker-result' and result['version'] == 1
assert result['fatal'] is None and result['failures'] == []
assert result['automation_security_before'] == result['automation_security_after'] == 1
assert result['excel_machine'] == 'x86-64'
assert result['excel_pid'] == 32320 and result['excel_pid'] != 3144
isolation = (HERE / 'isolation.txt').read_text()
assert all(s in isolation for s in ['excel: Exited', 'done: true', 'stderr: ""', '32320'])
rows, typed = [], []
for source, asked, answer in zip(packet['witnesses'], request['rows'], result['rows']):
    assert source['id'] == asked['id'] == answer['id']
    assert asked['formula'] == '=POISSON.DIST(RC[1],RC[2],RC[3])'
    decoded = [a['logical'] if 'logical' in a else '0x' + a['number'] for a in asked['args']]
    assert decoded == source['args']
    # Worker Test-Kept requires System.Double with identical bits, or System.Boolean
    # with identical value. A changed type/value never becomes an answer.
    assert answer['input_kept'] is True
    assert set(answer['value']) == {'number'}
    bits = answer['value']['number']
    assert len(bits) == 16
    int(bits, 16)
    rows.append({'id': source['id'], 'args': source['args'], 'expected_bits': '0x' + bits})
    typed.append({'id': source['id'], 'argument_types': [
        'System.Boolean / VT_BOOL' if 'logical' in a else 'System.Double / VT_R8'
        for a in asked['args']], 'readback_type_and_bits_kept': True,
        'result_kind': 'number / binary64'})
assert sum(isinstance(r['args'][2], bool) for r in rows) == 19
doc = {
    'function': 'POISSON.DIST',
    'capture_provenance': {
        'schema_version': 'dnacalc-witness-reading/1',
        'captured_utc': manifest['captured_utc'],
        'reader': 'DnaCalc c62ffca1e48b61989e7b481f9243a44fb6576b50 calc-oracle-excel::read_witnesses; existing run_isolated supervisor',
        'inputs': 'probes/2026-10-31-calcvba-run7/requests.json',
        'inputs_sha256': manifest['sha256']['requests.json'],
        'raw_result': 'probes/2026-10-31-calcvba-run7/poisson-dist/result.json',
        'raw_result_sha256': manifest['sha256']['poisson-dist/result.json'],
        'blind': True,
        'automation_security_before': 1, 'automation_security_after': 1,
        'environment': {
            'excel_version': result['excel_version'], 'excel_build': result['excel_build'],
            'excel_file_version': result['excel_file_version'], 'excel_bitness': '64-bit',
            'platform': 'Windows', 'excel_operating_system': result['os_version'],
            'cpu_id': result['cpu'], 'excel_input_plumbing': 'cell_value2_bulk',
        },
    },
    'witnesses': rows, 'unread': [],
}
reading = REPO / 'readings/excel-20527/POISSON.DIST-calcvba7.json'
types = HERE / 'argument-types.json'
for path, content in [(reading, doc), (types, typed)]:
    if '--write' in sys.argv and not path.exists():
        path.write_text(json.dumps(content, indent=2) + '\n', encoding='utf-8', newline='\n')
    assert json.loads(path.read_bytes()) == content
print('38/38 exact-input blind Excel answers; 19 Boolean and 19 Double false flags; 0 unread; owned Excel exited')
