import json
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
A = (C / 'A_r1_data.bin').read_bytes()
B = (C / 'B_r1_data.bin').read_bytes()
A1 = (C / 'A_r1_data001.bin').read_bytes()
B1 = (C / 'B_r1_data001.bin').read_bytes()
AR = (C / 'A_r1_rdata01.bin').read_bytes()
BR = (C / 'B_r1_rdata01.bin').read_bytes()

def diffs(a, b, lo=0, hi=None):
    hi = hi or len(a)
    return [i for i in range(lo, hi) if a[i] != b[i]]

d = diffs(A, B)
print('total .data diffs:', len(d))

# janela de licenca
lo, hi = 0x530000, 0x540000
w = diffs(A, B, lo, hi)
print('\n--- licenca .data+0x530000..0x540000 ---')
print('nao-zero A:', sum(1 for x in A[lo:hi] if x), '| B:', sum(1 for x in B[lo:hi] if x))
print('diffs:', len(w), 'primeiros:', [hex(x) for x in w[:12]], 'ultimos:', [hex(x) for x in w[-6:]])

def strings(buf, minlen=6):
    out, cur, start = [], bytearray(), 0
    for i, c in enumerate(buf):
        if 32 <= c < 127:
            if not cur: start = i
            cur.append(c)
        else:
            if len(cur) >= minlen: out.append((start, cur.decode('ascii')))
            cur = bytearray()
    if len(cur) >= minlen: out.append((start, cur.decode('ascii')))
    return out

sa = strings(A[lo:hi]); sb = strings(B[lo:hi])
print('strings A (%d):' % len(sa))
for o, s in sa[:10]: print('   +0x%X %r' % (lo + o, s))
print('strings B (%d):' % len(sb))
for o, s in sb[:10]: print('   +0x%X %r' % (lo + o, s))

# valores nos offsets que diferem, agrupados
import collections
blk = collections.Counter(x // 16 for x in w)
print('\nblocos de 16B com diff (licenca):', len(blk))
for k, v in sorted(blk.items())[:8]:
    off = lo + k * 16
    print('   +0x%X  %d B | A=%s | B=%s' % (off, v, A[off:off+16].hex(), B[off:off+16].hex()))

print('\n--- .data001 ---')
d1 = diffs(A1, B1)
print('diffs:', len(d1), '| primeiro 0x%X ultimo 0x%X' % (d1[0], d1[-1]) if d1 else '')
for x in d1[:6]:
    off = x & ~0xF
    print('   +0x%X A=%s B=%s' % (off, A1[off:off+16].hex(), B1[off:off+16].hex()))

print('\n--- .rdata01 ---')
dr = diffs(AR, BR)
print('diffs:', len(dr), [hex(x) for x in dr])
for x in dr:
    off = x & ~0xF
    print('   +0x%X A=%s B=%s' % (off, AR[off:off+16].hex(), BR[off:off+16].hex()))
