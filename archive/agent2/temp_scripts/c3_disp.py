import ctypes
from pathlib import Path
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
b = ctypes.string_at(BASE + 0x460650, 0x130)
for i in range(0, len(b), 11):
    print(hex(0x460650 + i), b[i:i+11].hex(' '))
