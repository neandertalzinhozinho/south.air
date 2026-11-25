"""C3 — 12 desvios corrigidos + micro-VEH passivo (captura rip/info0)."""
import ctypes
import json
import sys
from ctypes import wintypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
CAP = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\av_capture.dll')
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DEV = json.loads((TMP / 'c3_deviations.json').read_text())
SITES = sorted(
    [r for r in DEV
     if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable'],
    key=lambda r: int(r['site_rva'], 16))
RUN = sys.argv[1] if len(sys.argv) > 1 else 'v1'
LOG = TMP / f'c3_patch12_veh_{RUN}.txt'
CNT = TMP / f'c3_patch12_count_{RUN}.txt'
REPORT = TMP / f'c3_patch12_veh_report_{RUN}.json'

cap = ctypes.CDLL(str(CAP))
cap.CaptureInstallMicroVEH.argtypes = [ctypes.c_char_p, ctypes.c_uint64, ctypes.c_uint64]
cap.CaptureInstallMicroVEH.restype = ctypes.c_int
installed = cap.CaptureInstallMicroVEH(str(LOG).encode('ascii'), 0, 0)
CNT.write_text('0', encoding='utf-8')

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                               wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
k32.VirtualProtect.restype = wintypes.BOOL

meta = {'run': RUN, 'veh_installed': bool(installed), 'phase': 'loading'}
REPORT.write_text(json.dumps(meta), encoding='utf-8')
lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
meta['base'] = hex(BASE)
for r in SITES:
    site = BASE + int(r['site_rva'], 16) + 2
    old = wintypes.DWORD()
    assert k32.VirtualProtect(ctypes.c_void_p(site), 4, 0x40, ctypes.byref(old))
    ctypes.memmove(site, ctypes.create_string_buffer(bytes.fromhex(r['fix_disp32']), 4), 4)
    back = wintypes.DWORD()
    assert k32.VirtualProtect(ctypes.c_void_p(site), 4, old.value, ctypes.byref(back))
meta['phase'] = 'calling'
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
