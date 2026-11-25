"""Varredura corrigida: imediato -0x90 em memoria apos RecoveredInit+12 patches."""
import ctypes as C
import json
from capstone import *
from pathlib import Path

TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
DEV = json.loads((TMP / 'c3_deviations.json').read_text())
SITES = sorted([r for r in DEV
                if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable'],
               key=lambda r: int(r['site_rva'], 16))
k32 = C.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, C.c_uint32, C.POINTER(C.c_uint32)]
k32.VirtualProtect.restype = C.c_int
lib = C.CDLL(str(DLL)); lib.RecoveredInit.restype = None
BASE = C.cast(lib._handle, C.c_void_p).value
lib.RecoveredInit()
for r in SITES:
    s = BASE + int(r['site_rva'], 16) + 2
    old = C.c_uint32()
    assert k32.VirtualProtect(C.c_void_p(s), 4, 0x40, C.byref(old))
    C.memmove(s, C.create_string_buffer(bytes.fromhex(r['fix_disp32']), 4), 4)
    bk = C.c_uint32()
    assert k32.VirtualProtect(C.c_void_p(s), 4, old.value, C.byref(bk))

md = Cs(CS_ARCH_X86, CS_MODE_64)
def fmt(ins):
    return '%s %s' % (ins.mnemonic, ins.op_str)

for name, off, size in (('.text', 0x1000, 0x3260a8), ('R2TEXT', 0x328000, 0x365c1e)):
    b = C.string_at(BASE + off, size)
    pat = bytes.fromhex('70ffffff')
    hits = []
    i = b.find(pat)
    while i >= 0:
        hits.append(i)
        i = b.find(pat, i + 1)
    print('===', name, 'hits', len(hits))
    for i in hits:
        rva = off + i
        # determine the instruction containing this immediate
        found = None
        for back in range(0, 9):
            st = i - back
            if st < 0: continue
            for ins in md.disasm(bytes(b[st:i+4]), off + st):
                if ins.address + ins.size == i + 4 and ins.address <= off+i:
                    found = ins
                    break
            if found: break
        if found:
            print('  0x%x: %-30s %s' % (found.address, found.bytes.hex(' '), fmt(found)))
        else:
            print('  0x%x: raw %s' % (rva, b[max(0,i-6):i+8].hex(' ')))
