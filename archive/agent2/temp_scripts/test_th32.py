import ctypes as C

k32 = C.WinDLL('kernel32', use_last_error=True)
k32.CreateToolhelp32Snapshot.restype = C.c_void_p
k32.CreateToolhelp32Snapshot.argtypes = [C.c_uint32, C.c_uint32]
k32.Thread32First.argtypes = [C.c_void_p, C.c_void_p]
k32.Thread32Next.argtypes = [C.c_void_p, C.c_void_p]

snap = k32.CreateToolhelp32Snapshot(4, 0)
print('snap', hex(snap or 0), 'gle', C.get_last_error())
buf = C.create_string_buffer(64)
C.c_uint32.from_buffer(buf, 0).value = 28
r = k32.Thread32First(snap, buf)
print('first', r, 'gle', C.get_last_error())
n = 0
if r:
    while True:
        n += 1
        tid = C.c_uint32.from_buffer(buf, 8).value
        pid = C.c_uint32.from_buffer(buf, 12).value
        if n < 5:
            print('tid', tid, 'pid', pid)
        if not k32.Thread32Next(snap, buf):
            break
print('count', n, 'gle', C.get_last_error())
