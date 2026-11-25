import re,struct
from pathlib import Path
import pefile
ROOT=Path(r'D:\PROJETOS\shadowFILES')
dump=(ROOT/'soothe3_unpacked_mem.bin').read_bytes()
pe=pefile.PE(str(ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
data=pe.__data__
CAP=0x18CC0000
targets=[0x18061d8b0,0x61d8b0,0x18061d895,0x18061563f,0x18061565f]
print('=== raw qword search in DLL (all alignments) ===')
for t in targets:
    needle=struct.pack('<Q',t)
    hits=[m.start() for m in re.finditer(re.escape(needle),data)]
    print(f'  {t:#x}: {len(hits)} hits',[hex(h) for h in hits[:20]])
print('\n=== raw qword search in dump: CAP+0x241426 etc (all alignments) ===')
for t in [0x241426,0x24144a,0x24144f,0x24140b,0x241471]:
    needle=struct.pack('<Q',CAP+t)
    hits=[m.start() for m in re.finditer(re.escape(needle),dump)]
    print(f'  CAP+{t:#x} = {CAP+t:#x}: {len(hits)} hits',[hex(h) for h in hits[:20]])
print('\n=== all qwords in dump with high dword 0x27 and low dword 3 (all alignments) ===')
needle=struct.pack('<Q',0x2700000003)
hits=[m.start() for m in re.finditer(re.escape(needle),dump)]
print(' exact 0x27000000003',len(hits),[hex(h) for h in hits[:20]])
# scan every byte offset for qwords whose high32 in 0x20..0x30 and low==3
res=[]
for off in range(0,len(dump)-8):
    v=struct.unpack_from('<Q',dump,off)[0]
    if (v&0xffffffff)==3 and 0x20<=(v>>32)<=0x30:
        res.append((off,v))
print(' low32==3 high32 0x20..0x30 (all alignments):',len(res))
for off,v in res[:60]: print(f'   dump@{off:#x} = {v:#x}')
