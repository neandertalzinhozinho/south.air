import json
from pathlib import Path
ROOT = Path(r'D:\PROJETOS\shadowFILES')
CL = ROOT/'analysis/recovered_native/dsp/dependency_build.json'
d = json.loads(CL.read_text())
tgt = [0x6f360,0x715c0,0x24140b,0x71360,0x71400,0x72180,0x6ff80,0x7002e]
print('=== exact-start records ===')
for rec in d:
    s=int(rec['start'],16)
    if s in tgt:
        print(json.dumps(rec, indent=1))
        print('-'*70)
print('=== records CONTAINING target rva ===')
for t in tgt:
    hits=[r for r in d if int(r['start'],16)<=t<int(r['end'],16)]
    print(f'{t:#x}: {len(hits)} covering')
    for r in hits[:4]:
        print('   ',r['start'],r['end'],'bid',r.get('byte_identical'),'status',r.get('status'),
              'ext',r.get('external_count'),'unwind',len(r.get('unwind_records',[])))
print('=== schema of unwind_records (first nonempty) ===')
for r in d:
    u=r.get('unwind_records')
    if u:
        print(json.dumps(u,indent=1)[:1500])
        print('rec start',r['start'])
        break
