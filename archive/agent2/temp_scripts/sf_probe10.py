import json,re,struct,importlib.util
from pathlib import Path
ROOT=Path(r'D:\PROJETOS\shadowFILES')
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
CAP=0x18CC0000;SPAN=0x82A5000;HI=CAP+SPAN;IB=0x180000000
MAPP=ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
syms={}
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        v=int(mm.group(2),16)
        if IB<=v<IB+0x10000000:syms[mm.group(1)]=v-IB
print('dump_24144a DLL RVA',hex(syms.get('dump_24144a',0)),' dump_24142b',hex(syms.get('dump_24142b',0)))
print('dump_24144a delta from dump_24140b:',hex(syms.get('dump_24144a',0)-syms['dump_24140b']))

# rebuild exact span table via builder
spec=importlib.util.spec_from_file_location('b',ROOT/'analysis/scripts/build_recovered_dsp_dll.py')
b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
defined,externs,objs=b.collect()
data=sorted(n for n,k in externs.items() if n not in defined and n not in b.C_EXTERNALS and k!='PROC')
spans,blobs=b.collect_symbol_spans(data)
starts=json.loads((ROOT/'analysis/recovered_native/testdll/extra_blob_starts.json').read_text())
extra=[s for s in sorted(starts)]
BLOB=0x400
print('spans',len(spans),'base blobs',len(blobs),'extra blobs',len(extra))

# solve for t such that lookup_addr(t) == IB+0x61d8b0
TARGET=IB+0x61d8b0
sols=[]
for s,e,addrname in spans:
    a=syms.get(addrname)
    if a is None:continue
    t=s+(TARGET-(IB+a))
    if s<=t<e and 0<=t<SPAN:
        sols.append((t,s,e,addrname,a,'span'))
for s in extra:
    # extra blob addr unknown from map; skip (we can get from extra_blobs.asm symbols)
    pass
# get extra addr from extra_blobs.h/asm map
for line in (ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map').read_text(encoding='latin-1').splitlines():
    mm=re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(xtra_[0-9a-f]+|xtra_zero)\s+([0-9a-fA-F]+)H?',line)
    if mm:
        a=int(mm.group(2),16)-IB
        s=0 if mm.group(1)=='xtra_zero' else int(mm.group(1)[5:],16)
        t=s+(TARGET-(IB+a))
        if s<=t<s+BLOB and 0<=t<SPAN: sols.append((t,s,s+BLOB,mm.group(1),a,'extra'))
print('\nsolutions t mapping to target:')
for sol in sols[:30]:print('  ',[hex(x) if isinstance(x,int) else x for x in sol])

print('\n=== qword existence in dump for each t ===')
for t,*_ in sols:
    v=CAP+t; needle=struct.pack('<Q',v)
    hits=[m.start() for m in re.finditer(re.escape(needle),dump)]
    print(f'  t={t:#x} v={v:#x} dump hits={len(hits)} {[hex(h) for h in hits[:6]]}')
