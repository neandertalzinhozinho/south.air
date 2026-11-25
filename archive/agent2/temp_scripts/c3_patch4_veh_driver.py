"""C3 — mesmo patch de 4 bytes + micro-VEH passivo para capturar o AV.

So instrumentacao: av_capture.dll apenas observa (EXCEPTION_CONTINUE_SEARCH).
Reporta rip/info0/target e numero de callbacks ate o instante do AV.
"""
import ctypes
import json
import sys
from ctypes import wintypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
CAP = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\av_capture.dll')
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
RUN = sys.argv[1] if len(sys.argv) > 1 else 'v1'
LOG = TMP / f'c3_patch4_veh_{RUN}.txt'
CNT = TMP / f'c3_patch4_count_{RUN}.txt'
REPORT = TMP / f'c3_patch4_veh_report_{RUN}.json'

cap = ctypes.CDLL(str(CAP))
cap.CaptureInstallMicroVEH.argtypes = [ctypes.c_char_p, ctypes.c_uint64,
                                       ctypes.c_uint64]
cap.CaptureInstallMicroVEH.restype = ctypes.c_int
installed = cap.CaptureInstallMicroVEH(str(LOG).encode('ascii'), 0, 0)

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                               wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
k32.VirtualProtect.restype = wintypes.BOOL

meta = {'run': RUN, 'veh_installed': bool(installed), 'phase': 'loading'}
REPORT.write_text(json.dumps(meta), encoding='utf-8')
CNT.write_text('0', encoding='utf-8')

lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
SITE = BASE + 0x460687
old = wintypes.DWORD()
assert k32.VirtualProtect(ctypes.c_void_p(SITE), 4, 0x40, ctypes.byref(old))
ctypes.memmove(SITE, ctypes.create_string_buffer(bytes.fromhex('d4dcc4ff'), 4), 4)
restore = wintypes.DWORD()
assert k32.VirtualProtect(ctypes.c_void_p(SITE), 4, old.value, ctypes.byref(restore))
meta.update(phase='calling', base=hex(BASE), after=ctypes.string_at(SITE, 4).hex(' '))
REPORT.write_text(json.dumps(meta), encoding='utf-8')

calls = [0]


def bump():
    calls[0] += 1
    CNT.write_text(str(calls[0]), encoding='utf-8')


def cb_reg(a, b, c_, d):
    bump()
    return 1


def cb_evt(a):
    bump()
    return 1


f1 = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int,
                      ctypes.c_void_p, ctypes.c_int)(cb_reg)
f2 = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)(cb_evt)
host = (ctypes.c_ubyte * 0x80)()
for off, fn in ((0x18, f1), (0x20, f2)):
    ctypes.memmove(ctypes.byref(host, off),
                   ctypes.byref(ctypes.c_void_p(ctypes.cast(fn, ctypes.c_void_p).value)), 8)
cfg = (ctypes.c_int32 * 64)(*([5] * 64))
lib.Audio_863170.restype = ctypes.c_void_p
lib.Audio_863170.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double]

ret = lib.Audio_863170(ctypes.byref(host), ctypes.byref(cfg), 48000.0)
meta.update(phase='returned', ret=hex(ret) if ret else 'NULL', callbacks=calls[0])
REPORT.write_text(json.dumps(meta), encoding='utf-8')
print('returned', meta['ret'], 'callbacks', calls[0])
