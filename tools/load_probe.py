import ctypes, sys, os
from ctypes import wintypes

path = sys.argv[1]
k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.LoadLibraryW.restype = wintypes.HMODULE
k32.LoadLibraryW.argtypes = [wintypes.LPCWSTR]
k32.GetProcAddress.restype = ctypes.c_void_p
k32.GetProcAddress.argtypes = [wintypes.HMODULE, ctypes.c_char_p]
k32.GetModuleHandleW.restype = wintypes.HMODULE
k32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]

print('loading', path, flush=True)
h = k32.LoadLibraryW(path)
if not h:
    print('LoadLibrary FAILED err', ctypes.get_last_error(), flush=True)
    sys.exit(2)
print('module handle', hex(h), flush=True)
base = k32.GetModuleHandleW(os.path.basename(path))
print('GetModuleHandleW ->', hex(base or 0), flush=True)

fn = k32.GetProcAddress(h, b'GetPluginFactory')
print('GetPluginFactory at', hex(fn or 0), flush=True)
if not fn:
    sys.exit(3)

proto = ctypes.CFUNCTYPE(ctypes.c_void_p)
f = proto(fn)
fac = f()
print('factory ->', hex(fac or 0), flush=True)
sys.exit(0 if fac else 4)
