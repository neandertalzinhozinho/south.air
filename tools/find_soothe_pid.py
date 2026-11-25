"""Find every live process that has soothe3.vst3 loaded (read-only).

Usage: py tools/find_soothe_pid.py
Prints: pid, process name, module path, base, size.
"""
import ctypes, ctypes.wintypes as wt, sys

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_VM_READ = 0x0010
LIST_MODULES_ALL = 0x03

class MODULEINFO(ctypes.Structure):
    _fields_ = [('lpBaseOfDll', ctypes.c_void_p),
                ('SizeOfImage', wt.DWORD),
                ('EntryPoint', ctypes.c_void_p)]

k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.CloseHandle.argtypes = [wt.HANDLE]
psapi.EnumProcesses.argtypes = [ctypes.POINTER(wt.DWORD), wt.DWORD, ctypes.POINTER(wt.DWORD)]
psapi.EnumProcesses.restype = wt.BOOL
psapi.EnumProcessModulesEx.argtypes = [wt.HANDLE, ctypes.POINTER(wt.HMODULE), wt.DWORD,
                                       ctypes.POINTER(wt.DWORD), wt.DWORD]
psapi.GetModuleFileNameExW.argtypes = [wt.HANDLE, wt.HMODULE, wt.LPWSTR, wt.DWORD]
psapi.GetModuleInformation.argtypes = [wt.HANDLE, wt.HMODULE, ctypes.POINTER(MODULEINFO), wt.DWORD]

pids = (wt.DWORD * 4096)()
need = wt.DWORD()
if not psapi.EnumProcesses(pids, ctypes.sizeof(pids), ctypes.byref(need)):
    print('EnumProcesses failed', ctypes.get_last_error()); sys.exit(2)
n = need.value // ctypes.sizeof(wt.DWORD)

buf = ctypes.create_unicode_buffer(2048)
found = 0
for i in range(n):
    pid = pids[i]
    if not pid:
        continue
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h:
        continue
    try:
        mods = (wt.HMODULE * 4096)()
        mneed = wt.DWORD()
        if not psapi.EnumProcessModulesEx(h, mods, ctypes.sizeof(mods), ctypes.byref(mneed), LIST_MODULES_ALL):
            continue
        for j in range(mneed.value // ctypes.sizeof(wt.HMODULE)):
            if not psapi.GetModuleFileNameExW(h, mods[j], buf, 2048):
                continue
            if 'soothe3' in buf.value.lower():
                mi = MODULEINFO()
                psapi.GetModuleInformation(h, mods[j], ctypes.byref(mi), ctypes.sizeof(mi))
                print('PID %d  base 0x%X  size 0x%X' % (pid, mi.lpBaseOfDll, mi.SizeOfImage))
                print('   %s' % buf.value)
                found += 1
    finally:
        k32.CloseHandle(h)

if not found:
    print('soothe3 not loaded in any accessible process')
