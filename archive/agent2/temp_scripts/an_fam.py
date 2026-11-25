import json, collections
import numpy as np
from pathlib import Path

C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
A = np.fromfile(C / 'A_r1_data.bin', dtype=np.uint8)
B = np.fromfile(C / 'B_r1_data.bin', dtype=np.uint8)
A1 = [np.fromfile(C / f'A_r{i}_data.bin', dtype=np.uint8) for i in (1,2,3)]
B1 = [np.fromfile(C / f'B_r{i}_data.bin', dtype=np.uint8) for i in (1,2,3)]
va = ~((A1[0]==A1[1]) & (A1[0]==A1[2]))
vb = ~((B1[0]==B1[1]) & (B1[0]==B1[2]))
stable = ~(va|vb)
idx = np.flatnonzero((A!=B) & stable)

# 1. familia "dword com bit 0x80000000 e delta -4"
fam4 = []
for o in idx:
    s = int(o) & ~3
    a4 = int.from_bytes(A[s:s+4].tobytes(),'little')
    b4 = int.from_bytes(B[s:s+4].tobytes(),'little')
    if a4 == (b4 + 4) and (a4 & 0x80000000):
        fam4.append(s)
print('familia A.dword = B.dword + 4 (bit 0x80000000): %d dwords distintos, %d bytes' %
      (len(set(fam4)), len(idx[[int(o)&~3 in set(fam4) for o in idx]])))
print('  valores A:', sorted({int.from_bytes(A[s:s+4].tobytes(),"little") & 0x7fffffff for s in set(fam4)})[:20])

# 2. entropia alta: bloco de 16 B sem zero e com >=12 bytes distintos
def ent(o):
    s = int(o) & ~0xF
    a = A[s:s+16].tobytes(); b = B[s:s+16].tobytes()
    return (0 not in a) and len(set(a)) >= 12 and (0 not in b) and len(set(b)) >= 12
hi = [int(o) for o in idx if ent(o)]
print('\nbytes em blocos de entropia alta (sem zero, >=12 valores distintos): %d em %d blocos' %
      (len(hi), len({o & ~0xF for o in hi})))
print('  faixa: 0x%X .. 0x%X' % (min(hi), max(hi)))

# 3. licenca
lic = [int(o) for o in idx if 0x530000 <= o < 0x540000]
print('\njanela de licenca 0x530000-0x540000: %d bytes' % len(lic))

# 4. resto
resto = [int(o) for o in idx if int(o) not in set(hi) and not (0x530000 <= int(o) < 0x540000)
         and (int(o) & ~3) not in set(fam4)]
print('resto nao classificado: %d bytes' % len(resto))
for o in resto[:30]:
    print('   +0x%07X A=%s B=%s' % (o, A[o:o+8].tobytes().hex(), B[o:o+8].tobytes().hex()))

# 5. teste de deslocamento na faixa de entropia
lo, hi_end = 0x550000, 0x590000
best = []
for s in range(-64, 65):
    if s == 0: continue
    same = 0; tot = 0
    for x in range(lo, hi_end, 1):
        y = x + s
        if lo <= y < hi_end:
            tot += 1
            if A[x] == B[y]: same += 1
    best.append((same / tot, s, tot))
best.sort(reverse=True)
print('\nmelhor alinhamento A[x] == B[x+s] em 0x550000-0x590000:')
for r, s, t in best[:5]:
    print('   s=%+d  igualdade=%.4f (%d amostras)' % (s, r, t))

# 6. strings exclusivas SO na janela de licenca
def st(buf, base, lo, hi, minlen=5):
    out=[];cur=bytearray();start=0
    for i in range(lo, hi):
        c = int(buf[i])
        if 32 <= c < 127:
            if not cur: start = i
            cur.append(c)
        else:
            if len(cur) >= minlen: out.append((start, bytes(cur).decode('ascii')))
            cur = bytearray()
    if len(cur) >= minlen: out.append((start, bytes(cur).decode('ascii')))
    return out
sa = st(A,0,0x530000,0x540000); sb = st(B,0,0x530000,0x540000)
seta={s for _,s in sa}; setb={s for _,s in sb}
print('\nlicenca: strings A=%d B=%d | so em A=%d | so em B=%d' % (len(sa),len(sb),len(seta-setb),len(setb-seta)))
for o,s in sa:
    if s not in setb: print('   A-only +0x%07X %r' % (o,s))
for o,s in sb:
    if s not in seta: print('   B-only +0x%07X %r' % (o,s))
