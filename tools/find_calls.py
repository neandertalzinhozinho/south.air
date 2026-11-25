"""Find direct E8 rel32 call sites to given RVAs in the .text section.

Usage: py -3 tools\\find_calls.py 0x876E0 0x87AA0 ...
"""
import re
import struct
import sys

DUMP = r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin"


def sections(d):
    e = struct.unpack_from("<I", d, 0x3C)[0]
    nsec = struct.unpack_from("<H", d, e + 6)[0]
    sh = e + 24 + struct.unpack_from("<H", d, e + 20)[0]
    out = []
    for i in range(nsec):
        o = sh + i * 40
        name = d[o:o + 8].rstrip(b"\0").decode("latin1")
        vs, va, rs, ra = struct.unpack_from("<IIII", d, o + 8)
        out.append((name, va, vs, ra, rs))
    return out


def main():
    targets = {int(a, 16) for a in sys.argv[1:]}
    d = open(DUMP, "rb").read()
    secs = sections(d)
    for s in secs:
        print(s)
    hits = {t: [] for t in targets}
    for name, va, vs, ra, rs in secs:
        if name != ".text":
            continue
        buf = d[ra:ra + rs]
        for m in re.finditer(b"\xe8", buf):
            i = m.start()
            if i + 5 > len(buf):
                break
            rel = struct.unpack_from("<i", buf, i + 1)[0]
            tgt = va + i + 5 + rel
            if tgt in targets:
                hits[tgt].append(va + i)
    for t, v in hits.items():
        print(hex(t), [hex(x) for x in v])


if __name__ == "__main__":
    main()
