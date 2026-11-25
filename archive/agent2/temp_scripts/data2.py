import sys, struct
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64); md.detail = True
BASE = re_lib.BASE


def hexs(o, n=32):
    return d[o:o + n].hex(' ', 4)


def floats(o, n=8):
    return [round(v, 6) for v in struct.unpack_from('<%df' % n, d, o)]


def doubles(o, n=6):
    return [round(v, 9) for v in struct.unpack_from('<%dd' % n, d, o)]


print('== string target of getName lea')
for t in (0x2177FD8,):
    print(hex(t), repr(re_lib.cstr(t, 32)))

print('== 0x490480')
f = re_lib.func_at(0x490480)
print('func', f and (hex(f[0]), f[1] - f[0]))
k = 0
for ins in md.disasm(d[f[0]:f[1]], f[0]):
    print('   ', ins.address, ins.mnemonic, ins.op_str)
    k += 1
    if k > 25: break

print('== window 0x1DF3F80 floats', floats(0x1DF3F80, 10))
print('   raw', hexs(0x1DF3F80, 32))
print('== window 0x2037240 floats', floats(0x2037240, 10))
print('   raw', hexs(0x2037240, 32))

print('== abs pointers to windows in .data/.rdata')
for wt in (0x1DF3F80, 0x2037240):
    pat = struct.pack('<Q', BASE + wt)
    hits = []
    off = 0x1D8C000
    while True:
        i = d.find(pat, off, 0x2757DD8)
        if i < 0: break
        hits.append(i)
        off = i + 1
        if len(hits) > 12: break
    print(f'  0x{wt:X}: {[hex(h) for h in hits]}')

print('== table 0x23926F8 (member ctor arg) first bytes', hexs(0x23926F8, 48))
print('== 0x32AEC0 (param helper)')
f = re_lib.func_at(0x32AEC0)
print('func', f and (hex(f[0]), f[1] - f[0]))
for ins in md.disasm(d[f[0]:f[1]], f[0]):
    print('   ', ins.address, ins.mnemonic, ins.op_str)
