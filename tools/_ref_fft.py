import struct, sys, cmath

order = int(sys.argv[1])
path = r"D:\PROJETOS\soultree\checks\.build\j%d_stage_rand.bits" % order
secs = {}
cur = None
for line in open(path):
    line = line.rstrip("\n")
    if line.startswith("#"):
        continue
    if len(line) >= 8 and all(c in "0123456789abcdef" for c in line.lower()):
        secs[cur].append(int(line, 16))
    elif line:
        cur = line
        secs[cur] = []

def f32(b):
    return struct.unpack("<f", struct.pack("<I", b))[0]

src = [f32(b) for b in secs["SRC"]]
kd = [f32(b) for b in secs["KD"]]
n = len(kd)
# complex input pairs
x = [complex(src[2 * k], src[2 * k + 1]) for k in range(n // 2)]
N = len(x)
# iterative radix-2 FFT
import math
j = 0
a = x[:]
for i in range(1, N):
    bit = N >> 1
    while j & bit:
        j ^= bit
        bit >>= 1
    j ^= bit
    if i < j:
        a[i], a[j] = a[j], a[i]
length = 2
while length <= N:
    ang = -2 * math.pi / length
    wl = complex(math.cos(ang), math.sin(ang))
    half = length // 2
    for i in range(0, N, length):
        w = 1 + 0j
        for k in range(half):
            u = a[i + k]
            v = a[i + k + half] * w
            a[i + k] = u + v
            a[i + k + half] = u - v
            w *= wl
    length <<= 1

# compare KD (interleaved re,im) to a
maxerr = 0.0
bad = 0
for k in range(N):
    er = abs(a[k].real - kd[2 * k])
    ei = abs(a[k].imag - kd[2 * k + 1])
    e = max(er, ei)
    if e > maxerr:
        maxerr = e
    if e > 1e-3:
        if bad < 5:
            print("k", k, "ref", a[k], "kd", kd[2 * k], kd[2 * k + 1])
        bad += 1
print("order", order, "N", N, "maxerr", maxerr, "bad", bad)
