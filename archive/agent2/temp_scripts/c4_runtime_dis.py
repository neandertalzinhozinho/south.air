"""Desmonta bytes EM MEMORIA (apos RecoveredInit + 12 patches) nos RVAs dos frames do AV."""
import ctypes as C
import json
import sys
from ctypes import wintypes as W
from capstone import *
from pathlib import Path

TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
DEV = json.loads((TMP / 'c3_deviations.json').read_text())
SITES = sorted([r for r in DEV
                if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable'],
               key=lambda r: int(r['site_rva'], 16))
k32 = C.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [C.c_void_p, C.c_size_t, W.DWORD, C.POINTER(W.DWORD)]
k32.VirtualProtect.restype = W.BOOL

lib = C.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = C.cast(lib._handle, C.c_void_p).value
lib.RecoveredInit()
for r in SITES:
    site = BASE + int(r['site_rva'], 16) + 2
    old = W.DWORD()
    assert k32.VirtualProtect(C.c_void_p(site), 4, 0x40, C.byref(old))
    C.memmove(site, C.create_string_buffer(bytes.fromhex(r['fix_disp32']), 4), 4)
    back = W.DWORD()
    assert k32.VirtualProtect(C.c_void_p(site), 4, old.value, C.byref(back))

md = Cs(CS_ARCH_X86, CS_MODE_64)
for a in sys.argv[1:]:
    rva = int(a, 16)
    start_rva = rva - 48
    code = C.string_at(BASE + start_rva, 96)
    print('=== runtime RVA 0x%x ===' % rva)
    for ins in md.disasm(code, start_rva):
        mark = ' <== ' if ins.address == rva else ''
        print('  0x%x: %-27s %s%s' % (ins.address, ins.bytes.hex(' '),
              ins.mnemonic + ' ' + ins.op_str, mark))
