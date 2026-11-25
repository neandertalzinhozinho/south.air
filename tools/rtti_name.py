import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
d = re_lib.data()
BASE = 0x199B0000

def u32(o): return struct.unpack_from('<I', d, o)[0]

def col_name(col_rva):
    sig, off, cd, td, cd2, self_ = struct.unpack_from('<IIIIII', d, col_rva)
    # TypeDescriptor: vftable ptr (8) + spare (8) + name (char[])
    name = re_lib.cstr(td + 16, 200)
    return sig, off, td, name

def vtables_near(vt):
    print(f'--- vtable 0x{vt:X}')
    prev = struct.unpack_from('<Q', d, vt - 8)[0]
    if prev == 0:
        print('   no COL (prev=0)'); return
    # prev is an absolute pointer: subtract BASE, or it may be image-relative already
    col = prev - BASE
    if not (0x1D8C000 <= col < 0x2758000):
        # maybe it's already an RVA-ish pointer
        col = prev - 0x180000000
    if not (0x1D8C000 <= col < 0x2758000):
        print(f'   prev=0x{prev:X} -> col 0x{col:X} out of .data'); return
    try:
        sig, off, td, name = col_name(col)
        print(f'   COL 0x{col:X} sig=0x{sig:X} offset={off} type_desc=0x{td:X} name={name!r}')
    except Exception as e:
        print('   err', e)

for a in sys.argv[1:]:
    vtables_near(int(a, 0))
