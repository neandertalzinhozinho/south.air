"""Own copy of worker with timing logs (read-only w.r.t. project)."""
import ctypes, time, os
from pathlib import Path
DLL = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\testdll\recovered_dsp_test.dll'
t0=time.time()
def log(s): print(f'[{time.time()-t0:.3f}] {s}', flush=True)
log('start pid=%d' % os.getpid())
lib = ctypes.CDLL(DLL)
log('loaded handle=0x%x' % (lib._handle or 0))
lib.RecoveredInit.restype = None
lib.RecoveredInit()
log('RecoveredInit done')
time.sleep(3.0)
log('before factory')
cb_reg = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
cb_evt = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p)
keep = [cb_reg(lambda *a: 0), cb_evt(lambda *a: 0)]
host = (ctypes.c_ubyte * 0x80)()
for off, fn in ((0x18, keep[0]), (0x20, keep[1])):
    ctypes.memmove(ctypes.byref(host, off), ctypes.byref(ctypes.c_void_p(ctypes.cast(fn, ctypes.c_void_p).value)), 8)
cfg = (ctypes.c_int32 * 64)(*([5] * 64))
lib.Audio_863170.restype = ctypes.c_void_p
lib.Audio_863170.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_double]
w = lib.Audio_863170(ctypes.byref(host), ctypes.byref(cfg), 48000.0)
log('factory -> %s' % (hex(w) if w else w))
