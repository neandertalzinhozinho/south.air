import struct, sys
from pathlib import Path
from capstone import *
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
b = DLL.read_bytes()
# parse PE sections
pe = struct.unpack_from('<I', b, 0x3c)[0]
nsec = struct.unpack_from('<H', b, pe+6)[0]
opt = pe + 24
secs=[]
for i in range(nsec):
    o = opt + struct.unpack_from('<H', b, pe+20)[0] + i*40
    name = b[o:o+8].split(b'\0')[0].decode('ascii','replace')
    vsize,vaddr,rsize,rptr = struct.unpack_from('<IIII', b, o+8)
    secs.append((name,vaddr,vsize,rptr,rsize))
print('SECTIONS:')
for s in secs: print(' ',s)
def r2o(rva):
    for name,va,vs,rp,rs in secs:
        if va <= rva < va+max(vs,rs): return rp + (rva-va)
    return None
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail=True
def dis(rva, before=16, after=32):
    off = r2o(rva)
    if off is None:
        print('  RVA',hex(rva),'unmapped'); return
    start = max(0, off-before)
    code = b[start:off+after]
    print('  === RVA 0x%x (file 0x%x) ===' % (rva, off))
    for ins in md.disasm(code, rva-(off-start)):
        mark = ' <== ' if ins.address == rva else ''
        print('   0x%x: %-24s %s%s' % (ins.address, ins.bytes.hex(' '), ins.mnemonic+' '+ins.op_str, mark))
for a in sys.argv[1:]:
    dis(int(a,16))
