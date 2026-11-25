import struct
from pathlib import Path
p = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll').read_bytes()
e_lfanew = struct.unpack_from('<I', p, 0x3c)[0]
print('e_lfanew=0x%x sig=%r' % (e_lfanew, p[e_lfanew:e_lfanew+4]))
coff = e_lfanew+4
machine,nsec,ts,ptrsym,nsym,optsz,chars = struct.unpack_from('<HHIIIHH', p, coff)
print('machine=0x%x nsec=%d optsz=%d' % (machine,nsec,optsz))
opt = coff+20
magic = struct.unpack_from('<H',p,opt)[0]
print('magic=0x%x' % magic)
if magic==0x20b:
    imagebase = struct.unpack_from('<Q',p,opt+24)[0]
    sectab = opt+optsz
    print('imagebase=0x%x sectab=0x%x' % (imagebase,sectab))
    for i in range(nsec):
        s = sectab+40*i
        name = p[s:s+8].rstrip(b'\0').decode('latin1')
        vsize,vaddr,rsize,raddr = struct.unpack_from('<IIII',p,s+8)
        print('%d %-8s vsize=0x%x vaddr=0x%x rsize=0x%x raddr=0x%x  (RVA0x46065f->file 0x%x)' % (
            i,name,vsize,vaddr,rsize,raddr, raddr+(0x46065f-vaddr) if vaddr<=0x46065f<vaddr+vsize else -1))
