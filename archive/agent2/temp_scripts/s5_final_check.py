import json
import re
from pathlib import Path

F1 = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1')
TAB = Path(r'D:\PROJETOS\shadowFILES\analysis\parameter_table.json')
tab = json.loads(TAB.read_text(encoding='utf-8'))


def load(p):
    return [json.loads(l) for l in open(p, encoding='utf-8')
            if l.startswith('{') and '"parameter"' in l]


c = load(F1 / 's5_params_wrapperstub.jsonl')
o = load(F1 / 's5_params_oracle.jsonl')
print('c', len(c), 'o', len(o), 'equal jsonl payload:',
      [x for x in c] == [x for x in o])

def num(text):
    s = text.strip().lower()
    if not s:
        return None
    mult = 1.0
    if s.endswith('khz'):
        mult, s = 1000.0, s[:-3]
    elif s.endswith('hz'):
        mult, s = 1.0, s[:-2]
    elif s.endswith('db'):
        s = s[:-2]
    elif s.endswith('%'):
        s = s[:-1]
    elif s.endswith('x'):
        s = s[:-1]
    s = s.replace(',', '.').strip()
    if not re.fullmatch(r'[-+]?\d*\.?\d+(e[-+]?\d+)?', s):
        return None
    return float(s) * mult


by = {p['name']: p for p in tab['parameters']}
hit = miss = nota = 0
misses = []
for p in c:
    t = by.get(p['title'])
    if not t:
        continue
    lo = num(p['string_samples'][0]['text'])
    hi = num(p['string_samples'][-1]['text'])
    if lo is None or hi is None:
        nota += 1
        continue
    ok = abs(lo - t['minimum']) < 1e-6 and abs(hi - t['maximum']) < 1e-9 * max(1, abs(t['maximum']))
    ok = ok or (abs(lo - t['minimum']) <= 1e-6 and abs(hi - t['maximum']) <= 1e-3)
    if ok:
        hit += 1
    else:
        miss += 1
        misses.append((p['title'], t['minimum'], t['maximum'], lo, hi))
print(f'endpoint range check (suffix-parsed): match {hit} | mismatch {miss} | non-numeric {nota}')
for m in misses:
    print('  MISMATCH', m)

print('\n--- enumerations vs dump tables ---')
tabs = tab['validated_enum_tables']
shape = [v['label'] for v in tabs['band_shape']['values']]
ster = [v['label'] for v in tabs['stereo_mode']['values']]
qual = [v['label'] for v in tabs['quality']['values']]
chan = [v['label'] for v in tabs['band_channels']['values']]
for p in c:
    got = [s['text'] for s in p['string_samples']]
    if p['title'].endswith(' shape'):
        print(f"  {p['title']:14s} 8 values, match 0x1f77af0 => {got == shape}")
    elif p['title'] == 'Stereo mode':
        print(f"  Stereo mode    match 0x1f77ae0 => {got == ster}")
    elif p['title'] == 'Quality':
        print(f"  Quality        match table   => {got == qual} {got}")
    elif p['title'] == 'Band 1 channels':
        print(f"  Band 1 channels: runtime {len(got)} values vs table {len(chan)}; match={got == chan}")
        print('     runtime:', got)
        print('     table  :', chan)
    elif p['title'] == 'Program':
        print(f"  Program: {len(got)} values; first 6 = {got[:6]}")
