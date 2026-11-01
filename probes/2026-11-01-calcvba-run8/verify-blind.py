"""Verify round-10 input transport and answers without reading prediction files."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

def load(path):
    return json.loads(path.read_bytes())

def argument(value):
    if isinstance(value, bool):
        return {'logical': value}
    if isinstance(value, str) and value.startswith('0x'):
        return {'number': value[2:].lower()}
    assert isinstance(value, str)
    return {'text': value}

total = 0
for function, folder, packet_name, count, literals, changed in [
    ('PMT', 'pmt', 'requests-PMT.json', 64, 16, 14),
    ('NORM.S.DIST', 'norm-s-dist', 'requests-NORM.S.DIST-all.json', 24, 0, 0),
]:
    packet = load(HERE / 'packet' / packet_name)
    request = load(HERE / folder / 'request.json')
    result = load(HERE / folder / 'result.json')
    reading = load(REPO / 'readings' / 'excel-20527' / (function + '.json'))
    assert packet['function'] == request['function'] == reading['function'] == function
    assert len(packet['witnesses']) == len(request['rows']) == len(result['rows']) == count
    assert result['fatal'] is None and result['failures'] == []
    assert result['excel_pid'] in (15396, 50400) and result['excel_pid'] != 3144
    assert result['automation_security_before'] == result['automation_security_after'] == 1
    assert result['excel_machine'] == 'x86-64' and result['excel_build'] == '20527'
    assert len(reading['witnesses']) == count - literals
    assert reading['unread'] == []
    assert len(reading['transport_audit_readings']) == literals
    assert len(reading['input_audits']) == count
    assert sum(not r['input_kept'] for r in result['rows']) == changed
    semantic = {r['id']: r for r in reading['witnesses']}
    audit_rows = {r['id']: r for r in reading['transport_audit_readings']}
    for source, asked, answer in zip(packet['witnesses'], request['rows'], result['rows']):
        assert source['id'] == asked['id'] == answer['id']
        expected = [argument(a) for a in source['args']]
        assert asked['args'] == answer['input_audit']['requested'] == expected
        audit = answer['input_audit']
        transported = [({'text': ''.join(f'{ord(c):04x}' for c in a['text'])}
                        if 'text' in a else a) for a in expected]
        assert audit['submitted_value2'] == transported
        assert audit['formula'] == asked['formula']
        if source.get('input_transport') == 'formula_literals':
            retained = audit_rows[source['id']]
            assert retained['semantic_witness'] is False
            assert retained['input_audit'] == audit
            assert retained['observed_raw'] == answer['value']
            assert bool(retained['reading_failure']) == (not answer['input_kept'])
        else:
            assert answer['input_kept'] is True and audit['read_back'] == transported
            assert set(answer['value']) == {'number'}
            assert semantic[source['id']]['expected_bits'] == '0x' + answer['value']['number']
    settings = result['calculation_settings']
    assert settings['calculation'] == -4135 and settings['PrecisionAsDisplayed'] is False
    assert settings['Date1904'] is False and settings['CompatibilityVersion'] == 2
    assert reading['capture_provenance']['calculation_settings'] == settings
    total += count
assert total == 88
manifest = load(HERE / 'blind-manifest.json')
for name, digest in manifest['sha256'].items():
    assert 'prediction' not in name.lower() and 'frozen-model' not in name
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == digest, name
print('88/88 calls retained: 72 exact-input semantic readings; 16 literal transport audits, 14 changed-input obligations; no predictions inspected')
