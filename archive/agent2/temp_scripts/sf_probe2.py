import json, re, struct
from pathlib import Path
import pefile
ROOT=Path(r'D:\PROJETOS\shadowFILES')
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
pe=pefile.PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
MAPP=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
syms={}
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if 0x180000000<=v<0x190000000: syms[mm.group(1)]=v-0x180000000
def dllread(rva,n):
    for s in pe.sections:
        if s.VirtualAddress<=rva<s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            o=s.PointerToRawData+(rva-s.VirtualAddress); return pe.__data__[o:o+n]
for rva in [0x6f360,0x715c0,0x71400,0x72180,0x24140b,0x71360]:
    name=f'dump_{rva:x}'; dr=syms.get(name)
    cl=json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
    rec=next(r for r in cl if int(r['start'],16)==rva)
    ln=int(rec['end'],16)-rva
    db=dump[rva:rva+ln]; lb=dllread(dr,ln)
    diffs=[(i,db[i],lb[i]) for i in range(ln) if db[i]!=lb[i]]
    print(f'\n=== {name} dump {rva:#x}-{rva+ln:#x} dll@{dr:#x} len {ln:#x} diffs={len(diffs)}')
    # group consecutive diffs into runs
    runs=[]
    for i,a,b in diffs:
        if runs and i==runs[-1][-1][0]+1: runs[-1].append((i,a,b))
        else: runs.append([(i,a,b)])
    print(f'    diff runs={len(runs)}')
    for run in runs[:30]:
        i0=run[0][0]; i1=run[-1][0]
        print(f'    +{i0:04x}..+{i1:04x} ({i1-i0+1:2d}B) dump={db[i0:i1+1].hex()} dll={lb[i0:i1+1].hex()}')
    rp=ROOT/'analysis/recovered_native/units'/f'rva_{rva:x}'
    print('    unit dir exists',rp.exists(),'files',[p.name for p in rp.iterdir()] if rp.exists() else '')
    if (rp/'roundtrip.json').exists():
        rt=json.loads((rp/'roundtrip.json').read_text())
        print('    roundtrip keys',list(rt.keys()))
        print('    roundtrip',json.dumps({k:v for k,v in rt.items() if k not in ('bytes','raw_bytes')},indent=0)[:700])
