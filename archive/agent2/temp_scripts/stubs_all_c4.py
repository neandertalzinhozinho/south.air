import re,struct
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
    vs,va,rs,ra=struct.unpack_from('<IIII',dll,s+8); secs.append((name,va,vs,ra))
def r2o(r):
    for n,va,vs,ra in secs:
        if va<=r<va+vs: return ra+(r-va)
    return None
def rd(r,n):
    o=r2o(r); return dll[o:o+n] if o is not None else b''
def secname(r):
    for n,va,vs,ra in secs:
        if va<=r<va+vs: return n
    return '?'

byname={}; byrva={}
for line in (BASED/'recovered_dsp_test.map').read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*([0-9a-fA-F]{4}):([0-9a-fA-F]{8})\s+(\S+)\s+([0-9a-fA-F]{16})\s+\S+\s+(\S+)',line)
    if m:
        n=m.group(3); rva=int(m.group(4),16)-0x180000000; obj=m.group(5)
        byname[n]=rva; byrva[rva]=(n,obj)
STUB=bytes.fromhex('0f57c033c0c3')
stub_rvas=set()
for n,rva in byname.items():
    if n.startswith('dump_') and rd(rva,6)==STUB:
        stub_rvas.add(rva)
print('total stub RVAs in map:',len(stub_rvas))

# scan CODE sections for rel32 branches targeting stubs
md=Cs(CS_ARCH_X86,CS_MODE_64)
hits=[]
for name,va,vs,ra in secs:
    if name not in ('.text','R2TEXT'): continue
    code=rd(va,vs)
    # linear sweep from section start; may misalign but good coverage
    for ins in md.disasm(code, va):
        if ins.mnemonic in ('call','jmp') or ins.mnemonic.startswith('j'):
            op=ins.op_str
            if op.startswith('0x'):
                try: tgt=int(op,16)
                except: continue
                if tgt in stub_rvas:
                    hits.append((ins.address,name,ins.mnemonic,tgt,ins.bytes.hex()))
print('branches -> stubs (linear sweep):',len(hits))
from collections import Counter
print('by mnemonic:',Counter(h[2] for h in hits))
print('by section:',Counter(h[1] for h in hits))
# group by target symbol
c=Counter(byrva[h[3]][0] for h in hits)
print('top stub targets:',c.most_common(40))
for h in hits[:120]:
    print('site 0x%-9x %-7s %-4s -> 0x%x %s  bytes=%s' % (h[0],h[1],h[2],h[3],byrva[h[3]],h[4]))
