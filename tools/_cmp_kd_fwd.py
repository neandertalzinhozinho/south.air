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

kd = [f32(b) for b in secs["KD"]]
fwd = [f32(b) for b in secs["FWD"]]
n = len(kd)
print("n", n, "FWD len", len(fwd))
bad = 0
for i in range(n):
    if secs["KD"][i] != secs["FWD"][i]:
        if bad < 6:
            print(i, hex(secs["KD"][i]), hex(secs["FWD"][i]), kd[i], fwd[i])
        bad += 1
print("KD vs FWD bad", bad, "/", n)
print("FWD tail", [hex(x) for x in secs["FWD"][n:n+4]])
