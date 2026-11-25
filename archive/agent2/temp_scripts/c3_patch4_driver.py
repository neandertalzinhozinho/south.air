"""C3 — validacao EM MEMORIA do patch de 4 bytes no disp32 do je.

Load DLL -> RecoveredInit -> VirtualProtect(RW) em base+0x460687 ->
escreve d4 dc c4 ff -> restaura protecao -> 1 chamada Audio_863170.

Saida: c3_patch4_report_<run>.json no proprio temp (fora do repo).
"""
import ctypes
import json
import sys
from ctypes import wintypes
from pathlib import Path

DLL = Path(r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll')
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
RUN = sys.argv[1] if len(sys.argv) > 1 else '1'
REPORT = TMP / f'c3_patch4_report_{RUN}.json'

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.VirtualProtect.argtypes = [ctypes.c_void_p, ctypes.c_size_t,
                               wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
k32.VirtualProtect.restype = wintypes.BOOL

payload = {
    'run': RUN,
    'dll': str(DLL),
    'phase': 'loading',
    'base': None,
    'site_offset': '0x460687',
    'patch': 'd4 dc c4 ff',
    'protect_ok': None,
    'old_protect': None,
    'before': None,
    'after': None,
    'target_rva': None,
    'callbacks': 0,
    'ret': None,
}


def save():
    REPORT.write_text(json.dumps(payload, indent=2), encoding='utf-8')


try:
    lib = ctypes.CDLL(str(DLL))
    lib.RecoveredInit.restype = None
    BASE = ctypes.cast(lib._handle, ctypes.c_void_p).value
    payload['base'] = hex(BASE)
    lib.RecoveredInit()

    SITE = BASE + 0x460687
    old = wintypes.DWORD()
    ok = k32.VirtualProtect(ctypes.c_void_p(SITE), 4, 0x40, ctypes.byref(old))
    payload['protect_ok'] = bool(ok)
    payload['old_protect'] = hex(old.value)
    if not ok:
        payload['phase'] = 'virtualprotect_failed'
        payload['winerror'] = ctypes.get_last_error()
        save()
        sys.exit(2)

    payload['before'] = ctypes.string_at(SITE, 4).hex(' ')
    buf = ctypes.create_string_buffer(bytes.fromhex('d4dcc4ff'), 4)
    ctypes.memmove(SITE, buf, 4)
    payload['after'] = ctypes.string_at(SITE, 4).hex(' ')

    restore = wintypes.DWORD()
    payload['restore_ok'] = bool(k32.VirtualProtect(ctypes.c_void_p(SITE), 4,
                                                    old.value, ctypes.byref(restore)))
    # je rel32: proxima instrucao em BASE+0x46068b; disp = 0xffc4dcd4 = -0x3b232c
    disp = ctypes.c_int32.from_buffer_copy(buf.raw).value
    payload['disp'] = hex(disp & 0xFFFFFFFF)
    payload['target_rva'] = hex((BASE + 0x46068B + disp) - BASE)
    save()

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

    payload['phase'] = 'calling'
    save()
    ret = lib.Audio_863170(ctypes.byref(host), ctypes.byref(cfg), 48000.0)
    payload['phase'] = 'returned'
    payload['ret'] = hex(ret) if ret else 'NULL'
    payload['callbacks'] = calls[0]
    save()
    print('returned', payload['ret'], 'callbacks', calls[0])
except Exception as exc:  # noqa: BLE001
    payload['phase'] = 'exception'
    payload['exception'] = repr(exc)
    save()
    raise
