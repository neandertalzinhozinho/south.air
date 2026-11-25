import json

p = json.load(open('analysis/recovered_native/dsp/params_dump.json', encoding='utf-8'))
print('params_dump type:', type(p).__name__)
if isinstance(p, list):
    print('len:', len(p))
    print('primeiro:', json.dumps(p[0], ensure_ascii=False)[:300] if p else None)
    print('ultimo:', json.dumps(p[-1], ensure_ascii=False)[:300] if p else None)
elif isinstance(p, dict):
    print('keys:', list(p.keys())[:10])
    for k in list(p.keys())[:2]:
        print(k, str(p[k])[:300])

t = json.load(open('analysis/parameter_table.json', encoding='utf-8'))
print('parameter_table type:', type(t).__name__)
if isinstance(t, dict):
    print('keys:', list(t.keys())[:10])
    for k in list(t.keys())[:3]:
        v = t[k]
        print(' ', k, type(v).__name__, len(v) if hasattr(v, '__len__') else v)
elif isinstance(t, list):
    print('len:', len(t))
