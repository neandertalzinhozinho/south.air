import json
from pathlib import Path

F1 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1')


def load(p):
    ev = [json.loads(l) for l in open(p, encoding='utf-8') if l.startswith('{')]
    return [e for e in ev if e['event'] == 'parameter']


c = load(F1 / 's5_params_wrapperstub.jsonl')
o = load(F1 / 's5_params_oracle.jsonl')
print('c', len(c), 'o', len(o))
fields = ('id', 'title', 'shortTitle', 'units', 'stepCount', 'defaultNormalizedValue',
          'unitId', 'flags', 'status', 'string_samples', 'string_status_nonzero',
          'plain_probes', 'set_0_375_status', 'readback_after_set')
diff = 0
for a, b in zip(c, o):
    for f in fields:
        if a[f] != b[f]:
            diff += 1
            if diff <= 12:
                print('DIFF', a['index'], a['title'], f, a[f], b[f])
print('field diffs:', diff)
print('nonzero string status total (cand):', sum(p['string_status_nonzero'] for p in c))

for t in ('Band 1 shape', 'Band 2 shape', 'Stereo mode', 'Quality', 'Program',
          'Band 1 channels', 'Band solo', 'Bypass', 'Depth'):
    p = next(x for x in c if x['title'] == t)
    print(f"{t:14s} idx={p['index']:3d} step={p['stepCount']:2d} flags=0x{p['flags']:X} "
          f"def={p['defaultNormalizedValue']:.6g}")
    print('   strings:', [s['text'] for s in p['string_samples']])
