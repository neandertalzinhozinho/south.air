import struct, sys

path = r"D:\PROJETOS\soultree\checks\.build\j%s_stage_rand.bits" % sys.argv[1]
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
n = len(src)
re = sum(src[0::2])
im = sum(src[1::2])
print("n", n, "counts", {k: len(v) for k, v in secs.items()})
print("sum even (double) =", re, " KD[0] =", kd[0], " diff", re - kd[0])
print("sum odd  (double) =", im, " KD[1] =", kd[1], " diff", im - kd[1])
# check kd magnitude plausibility
print("max|kd|", max(abs(v) for v in kd[:200]))
