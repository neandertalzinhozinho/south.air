"""C3 — aplica os 12 desvios da tabela do C2 em memoria e roda 1 chamada."""
import ctypes
import json
import sys
from ctypes import wintypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
DEV = json.loads((TMP / 'c3_deviations.json').read_text())
SITES = sorted(
    [r for r in DEV
     if 0x460650 <= int(r['site_rva'], 16) <= 0x460700 and r['status'] == 'fixable'],
    key=lambda r: int(r['site_rva'], 16))
assert len(SITES) == 12, len(SITES)
RUN = sys.argv[1] if len(sys.argv) > 1 else '1'
REPORT = TMP / f'c3_patch12_report_{RUN}.json'

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                               wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
k32.VirtualProtect.restype = wintypes.BOOL

payload = {'run': RUN, 'phase': 'loading', 'patches': []}
REPORT.write_text(json.dumps(payload, indent=2), encoding='utf-8')

lib = ctypes.CDLL(str(DLL))
lib.RecoveredInit.restype = None
BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
lib.RecoveredInit()
payload['base'] = hex(BASE)

for r in SITES:
    je = int(r['site_rva'], 16)
    site = BASE + je + 2
    before = ctypes.string_at(site, 4).hex(' ')
    old = wintypes.DWORD()
    assert k32.VirtualProtect(ctypes.c_void_p(site), 4, 0x40, ctypes.byref(old))
    fix = bytes.fromhex(r['fix_disp32'])
    ctypes.memmove(site, ctypes.create_string_buffer(fix, 4), 4)
    restore = wintypes.DWORD()
    assert k32.VirtualProtect(ctypes.c_void_p(site), 4, old.value, ctypes.byref(restore))
    after = ctypes.string_at(site, 4).hex(' ')
    payload['patches'].append({
        'je_rva': hex(je), 'before': before, 'after': after,
        'expected': r['fix_disp32'], 'ok': after == r['fix_disp32'].replace('', ' ').strip(),
        'authentic_rva': r['authentic_rva'],
    })
payload['phase'] = 'calling'
REPORT.write_text(json.dumps(payload, indent=2), encoding='utf-8')

calls = [0]


def cb_reg(a, b, c_, d):
    calls[0] += 1
    return 1


def cb_evt(a):
    calls[0] += 1
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
payload['phase'] = 'returned'
payload['ret'] = hex(ret) if ret else 'NULL'
payload['callbacks'] = calls[0]
REPORT.write_text(json.dumps(payload, indent=2), encoding='utf-8')
print('returned', payload['ret'], 'callbacks', calls[0])
