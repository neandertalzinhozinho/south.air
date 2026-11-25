"""Robust .dis reader: handles UTF-8 BOM, UTF-16LE/BE with or without BOM."""
from pathlib import Path


def rd(path):
    raw = Path(path).read_bytes()
    if raw[:3] == b"\xef\xbb\xbf":
        return raw.decode("utf-8-sig", errors="replace")
    if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return raw.decode("utf-16", errors="replace")
    # BOM-less UTF-16LE: lots of NUL bytes in odd positions
    if len(raw) > 8 and raw[1::2].count(0) > len(raw) // 4:
        return raw.decode("utf-16-le", errors="replace")
    return raw.decode("utf-8", errors="replace")


if __name__ == "__main__":
    import sys

    print(rd(sys.argv[1]))
