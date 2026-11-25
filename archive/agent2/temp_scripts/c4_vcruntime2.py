import ctypes as C
from capstone import *
p = r'C:\WINDOWS\System32\VCRUNTIME140.dll'
lib = C.CDLL(p)
BASE = C.cast(lib._handle, C.c_void_p).value
md = Cs(CS_ARCH_X86, CS_MODE_64); md.skipdata = True
rva = 0x121dd
start = 0x12100
b = C.string_at(BASE + start, 0x100)
print('base', hex(BASE), 'target', hex(BASE+rva))
for ins in md.disasm(b, start):
    mark = ' <== ' if ins.address == rva else ''
    if ins.address <= rva + 8:
        print('0x%x: %-26s %s%s' % (ins.address, ins.bytes.hex(' '), ins.mnemonic+' '+ins.op_str, mark))
