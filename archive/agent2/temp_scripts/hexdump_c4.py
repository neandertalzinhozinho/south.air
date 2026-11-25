from pathlib import Path
dump = Path(r'D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin').read_bytes()
dll  = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll').read_bytes()

def hd(buf, off, n, label):
    print('--- %s off=0x%x len=0x%x ---' % (label, off, n))
    b = buf[off:off+n]
    for i in range(0,len(b),16):
        chunk=b[i:i+16]
        print('%08x  %-47s  %s' % (off+i, ' '.join('%02x'%x for x in chunk),
              ''.join(chr(x) if 32<=x<127 else '.' for x in chunk)))

# dump_277f56 region (real code)
hd(dump,0x277f56,0x120,'DUMP 277f56')
# DLL copy: image base 0x180000000, section .text RVA->file offset? map says 0001:003... -> 0x18032...; file offset likely = RVA for this PE? check
hd(dll,0x46065f,0x120,'DLL fileoff 0x46065f (RVA 0x46065f?)')
