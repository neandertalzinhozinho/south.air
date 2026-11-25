"""Resolve an x86-64 `jmp qword ptr [rip+disp32]` thunk at a given RVA.

Usage:
    py -3 tools\\resolve_thunk.py 0x1C9A5A1 [0x1C9AA01 ...]

Prints: thunk bytes, jmp displacement, IAT slot, IAT 8-byte target,
and the import name if the slot belongs to the import address table.

Import table parsed from the PE import directory (same rule as
tools/thunk_map.py): descriptor `+0x0C name`, `+0x10 INT`, `+0x10 IAT`.
RVA convention for the dump: data pointers are VAs on base 0x199B0000.
"""
import struct
import sys

sys.path.insert(0, 'tools')
import re_lib  # noqa: E402

BASE = 0x199B0000


def _cstr(d, off, maxlen=300):
    if not (0 < off < len(d)):
        return '?'
    end = d.find(b'\x00', off, off + maxlen)
    if end < 0:
        return '?'
    raw = d[off:end]
    try:
        return raw.decode('ascii')
    except UnicodeDecodeError:
        return raw.decode('latin1')


def import_names(d):
    """Return dict IAT slot RVA -> (name, dll)."""
    # PE headers live at the very start of the dump; e_lfanew at 0x3C.
    e_lfanew = struct.unpack_from('<I', d, 0x3C)[0]
    opt = e_lfanew + 24
    magic = struct.unpack_from('<H', d, opt)[0]
    if magic != 0x20B:
        raise SystemExit('not PE32+ (magic 0x%X)' % magic)
    dd = opt + 112  # data directories start at +112 for PE32+
    imp_rva, imp_size = struct.unpack_from('<II', d, dd + 8 * 1)
    out = {}
    o = imp_rva
    while True:
        name_rva, _ts, _fc, int_rva, iat_rva = struct.unpack_from('<IIIII', d, o)
        if name_rva == 0 and int_rva == 0 and iat_rva == 0:
            break
        dll = _cstr(d, name_rva)
        k = 0
        while True:
            entry = struct.unpack_from('<Q', d, int_rva + 8 * k)[0]
            if entry == 0:
                break
            if not (entry & 0x8000000000000000):
                nm = _cstr(d, entry & 0x7FFFFFFF)
            else:
                nm = 'ordinal#%d' % (entry & 0xFFFF)
            out[iat_rva + 8 * k] = (nm, dll)
            k += 1
        o += 20
    return out


def resolve(addr, names):
    d = re_lib.data()
    raw = d[addr:addr + 16]
    if raw[:2] != b'\xff\x25':
        return '0x%X: not a `jmp [rip+d32]` thunk (bytes %s)' % (addr, raw[:8].hex())
    disp = struct.unpack_from('<i', raw, 2)[0]
    slot = addr + 6 + disp
    val = struct.unpack_from('<Q', d, slot)[0]
    nm = names.get(slot)
    if nm is None:
        return ('0x%X: jmp [0x%X] -> 0x%X (not an IAT slot)' % (addr, slot, val))
    dll, name = nm[1], nm[0]
    return '0x%X: jmp [0x%X] -> IAT[0x%X] = %s ! %s' % (addr, slot, slot, dll, name)


if __name__ == '__main__':
    names = import_names(re_lib.data())
    args = [int(a, 16) for a in sys.argv[1:]]
    for a in args:
        print(resolve(a, names))
