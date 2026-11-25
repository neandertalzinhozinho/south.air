import ctypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
pat = (0xFFFFFFFFFFFFFF70).to_bytes(8, 'little')
for name, off, size in (('.text', 0x1000, 0x3260a8), ('.rdata', 0x68e000, 0x508d4),
                        ('.data', 0x6df000, 0xb63e18)):
    b = ctypes.string_at(BASE + off, size)
    hits = []
    i = b.find(pat)
    while i >= 0 and len(hits) < 20:
        hits.append(off + i)
        i = b.find(pat, i + 1)
    print(name, 'hits', [hex(h) for h in hits])
