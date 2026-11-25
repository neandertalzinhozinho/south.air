import ctypes as C

class THREADENTRY32(C.Structure):
    _fields_ = [('dwSize', C.c_uint32), ('cntUsage', C.c_uint32),
                ('th32ThreadID', C.c_uint32), ('th32OwnerProcessID', C.c_uint32),
                ('tpBasePri', C.c_long), ('tpDeltaPri', C.c_long), ('dwFlags', C.c_uint32)]

k = C.WinDLL('kernel32', use_last_error=True)
k.CreateToolhelp32Snapshot.restype = C.c_void_p
k.CreateToolhelp32Snapshot.argtypes = [C.c_uint32, C.c_uint32]
k.Thread32First.argtypes = [C.c_void_p, C.POINTER(THREADENTRY32)]
k.Thread32Next.argtypes = [C.c_void_p, C.POINTER(THREADENTRY32)]
k.GetCurrentProcessId.restype = C.c_uint32

s = k.CreateToolhelp32Snapshot(4, 0)
e = THREADENTRY32()
e.dwSize = C.sizeof(THREADENTRY32)
me = k.GetCurrentProcessId()
n = 0
if k.Thread32First(s, C.byref(e)):
    while True:
        if e.th32OwnerProcessID == me:
            n += 1
            if n <= 5:
                print('tid', e.th32ThreadID, 'pid', e.th32OwnerProcessID)
        if not k.Thread32Next(s, C.byref(e)):
            break
print('mine', n, 'gle', C.get_last_error())
