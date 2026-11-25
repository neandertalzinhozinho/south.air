from pathlib import Path
dump = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
dll  = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll').read_bytes()
def rva2off(rva):
    if 0x328000 <= rva < 0x328000+0x365b1e: return rva-0x1a00
    if 0x1000 <= rva < 0x1000+0x3260a8: return rva-0xc00
    if 0x68e000 <= rva < 0x68e000+0x508d4: return rva-0x1e00
    if 0x6df000 <= rva < 0x6df000+0xb63e18: return rva-0x2400
    raise ValueError(hex(rva))
def hd(buf, off, n, label):
    print('--- %s off=0x%x len=0x%x ---' % (label, off, n))
    b = buf[off:off+n]
    for i in range(0,len(b),16):
        chunk=b[i:i+16]
        print('%08x  %-47s  %s' % (off+i, ' '.join('%02x'%x for x in chunk),
              ''.join(chr(x) if 32<=x<127 else '.' for x in chunk)))

hd(dll,rva2off(0x46065f),0x120,'DLL RVA 0x46065f dump_277f56')
# compare to dump
a=dll[rva2off(0x46065f):rva2off(0x46065f)+0x120]
b=dump[0x277f56:0x277f56+0x120]
print('equal first 0x120?',a==b)
# stub at RVA 0x323ed2 and 0x323ed8
hd(dll,rva2off(0x323ed2),0x40,'DLL RVA 0x323ed2 dump_27b823 stub')
hd(dll,rva2off(0x323ed8),0x40,'DLL RVA 0x323ed8 dump_27bb7f stub')
# real code at DLL 0xae35f (rva_279db4)
hd(dll,rva2off(0xae35f),0x80,'DLL RVA 0xae35f real 0x27b823')
