import re, struct
from pathlib import Path
from capstone import *

BASED = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll')
dump  = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
dll   = (BASED/'recovered_dsp_test.dll').read_bytes()

# --- PE section map RVA->fileoff
sections=[]
e=struct.unpack_from('<I',dll,0x3c)[0]; coff=e+4
nsec=struct.unpack_from('<H',dll,coff+2)[0]; optsz=struct.unpack_from('<H',dll,coff+16)[0]
opt=coff+20; st=opt+optsz
for i in range(nsec):
    s=st+40*i
    name=dll[s:s+8].rstrip(b'\0').decode('latin1')
    vsize,vaddr,rsize,raddr=struct.unpack_from('<IIII',dll,s+8)
    sections.append((name,vaddr,vsize,raddr,rsize))
def rva2off(r):
    for name,va,vs,ra,rs in sections:
        if va<=r<va+vs: return ra+(r-va)
    return None
def off2rva(o):
    for name,va,vs,ra,rs in sections:
        if ra<=o<ra+rs: return va+(o-ra)
    return None

# --- map
syms={}   # name -> (rva,obj)
byrva={}  # rva -> (name,obj)
for line in (BASED/'recovered_dsp_test.map').read_text(encoding='latin-1').splitlines():
    m=re.match(r'\s*([0-9a-fA-F]{4}):([0-9a-fA-F]{8})\s+(\S+)\s+([0-9a-fA-F]{16})\s+\S+\s+(\S+)',line)
    if m:
        sec=int(m.group(1),16); off=int(m.group(2),16); name=m.group(3); absaddr=int(m.group(4),16); obj=m.group(5)
        rva=absaddr-0x180000000
        syms[name]=(rva,obj); byrva[rva]=(name,obj)

def rdll(rva,n):
    o=rva2off(rva); return dll[o:o+n] if o is not None else b''
def is_stub(rva):
    b=rdll(rva,6)
    return b[:6]==bytes.fromhex('0f57c033c0c3') or b[:3]==bytes.fromhex('0f57c0')
def sym_for_dump(dumpaddr):
    n='dump_%x'%dumpaddr
    return syms.get(n,None)

md=Cs(CS_ARCH_X86,CS_MODE_64); md.detail=False

print('=== 12+ je rel32 in DLL dump_277f56 (RVA 0x46065f) ===')
rva=0x46065f
code=rdll(rva,0x100)
dcode=dump[0x277f56:0x277f56+0x100]
for ins in md.disasm(code,rva):
    if ins.mnemonic.startswith('j'):
        off=ins.address-rva
        # dump-side bytes at same offset
        db=dcode[off:off+ins.size]
        target_dll=ins.address+ins.size+int(ins.op_str,0) if ins.op_str.startswith('0x') else None
        # compute from raw disp32
        raw=code[off+2:off+6]
        disp=struct.unpack('<i',raw)[0]
        tgt_dll=ins.address+ins.size+disp
        # dump-side target
        ddisp=struct.unpack('<i',db[2:6])[0]
        tgt_dump=0x277f56+off+6+ddisp
        s=sym_for_dump(tgt_dump)
        sr=byrva.get(tgt_dll)
        print('site RVA 0x%x off=0x%x  %-6s %-12s | dump tgt 0x%x sym=%s | dll tgt 0x%x sym=%s stub=%s | raw %s' % (
            ins.address,off,ins.mnemonic,ins.op_str,tgt_dump,
            ('%s@%s rva=0x%x'%(s[0],s[1],s[0])) if s else '-',
            tgt_dll,
            ('%s@%s'%(sr[0],sr[1])) if sr else '-',
            is_stub(tgt_dll) if sr else '?',
            raw.hex()))
