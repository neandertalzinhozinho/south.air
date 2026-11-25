import mmap, struct, os, sys

path = r"D:\PROJETOS\shadowFILES\soothe3_unpacked_mem.bin"
f = open(path, "rb")
m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
data_len = len(m)
print("dump size", data_len)

# scan for PE signatures with plausible headers
cands = []
pos = 0
while True:
    pos = m.find(b"MZ", pos)
    if pos < 0:
        break
    pos += 1
    if pos + 0x40 > data_len:
        continue
    e_lfanew = struct.unpack_from("<I", m, pos + 0x3C)[0]
    if e_lfanew <= 0 or pos + e_lfanew + 0x100 > data_len:
        continue
    if m[pos + e_lfanew:pos + e_lfanew + 4] != b"PE\0\0":
        continue
    machine, nsec = struct.unpack_from("<HH", m, pos + e_lfanew + 4)
    opts = pos + e_lfanew + 0x18
    magic = struct.unpack_from("<H", m, opts)[0]
    if magic != 0x20B:
        continue
    sizeofimage = struct.unpack_from("<I", m, opts + 56)[0]
    cands.append((pos, machine, nsec, sizeofimage))

print("PE32+ candidates:", len(cands))
for c in cands:
    if 0x1800000 < c[3] < 0x4000000 or c[3] > 0x1800000:
        print("  off=%#x machine=%#x nsec=%d SizeOfImage=%#x" % c)

# target: image size close to the plugin
want = [c for c in cands if abs(c[3] - 0x1D90000) < 0x200000]
print("near-plugin candidates:", [(hex(c[0]), hex(c[3])) for c in want])
