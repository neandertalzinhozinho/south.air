"""Find references to RVAs: 8-byte pointers (several bases) and RIP-relative lea.

Usage: py -3 tools\\find_refs_any.py 0x876E0 ...
"""
import re
import struct
import sys

DUMP = r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin"
BASES = (0x180000000, 0x199B0000, 0x0)


def main():
    targets = [int(a, 16) for a in sys.argv[1:]]
    d = open(DUMP, "rb").read()
    for t in targets:
        print("== target", hex(t))
        for b in BASES:
            pat = struct.pack("<Q", b + t)
            offs = [m.start() for m in re.finditer(re.escape(pat), d)]
            if offs:
                print("  ptr base", hex(b), "->", [hex(o) for o in offs[:20]], "count", len(offs))
        # RIP-relative lea: 48 8d xx disp32 (modrm mod=00 rm=101)
        for m in re.finditer(rb"\x48\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]", d):
            i = m.start()
            disp = struct.unpack_from("<i", d, i + 3)[0]
            # instruction length 7
            if i + 7 + disp == t:
                print("  lea at", hex(i), "bytes", d[i:i + 7].hex())


if __name__ == "__main__":
    main()
