"""Repatch the flat dump so Windows can map it at its real runtime base.

The dump was captured with the image loaded at 0x199B0000 (all internal
absolute pointers use that base), but the normalised header still says
0x180000000.  We also clear the BASERELOC directory: the relocations were
already applied when the image was dumped, so letting the loader apply them
again would corrupt every pointer.
"""
import struct, shutil, sys, os

src = r'D:\PROJETOS\soultree\dumpsooth\soothe3_unpacked.dll'
dst = r'D:\PROJETOS\soultree\dumpsooth\soothe3_loadable.dll'
REAL_BASE = 0x199B0000

shutil.copyfile(src, dst)
with open(dst, 'r+b') as f:
    hdr = f.read(0x400)
    e_lfanew = struct.unpack_from('<I', hdr, 0x3C)[0]
    opt = e_lfanew + 24
    magic = struct.unpack_from('<H', hdr, opt)[0]
    assert magic == 0x20B, f'unexpected PE magic 0x{magic:X}'
    print('e_lfanew', hex(e_lfanew), 'optional', hex(opt))
    old = struct.unpack_from('<Q', hdr, opt + 24)[0]
    print('old ImageBase', hex(old))
    f.seek(opt + 24)
    f.write(struct.pack('<Q', REAL_BASE))
    # BASERELOC = data directory index 5
    dd = opt + 112
    rva, size = struct.unpack_from('<II', hdr, dd + 5 * 8)
    print('reloc dir rva', hex(rva), 'size', hex(size))
    f.seek(dd + 5 * 8)
    f.write(struct.pack('<II', 0, 0))
    # DllCharacteristics: clear DYNAMIC_BASE (0x40) so it must map at REAL_BASE
    dc = struct.unpack_from('<H', hdr, opt + 0x46)[0]
    print('DllCharacteristics', hex(dc))
    f.seek(opt + 0x46)
    f.write(struct.pack('<H', dc & ~0x40))

print('wrote', dst, os.path.getsize(dst), 'bytes')
