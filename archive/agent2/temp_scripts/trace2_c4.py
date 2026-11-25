import re, struct
from pathlib import Path
from capstone import *
BASED=Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll')
dump=Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
dll=(BASED/'recovered_dsp_test.dll').read_bytes()
secs=[]
e=struct.unpack_from('<I',dll,0x3c)[0]; coff=e+4
nsec=struct.unpack_from('<H',dll,coff+2)[0]; optsz=struct.unpack_from('<H',dll,coff+16)[0]
st=coff+20+optsz
for i in range(nsec):
    s=st+40*i; name=dll[s:s+8].rstrip(b'\0').decode('latin1')
    vs,va,rs,ra=struct.unpack_from('<IIII',dll,s+8); secs.append((va,vs,ra))
def r2o(r):
    for va,vs,ra in secs:
        if va<=r<va+vs: return ra+(r-va)
    return None
def rd(r,n):
    o=r2o(r); return dll[o:o+n] if o is not None else b''

syms={}; byname={}
for line in (BASED/'recovered_dsp_test.map').read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*([0-9a-fA-F]{4}):([0-9a-fA-F]{8})\s+(\S+)\s+([0-9a-fA-F]{16})\s+\S+\s+(\S+)',line)
    if m:
        name=m.group(3); rva=int(m.group(4),16)-0x180000000; obj=m.group(5)
        byname.setdefault(name,[]).append((rva,obj))
        syms.setdefault(rva,[]).append((name,obj))
def stub(rva):
    b=rd(rva,6); return b[:6]==bytes.fromhex('0f57c033c0c3')
def copies(name):
    return byname.get(name,[])

md=Cs(CS_ARCH_X86,CS_MODE_64)

targets=[0x27be7b,0x27bb7f,0x27b823,0x27b4c7,0x27b18b,0x27ae52,0x27ab10,0x27a7b8,0x27a781,0x27a46c,0x27a150,0x279deb,0x279cd7,0x279cae,0x279c85,0x279c5c]
print('=== copias no mapa para cada alvo autentico (dump space) ===')
for t in targets:
    n='dump_%x'%t
    c=copies(n)
    print('%s  bytecode_dump=%s' % (n, dump[t:t+10].hex()))
    for rva,obj in c:
        print('   rva=0x%-9x obj=%-22s stub=%s bytes=%s' % (rva,obj,stub(rva),rd(rva,10).hex()))

# show exact bytes at dump target and compare with DLL copies of same size
print('\n=== comparacao bytes: dump vs copia nao-stub ===')
for t in targets[:12]:
    n='dump_%x'%t
    db=dump[t:t+16]
    for rva,obj in copies(n):
        if not stub(rva):
            bb=rd(rva,16)
            print('%s dump=%s | dll@0x%x %s equal=%s' % (n,db.hex(),rva,bb.hex(),db==bb))
