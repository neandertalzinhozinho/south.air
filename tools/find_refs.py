import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib

d = re_lib.data()
T0, T1 = 0x1000, 0x1CD6487


def find_lea(target_rva, limit=40):
    """find RIP-relative lea/mov with disp32 pointing at target_rva"""
    out = []
    for i in range(T0, T1 - 8):
        if d[i] != 0x8D:
            continue
        modrm = d[i + 1]
        if (modrm & 0xC7) != 0x05:
            continue
        if (modrm >> 6) != 0:  # mod must be 00 for rip-rel
            continue
        disp = struct.unpack_from('<i', d, i + 2)[0]
        tgt = i + 6 + disp
        if tgt == target_rva:
            f = re_lib.func_at(i)
            out.append((i, f[0] if f else None))
            if len(out) >= limit:
                break
    return out


if __name__ == '__main__':
    for a in sys.argv[1:]:
        t = int(a, 0)
        print(f'--- refs to 0x{t:X} ---')
        for i, fb in find_lea(t):
            print(f'  0x{i:X} in func 0x{fb:X}' if fb else f'  0x{i:X}')
