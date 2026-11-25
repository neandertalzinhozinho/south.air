"""C3: inspecao somente-leitura dos bytes em memoria apos load + RecoveredInit."""
import ctypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
print('BASE', hex(BASE))
for off in (0x460680, 0x460685, 0x460687, 0xae35f, 0x323ed2, 0x27b823, 0x279db4):
    print(hex(off), ctypes.string_at(BASE + off, 24).hex(' '))
