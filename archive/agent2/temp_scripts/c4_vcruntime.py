import ctypes as C, struct
from capstone import *
p = r'C:\WINDOWS\System32\VCRUNTIME140.dll'
lib = C.CDLL(p)
BASE = C.cast(lib._handle, C.c_void_p).value
print('base', hex(BASE))
md = Cs(CS_ARCH_X86, CS_MODE_64)
rva = 0x121dd
start = rva - 0x60
b = C.string_at(BASE + start, 0x100)
for ins in md.disasm(b, start):
    mark = ' <== ' if ins.address == rva else ''
    print('0x%x: %-28s %s%s' % (ins.address, ins.bytes.hex(' '), ins.mnemonic+' '+ins.op_str, mark))
