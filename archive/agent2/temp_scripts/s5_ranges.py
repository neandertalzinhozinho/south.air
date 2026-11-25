import json
from pathlib import Path

F1 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1')
tab = json.loads(Path(r'D:\PROJETOS\shadowFILES\analysis\parameter_table.json').read_text(encoding='utf-8'))
c = [json.loads(l) for l in open(F1 / 's5_params_wrapperstub.jsonl', encoding='utf-8') if l.startswith('{')]
c = [e for e in c if e['event'] == 'parameter']
by = {p['name']: p for p in tab['parameters']}

def fnum(s):
    try:
        return float(s.replace(',', '.').replace(' ', ''))
    except Exception:
        return None

hit = miss = nota = 0
misses = []
for p in c:
    t = by.get(p['title'])
    if not t:
        continue
    lo = fnum(p['string_samples'][0]['text'])
    hi = fnum(p['string_samples'][-1]['text'])
    if lo is None or hi is None:
        nota += 1
        continue
    ok = abs(lo - t['minimum']) < 1e-6 and abs(hi - t['maximum']) < 1e-6
    if ok:
        hit += 1
    else:
        miss += 1
        if len(misses) < 15:
            misses.append((p['title'], t['minimum'], t['maximum'], lo, hi))
print(f'string endpoints vs table min/max: match {hit}, mismatch {miss}, non-numeric {nota}')
for m in misses:
    print('  ', m)

print('\n--- enum tables ---')
for key, table_name in (('band_shape', None), ('stereo_mode', None), ('quality', None)):
    pass
shape = [v['label'] for v in tab['validated_enum_tables']['band_shape']['values']]
ster = [v['label'] for v in tab['validated_enum_tables']['stereo_mode']['values']]
qual = [v['label'] for v in tab['validated_enum_tables']['quality']['values']]
chan = [v['label'] for v in tab['validated_enum_tables']['band_channels']['values']]
print('shape table', len(shape))
for p in c:
    if p['title'].endswith(' shape'):
        got = [s['text'] for s in p['string_samples']]
        print(f"  {p['title']}: match={got == shape}", '' if got == shape else got)
for p in c:
    if p['title'] == 'Stereo mode':
        got = [s['text'] for s in p['string_samples']]
        print(f"  Stereo mode: match={got == ster} {got}")
    if p['title'] == 'Quality':
        got = [s['text'] for s in p['string_samples']]
        print(f"  Quality: match={got == qual} {got}")
for p in c:
    if p['title'] == 'Band 1 channels':
        got = [s['text'] for s in p['string_samples']]
        print(f"  Band 1 channels ({p['stepCount']} steps): table has {len(chan)} entries; runtime={got}")
