import json, re, struct, bisect
from pathlib import Path
ROOT=Path(r'D:\PROJETOS\shadowFILES')
CL=json.loads((ROOT/'analysis/recovered_native/dsp/dependency_build.json').read_text())
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
CAP=0x18CC0000; HI=CAP+0x82A5000
UNITS=ROOT/'analysis/recovered_native/units'

print('=== closure end vs roundtrip end_exclusive (byte_identical passed) ===')
mis=[]
for r in CL:
    if not (r.get('byte_identical') and r.get('status')=='passed'): continue
    s=int(r['start'],16); e=int(r['end'],16)
    rt=UNITS/f'rva_{s:x}'/'roundtrip.json'
    if not rt.exists(): continue
    info=json.loads(rt.read_text())
    ee=int(info['end_exclusive'],16)
    if ee!=e:
        mis.append((s,e,ee,e-ee,info.get('source_bytes'),info.get('instruction_count'),r.get('assembler_output')))
print('mismatches',len(mis))
for m in mis[:60]:
    print(f'  {m[0]:#x}: closure_end={m[1]:#x} emitted_end={m[2]:#x} phantom={m[3]:#x}B src={m[4]} insns={m[5]} src="{m[6]}"')
print('  total phantom bytes',sum(m[3] for m in mis))

print('\n=== special targets ===')
for s,e,ee,*_ in mis:
    if s in (0x715c0,0x71360,0x24140b):
        print(f'  {s:#x} closure [{s:#x},{e:#x}) emitted [{s:#x},{ee:#x})')

print('\n=== search dump qwords with low32==3 & heap-ish high32 ===')
cnt=0
pat = re.compile(rb'')
# scan all 8-aligned positions (and every byte offset) for exact known values
for val in (0x24a00000003,0x27000000003,0x18cc00003,0x180000003):
    needle=struct.pack('<Q',val)
    hits=[m.start() for m in re.finditer(re.escape(needle),dump)]
    print(f'  exact {val:#x}: {len(hits)} hits', [hex(h) for h in hits[:20]])

# qwords with low dword 3 and high dword in 0x02000000..0x03000000 (heap-ish 0x2xxxxxxxxx)
hits=[]
for off in range(0,len(dump)-8,8):
    v=struct.unpack_from('<Q',dump,off)[0]
    if (v & 0xffffffff)==3 and 0x02000000 <= (v>>32) <= 0x03000000:
        hits.append((off,v))
print(f'  low32==3 & high32 in [0x2000000,0x3000000] (8-aligned): {len(hits)}')
for off,v in hits[:40]: print(f'    dump@{off:#x} = {v:#x}')

print('\n=== qwords in dump pointing to 0x241400..0x2414c0 (CAP based) ===')
for off in range(0,len(dump)-8,8):
    v=struct.unpack_from('<Q',dump,off)[0]
    if CAP+0x241400 <= v < CAP+0x2414c0:
        print(f'    dump@{off:#x} = {v:#x} -> orig {v-CAP:#x}')
