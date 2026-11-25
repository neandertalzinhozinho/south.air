"""READ-ONLY analysis of the recovered DSP DLL vs the canonical dump.
Writes nothing to the project. All output to stdout.
"""
import json, re, struct, bisect, importlib.util
from pathlib import Path
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_IMM, X86_OP_MEM

ROOT = Path(r'D:\PROJETOS\shadowFILES')
DUMPP = ROOT/'soothe3_unpacked_mem.bin'
DLLP = ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.dll'
MAPP = ROOT/'analysis/recovered_native/testdll/recovered_dsp_test.map'
CLP = ROOT/'analysis/recovered_native/dsp/dependency_build.json'
CAP = 0x18CC0000
SPAN = 0x82A5000
HI = CAP+SPAN
IB = 0x180000000

dump = DUMPP.read_bytes()
pe = pefile.PE(str(DLLP))
map_syms = {}
for line in MAPP.read_text(encoding='latin-1').splitlines():
    mm = re.match(r'\s*\d{4}:[0-9a-fA-F]{8}\s+(\S+)\s+([0-9a-fA-F]+)H?', line)
    if mm:
        try:
            va = int(mm.group(2),16)
            if IB <= va < IB+0x10000000:
                map_syms[mm.group(1)] = va-IB
        except ValueError: pass
sym_by_rva = sorted((r,n) for n,r in map_syms.items())
starts = [r for r,n in sym_by_rva]
def sym_at(rva):
    i = bisect.bisect_right(starts, rva)-1
    if i>=0:
        r,n = sym_by_rva[i]
        return f'{n}+0x{rva-r:x}' if rva>=r else '?'
    return '?'
def sym_exact(rva):
    return map_syms.get(f'dump_{rva:x}')

def dll_read(rva,n):
    for s in pe.sections:
        if s.VirtualAddress <= rva < s.VirtualAddress+max(s.Misc_VirtualSize,s.SizeOfRawData):
            off = s.PointerToRawData + (rva-s.VirtualAddress)
            return pe.__data__[off:off+n]
    raise KeyError(hex(rva))

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

def disasm(buf, va, capstone):
    out=[]
    for i in capstone.disasm(buf, va):
        out.append((i.address, i.mnemonic, i.op_str, i.bytes.hex(), i.size))
    return out

def norm(insns, kind):
    """Return normalized (mnemonic, ops) with branch targets converted to original RVA."""
    out=[]
    for (addr,mn,op,bs,sz) in insns:
        # convert immediate branch targets
        m2 = re.match(r'^(0x[0-9a-f]+)$', op)
        if m2 and mn in ('call','jmp','je','jne','ja','jb','jg','jl','jge','jle','jbe','jae','js','jns','jo','jno','jp','jnp','jz','jnz','jc','jnc','loop','loope','loopne'):
            v = int(m2.group(1),16)
            if kind=='dump':
                orig = v-CAP if CAP<=v<HI else v
            else:
                orig = v-IB if IB<=v<IB+0x10000000 else v
            op = f'0x{orig:x} [{sym_at(orig)}]'
        out.append((mn,op,bs))
    return out

regions = [(0x6f360,0x6f660,'6f360'),(0x715c0,0x71864,'715c0'),
           (0x71360,0x713eb,'71360'),(0x71400,0x715bc,'71400'),
           (0x72180,0x722bd,'72180'),(0x24140b,0x2414b0,'24140b')]

print('=== REGION BYTE / DISASM COMPARISON ===')
for rs,re_,tag in regions:
    name=f'dump_{rs:x}'
    drva = map_syms.get(name)
    print(f'\n--- {tag} dump[{rs:#x}..{re_:#x}] len={re_-rs:#x} dllsym={name}@{drva:#x}' if drva else f'\n--- {tag} NO DLL SYMBOL')
    db = dump[rs:re_]
    lb = dll_read(drva, re_-rs) if drva else b''
    nd = sum(1 for a,b in zip(db,lb) if a==b)
    print(f'    byte match {nd}/{min(len(db),len(lb))}  dll_first={lb[:16].hex()}  dump_first={db[:16].hex()}')
    di = disasm(db, CAP+rs, md)
    li = disasm(lb, IB+drva, md) if drva else []
    dn = norm(di,'dump'); ln = norm(li,'dll')
    # compare normalized instruction lists
    mism=[]
    for k in range(max(len(dn),len(ln))):
        a = dn[k] if k<len(dn) else None
        b = ln[k] if k<len(ln) else None
        if a!=b: mism.append((k,a,b))
    print(f'    disasm dump={len(dn)} insns dll={len(ln)} insns normalized_mismatch={len(mism)}')
    for k,a,b in mism[:25]:
        print(f'      [{k}] DUMP={a} DLL={b}')
    # qwords inside region that point into capture
    print('    --- capture-range qwords in region ---')
    q=0
    for off in range(rs, re_-7):
        v = struct.unpack_from('<Q',dump,off)[0]
        if CAP<=v<HI:
            t=v-CAP
            print(f'      dump@{off:#x}: q={v:#x} -> origRVA {t:#x} sym={sym_at(t)}')
            q+=1
    if q==0: print('      (none)')
