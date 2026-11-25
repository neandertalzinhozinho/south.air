import json
from pathlib import Path
ROOT = Path(r'D:\PROJETOS\shadowFILES')
closure = json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
h = lambda x: int(x,16) if isinstance(x,str) else int(x)
bad = []
ok = 0
nom = 0
for rec in closure:
    s = h(rec['start']); e = h(rec['end'])
    m = ROOT/'analysis/recovered_native/units'/f'rva_{s:x}'/'roundtrip.json'
    if not m.exists():
        nom += 1
        continue
    info = json.loads(m.read_text())
    ue = h(info['end_exclusive'])
    if ue != e:
        bad.append((s,e,ue,e-ue,rec.get('assembler_output','')))
    else:
        ok += 1
print('closure records', len(closure), 'matching', ok, 'no manifest', nom, 'MISMATCH', len(bad))
print('\nMismatches (start, closure_end, unit_end, missing_bytes, origin):')
for row in sorted(bad):
    print(f'  0x{row[0]:06x} closure_end=0x{row[1]:06x} unit_end=0x{row[2]:06x} missing={row[3]:5d}  {row[4]}')
