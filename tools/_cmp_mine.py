import struct, sys, math

order = int(sys.argv[1])
goldpath = r"D:\PROJETOS\soultree\checks\.build\j%d_stage_rand.bits" % order
mypath = sys.argv[2]

def load_secs(path):
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
    return secs

def f32(b):
    return struct.unpack("<f", struct.pack("<I", b))[0]

g = load_secs(goldpath)
src = [f32(b) for b in g["SRC"]]
kd = [f32(b) for b in g["KD"]]
mine_bits = []
for line in open(mypath):
    line = line.strip()
    if line:
        mine_bits.append(int(line, 16))
mine = [f32(b) for b in mine_bits]
n = len(kd)
N = n // 2
x = [complex(src[2 * k], src[2 * k + 1]) for k in range(N)]
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

mine_c = [complex(mine[2 * k], mine[2 * k + 1]) for k in range(N)]

# Is mine a permutation of ref magnitudes?
key = {}
for k in range(N):
    key.setdefault(round(abs(a[k]), 3), []).append(k)
hits = 0
for k in range(min(N, 4000)):
    r = round(abs(mine_c[k]), 3)
    if r in key:
        hits += 1
print("magnitude-match in first 4000:", hits)
# ratio test: mine[k]/ref[k] for the first few
for k in range(8):
    print(k, "ref", a[k], "mine", mine_c[k])
