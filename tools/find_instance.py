"""Read-only scan of a live process for a qword pattern (default: vtable ptr).

Usage: py tools/find_instance.py <pid> <hex-qword> [max_gb]
Prints every hit with its region, then dumps 0x200 bytes around the first hit.
"""
import ctypes, ctypes.wintypes as wt, sys, struct, time

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
PAGE_GUARD = 0x100
WRITABLE = (0x04, 0x08, 0x40, 0x80)  # RW, WRITECOPY, EXECUTE_RW, EXECUTE_WRITECOPY

class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_ulonglong), ('AllocationBase', ctypes.c_ulonglong),
                ('AllocationProtect', wt.DWORD), ('__a1', wt.DWORD),
                ('RegionSize', ctypes.c_ulonglong), ('State', wt.DWORD),
                ('Protect', wt.DWORD), ('Type', wt.DWORD), ('__a2', wt.DWORD)]

k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.ReadProcessMemory.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.ReadProcessMemory.restype = wt.BOOL
k32.VirtualQueryEx.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(MBI), ctypes.c_size_t]
k32.VirtualQueryEx.restype = ctypes.c_size_t

pid = int(sys.argv[1], 0)
val = int(sys.argv[2], 0)
max_gb = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
pat = struct.pack('<Q', val)

h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
if not h:
    print('OpenProcess failed', ctypes.get_last_error()); sys.exit(2)

def read(addr, n):
    b = ctypes.create_string_buffer(n)
    got = ctypes.c_size_t(0)
    if k32.ReadProcessMemory(h, ctypes.c_void_p(addr), b, n, ctypes.byref(got)) and got.value:
        return b.raw[:got.value]
    return b''

mbi = MBI()
addr = 0
hits = []
scanned = 0
limit = int(max_gb * (1 << 30))
t0 = time.time()
CH = 8 << 20
while addr < 0x7FFFFFFFFFFF and scanned < limit:
    if k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
        addr += 0x1000
        continue
    base, size, prot, state = mbi.BaseAddress, mbi.RegionSize, mbi.Protect, mbi.State
    if state == MEM_COMMIT and (prot & 0xFF) in WRITABLE and not (prot & PAGE_GUARD):
        off = 0
        while off < size and scanned < limit:
            n = min(CH, size - off)
            data = read(base + off, n)
            if data:
                scanned += len(data)
                i = data.find(pat)
                while i >= 0:
                    hits.append((base + off + i, base, size, prot & 0xFF))
                    if len(hits) >= 40:
                        break
                    i = data.find(pat, i + 1)
            off += n
        if len(hits) >= 40:
            break
    addr = base + size

print('scanned %.2f GB in %.1fs, hits %d' % (scanned / (1 << 30), time.time() - t0, len(hits)))
for a, rb, rs, pr in hits:
    print('  hit 0x%X  region 0x%X size 0x%X prot 0x%02X' % (a, rb, rs, pr))

if hits:
    a = hits[0][0]
    dump = read(a & ~0xF, 0x200)
    print('\n--- dump around first hit (object base aligned) ---')
    for o in range(0, len(dump), 16):
        chunk = dump[o:o + 16]
        qs = ' '.join('%016X' % struct.unpack_from('<Q', chunk, j)[0] for j in range(0, 16, 8) if len(chunk) >= j + 8)
        print('  +0x%03X  %-32s  %s' % (o, chunk.hex(), qs))
k32.CloseHandle(h)
