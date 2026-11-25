"""Desmonta intervalo em memoria com start alinhado, incluindo skipdata."""
import ctypes as C
import json, sys
from capstone import *
from pathlib import Path
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
DEV = json.loads((TMP/'c3_deviations.json').read_text())
SITES = sorted([r for r in DEV if 0x460650<=int(r['site_rva'],16)<=0x460700 and r['status']=='fixable'],
               key=lambda r:int(r['site_rva'],16))
k32=C.WinDLL('kernel32',use_last_error=True)
k32.VirtualProtect.argtypes=[C.c_void_p,C.c_size_t,C.c_uint32,C.POINTER(C.c_uint32)]
k32.VirtualProtect.restype=C.c_int
lib=C.CDLL(str(DLL)); lib.RecoveredInit.restype=None
BASE=C.cast(lib._handle,C.c_void_p).value
lib.RecoveredInit()
for r in SITES:
    s=BASE+int(r['site_rva'],16)+2; old=C.c_uint32()
    assert k32.VirtualProtect(C.c_void_p(s),4,0x40,C.byref(old))
    C.memmove(s,C.create_string_buffer(bytes.fromhex(r['fix_disp32']),4),4)
    bk=C.c_uint32(); assert k32.VirtualProtect(C.c_void_p(s),4,old.value,C.byref(bk))
md=Cs(CS_ARCH_X86,CS_MODE_64); md.skipdata=True
for a in sys.argv[1:]:
    rva=int(a,16); start=rva-0x40
    b=C.string_at(BASE+start,0xc0)
    print('=== runtime 0x%x ==='%rva)
    for ins in md.disasm(b,start):
        mark=' <== ' if ins.address==rva else ''
        print('  0x%x: %-27s %s%s'%(ins.address,ins.bytes.hex(' '),ins.mnemonic+' '+ins.op_str,mark))
