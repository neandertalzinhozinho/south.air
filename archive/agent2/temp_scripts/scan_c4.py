import struct, sys, re
from pathlib import Path

FILES = {
 'dump': r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin',
 'dll' : r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll',
}

# patterns to find (label, bytes)
pats = [
 ('QWORD -0x90 (70ff..ff)',        bytes.fromhex('70ffffffffffffff')),
 ('DWORD 0xffffff70',              bytes.fromhex('70ffffff')),
 ('mov r64,imm32 -0x90 (c7 c0/..)',None),  # special below
 ('movabs rax,-0x90',              bytes.fromhex('48b870ffffffffffffff')),
 ('sub r/m64,imm8 0x90 (48 83 /5)',None),  # special
 ('sub r/m64,imm32 0xffffff70',    bytes.fromhex('4881e870ffffff')),
 ('lea rax,[rax-0x90]',            bytes.fromhex('488d8070ffffff')),
]

def find_all(data, needle, cap=200):
    out=[]; start=0
    while True:
        i=data.find(needle,start)
        if i<0: break
        out.append(i); start=i+1
        if len(out)>=cap: break
    return out

for name,path in FILES.items():
    data=Path(path).read_bytes()
    print('==== %s size=0x%x ====' % (name,len(data)))
    for label,needle in pats:
        if needle is None: continue
        hits=find_all(data,needle)
        print('%-38s count=%d %s' % (label,len(hits),' '.join('0x%x'%h for h in hits[:40])))
    # special: sub r/m64,imm8 0x90  -> 48 83 ModRM(regfield=5) 90 ; list all 48 83 ?? 90
    sub_hits=find_all(data, bytes.fromhex('4883'), cap=10**9)
    sub90=[h for h in sub_hits if data[h+2] in range(0xE0,0xF8) and data[h+3]==0x90]
    print('%-38s count=%d %s' % ('sub r/m64,0x90 (48 83 e? 90)',len(sub90),' '.join('0x%x'%h for h in sub90[:60])))
    # special: mov r64,imm32 -0x90 -> 48 c7 c0..f8 70ffffff
    mov_hits=find_all(data, bytes.fromhex('48c7'), cap=10**9)
    mov90=[h for h in mov_hits if 0xC0<=data[h+2]<=0xFF and data[h+3:h+7]==bytes.fromhex('70ffffff')]
    print('%-38s count=%d %s' % ('mov r64,-0x90 (48 c7 c? 70ffffff)',len(mov90),' '.join('0x%x'%h for h in mov90[:60])))
    # count of raw 0x90 bytes (NOP / imm) for context
    print('raw byte 0x90 count = %d' % data.count(0x90))
