import ctypes
import os
from ctypes import wintypes

import pefile

k32 = ctypes.WinDLL('kernel32', use_last_error=True)
k32.GetModuleHandleA.restype = wintypes.HMODULE
k32.GetModuleHandleA.argtypes = [ctypes.c_char_p]
h = k32.GetModuleHandleA(b'ntdll.dll')
print('ntdll base', hex(h or 0))
p = os.path.join(os.environ['WINDIR'], 'System32', 'ntdll.dll')
pe = pefile.PE(p)
print('ntdll imagebase', hex(pe.OPTIONAL_HEADER.ImageBase), 'alvo RVA 0x17fe00')
exps = sorted((e.address, e.name) for e in pe.DIRECTORY_ENTRY_EXPORT.symbols if e.address)
prev = [x for x in exps if x[0] <= 0x17FE00][-5:]
nxt = [x for x in exps if x[0] > 0x17FE00][:5]
for a, n in prev:
    print('  %#x %s' % (a, n.decode('utf-8', 'replace')))
print('  >>> 0x17fe00')
for a, n in nxt:
    print('  %#x %s' % (a, n.decode('utf-8', 'replace')))
for s in pe.sections:
    if s.VirtualAddress <= 0x17FE00 < s.VirtualAddress + max(s.Misc_VirtualSize, s.SizeOfRawData):
        print('section', s.Name, 'chars', hex(s.Characteristics))
