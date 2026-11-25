"""Read-only probe of a live process: module layout + per-section entropy.

No code injection, no debugger attach: only OpenProcess(PROCESS_VM_READ) and
ReadProcessMemory / VirtualQueryEx.  Safe to run against a protected host.

Usage: py tools/live_probe.py <pid> <module-substring>
"""
import ctypes, ctypes.wintypes as wt, sys, math, hashlib

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
MEM_COMMIT = 0x1000
PAGE_GUARD = 0x100
PAGE_NOACCESS = 0x01
EXEC = (0x10, 0x20, 0x40, 0x80)  # EXECUTE, EXECUTE_READ, EXECUTE_READWRITE, EXECUTE_WRITECOPY

class MBI(ctypes.Structure):
    _fields_ = [('BaseAddress', ctypes.c_ulonglong),
                ('AllocationBase', ctypes.c_ulonglong),
                ('AllocationProtect', wt.DWORD),
                ('__a1', wt.DWORD),
                ('RegionSize', ctypes.c_ulonglong),
                ('State', wt.DWORD),
                ('Protect', wt.DWORD),
                ('Type', wt.DWORD),
                ('__a2', wt.DWORD)]

class MODULEINFO(ctypes.Structure):
    _fields_ = [('lpBaseOfDll', ctypes.c_void_p),
                ('SizeOfImage', wt.DWORD),
                ('EntryPoint', ctypes.c_void_p)]

k32.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
k32.OpenProcess.restype = wt.HANDLE
k32.ReadProcessMemory.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.c_void_p,
                                  ctypes.c_size_t, ctypes.POINTER(ctypes.c_size_t)]
k32.ReadProcessMemory.restype = wt.BOOL
k32.VirtualQueryEx.argtypes = [wt.HANDLE, ctypes.c_void_p, ctypes.POINTER(MBI), ctypes.c_size_t]
k32.VirtualQueryEx.restype = ctypes.c_size_t
k32.CloseHandle.argtypes = [wt.HANDLE]
psapi.EnumProcessModulesEx.argtypes = [wt.HANDLE, ctypes.POINTER(wt.HMODULE), wt.DWORD,
                                       ctypes.POINTER(wt.DWORD), wt.DWORD]
psapi.GetModuleFileNameExW.argtypes = [wt.HANDLE, wt.HMODULE, wt.LPWSTR, wt.DWORD]
psapi.GetModuleInformation.argtypes = [wt.HANDLE, wt.HMODULE, ctypes.POINTER(MODULEINFO), wt.DWORD]

def entropy(b):
    if not b:
        return 0.0
    c = [0] * 256
    for x in b:
        c[x] += 1
    n = len(b)
    e = 0.0
    for v in c:
        if v:
            p = v / n
            e -= p * math.log2(p)
    return e

pid = int(sys.argv[1])
needle = sys.argv[2].lower()
h = k32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
if not h:
    print('OpenProcess failed', ctypes.get_last_error()); sys.exit(2)

# --- modules
mods = (wt.HMODULE * 1024)()
needed = wt.DWORD()
if not psapi.EnumProcessModulesEx(h, mods, ctypes.sizeof(mods), ctypes.byref(needed), 3):
    print('EnumProcessModulesEx failed', ctypes.get_last_error()); sys.exit(3)
buf = ctypes.create_unicode_buffer(1024)
target = None
for i in range(needed.value // ctypes.sizeof(wt.HMODULE)):
    if psapi.GetModuleFileNameExW(h, mods[i], buf, 1024):
        if needle in buf.value.lower():
            mi = MODULEINFO()
            psapi.GetModuleInformation(h, mods[i], ctypes.byref(mi), ctypes.sizeof(mi))
            target = (buf.value, mi.lpBaseOfDll, mi.SizeOfImage)
            print('MODULE', target[0])
            print('  base 0x%X size 0x%X' % (target[1], target[2]))
if not target:
    print('module not found'); sys.exit(4)
path, base, size = target

def read(addr, n):
    out = []
    done = 0
    while done < n:
        chunk = min(n - done, 1 << 20)
        b = ctypes.create_string_buffer(chunk)
        got = ctypes.c_size_t(0)
        ok = k32.ReadProcessMemory(h, ctypes.c_void_p(addr + done), b, chunk, ctypes.byref(got))
        if not ok or got.value == 0:
            break
        out.append(b.raw[:got.value])
        done += got.value
        if got.value < chunk:
            break
    return b''.join(out)

# --- executable ranges (whole address space)
print('\n--- executable regions ---')
addr = 0
mbi = MBI()
regions = []
while addr < 0x7FFFFFFFFFFF:
    if k32.VirtualQueryEx(h, ctypes.c_void_p(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
        addr += 0x1000
        continue
    rbase, rsize, prot, state = mbi.BaseAddress, mbi.RegionSize, mbi.Protect, mbi.State
    if state == MEM_COMMIT and (prot & 0xFF) in EXEC and not (prot & PAGE_GUARD):
        regions.append((rbase, rsize, prot))
    addr = rbase + rsize
print('count', len(regions))
for rb, rs, pr in regions:
    inside = base <= rb < base + size
    tag = 'module' if inside else 'OUTSIDE'
    print('  0x%012X size 0x%-8X prot 0x%02X %s' % (rb, rs, pr & 0xFF, tag))

# --- PE sections from live memory
hdr = read(base, 0x1000)
if len(hdr) < 0x200:
    print('cannot read header'); sys.exit(5)
e_lfanew = int.from_bytes(hdr[0x3C:0x40], 'little')
nsec = int.from_bytes(hdr[e_lfanew + 6:e_lfanew + 8], 'little')
optsz = int.from_bytes(hdr[e_lfanew + 20:e_lfanew + 22], 'little')
sec0 = e_lfanew + 24 + optsz
print('\n--- live sections ---')
total_hash = hashlib.sha256()
for i in range(nsec):
    o = sec0 + 40 * i
    name = hdr[o:o + 8].rstrip(b'\x00').decode('latin-1')
    vsize = int.from_bytes(hdr[o + 8:o + 12], 'little')
    rva = int.from_bytes(hdr[o + 12:o + 16], 'little')
    data = read(base + rva, vsize) if vsize else b''
    if name in ('.text', '.data', '.guard', '.proxy', 'IPPCODE'):
        print('  %-10s rva 0x%-9X vsz 0x%-9X read 0x%-9X entropy %.3f sha256 %s'
              % (name, rva, vsize, len(data), entropy(data), hashlib.sha256(data).hexdigest()[:16]))
    else:
        print('  %-10s rva 0x%-9X vsz 0x%-9X read 0x%-9X entropy %.3f'
              % (name, rva, vsize, len(data), entropy(data)))
k32.CloseHandle(h)
