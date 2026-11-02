import json, hashlib, pathlib
root=pathlib.Path(r'C:\Work\DnaCalc\codex-runs\excel-results-r14-variance')
packet=root/'packet'
manifest=json.loads((packet/'manifest.json').read_text())
hashes={}
for name, want in manifest['files'].items():
    got=hashlib.sha256((packet/name).read_bytes()).hexdigest()
    assert got==want,(name,got,want)
for src in pathlib.Path(r'C:\Work\DnaCalc\codex-runs\excel-questions-r14-variance').iterdir():
    assert src.read_bytes()==(packet/src.name).read_bytes(),src.name
    hashes[src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
counts=[]
for f in ['VAR.S','VAR.P','STDEV.S','STDEV.P','DEVSQ','AVERAGE']:
    requested=json.loads((packet/f'requests-{f}.json').read_text())['witnesses']
    answer=json.loads((root/'OxFunc-Evidence/readings/excel-20527'/f'{f}.json').read_text())
    observed={r['id']:r for r in answer['witnesses']}
    assert len(observed)==len(answer['witnesses'])
    for req in requested:
        if req['id'] in observed: assert req['args']==observed[req['id']]['args']
    provenance=answer['capture_provenance']
    frozen=provenance['frozen_model_predictions']
    fp=pathlib.Path(frozen['frozen_path'])
    assert hashlib.sha256(fp.read_bytes()).hexdigest()==frozen['frozen_sha256']
    assert hashlib.sha256(pathlib.Path(frozen['inputs_path']).read_bytes()).hexdigest()==frozen['inputs_sha256']
    count={'function':f,'requested':len(requested),'read':len(observed),'unread':answer['unread'],'missing_ids':[r['id'] for r in requested if r['id'] not in observed],
      'frozen_product_matches':sum(r['expected_bits']==r['calc_func_prediction'] for r in observed.values()),'settings':provenance['calculation_settings'],'environment':provenance['environment'],
      'automation_security_before':provenance['automation_security_before'],'automation_security_after':provenance['automation_security_after']}
    counts.append(count)
summary={'format':'dnacalc-r14-reading-summary/1','requested':44,'read':sum(c['read'] for c in counts),'failed_read_obligations':sum(len(c['unread'])+len(c['missing_ids']) for c in counts),
 'frozen_product_matches':sum(c['frozen_product_matches'] for c in counts),'functions':counts,'limits':'Direct numeric Value2 arguments; original array surface and private callee operands are not asserted. Predictions and mathematical controls are not Excel readings.'}
(root/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(root/'packet-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
(root/'path-relocations.json').write_text(json.dumps({'target/witness':str(root/'worker')},indent=2)+'\n')
print(json.dumps(summary,indent=2))
