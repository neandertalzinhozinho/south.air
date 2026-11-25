"""Varredura em memoria por imediatos 0xffffff70 (-0x90) e sub/lea -0x90."""
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

pats = {
    'imm32_ffffff70': bytes.fromhex('70ffffff'),
    'imm64_ffffff70': bytes.fromhex('70ffffffffffffff'),
    'sub_imm32_90': bytes.fromhex('8190') + b'\x90\x00\x00\x00',
    'lea_disp_minus90': bytes.fromhex('8d'),
}
md = Cs(CS_ARCH_X86, CS_MODE_64)
for name, off, size in (('.text', 0x1000, 0x3260a8), ('R2TEXT', 0x328000, 0x365c1e)):
    b = C.string_at(BASE + off, size)
    print('===', name, 'size', hex(size))
    for key in ('imm32_ffffff70', 'imm64_ffffff70', 'sub_imm32_90'):
        pat = pats[key]
        hits = []
        i = b.find(pat)
        while i >= 0 and len(hits) < 60:
            hits.append(off + i)
            i = b.find(pat, i + 1)
        print(' ', key, len(hits), [hex(h) for h in hits[:60]])
        for h in hits[:12]:
            st = max(0, h - 12)
            code = b[st:h + 16]
            print('    @0x%x bytes=%s' % (h, b[h-4:h+12].hex(' ')))
            for ins in md.disasm(code, off + st):
                if ins.address <= h < ins.address + ins.size:
                    print('       -> 0x%x: %s %s' % (ins.address, ins.mnemonic, ins.op_str))
