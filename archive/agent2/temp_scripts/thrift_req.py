import json, struct, sys

p = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\final_candidate_uni46c.vst3.edenmulti.json"
d = json.load(open(p))
h = [e for e in d["events"] if e["kind"] == "recv"][0]["data"]
b = bytes.fromhex(h)
print("total", len(b))
print(b[:8].hex())
n = struct.unpack_from(">i", b, 4)[0]
print("name len", n, "name", b[8:8+n])
i = 8 + n
print("seqid", struct.unpack_from(">i", b, i)[0]); i += 4

TYPES = {2:"BOOL",3:"BYTE",4:"DOUBLE",6:"I16",8:"I32",10:"I64",11:"STR",12:"STRUCT",13:"MAP",14:"SET",15:"LIST"}

def val(t, depth):
    global i
    if t == 2:
        v = b[i]; i += 1; return bool(v)
    if t == 3:
        v = b[i]; i += 1; return v
    if t == 8:
        v = struct.unpack_from(">i", b, i)[0]; i += 4; return v
    if t == 10:
        v = struct.unpack_from(">q", b, i)[0]; i += 8; return v
    if t == 11:
        k = struct.unpack_from(">i", b, i)[0]; i += 4
        s = b[i:i+k]; i += k; return s
    if t in (12,):
        return struct_(depth)
    if t == 15:
        et = b[i]; i += 1
        k = struct.unpack_from(">i", b, i)[0]; i += 4
        return "list<%s>[%d]" % (TYPES.get(et, et), k), [val(et, depth+1) for _ in range(k)]
    raise SystemExit("unhandled type %d at %d" % (t, i))

def struct_(depth):
    global i
    out = []
    while True:
        t = b[i]; i += 1
        if t == 0:
            return ("STRUCTEND", out)
        fid = struct.unpack_from(">h", b, i)[0]; i += 2
        v = val(t, depth+1)
        if isinstance(v, tuple) and v and v[0] == "list<%s>[%d]":
            out.append((fid, TYPES.get(t, t), v[0], v[1]))
        else:
            out.append((fid, TYPES.get(t, t), v))

r = struct_(0)
for f in r[1]:
    print(f)
print("pos", i, "len", len(b), "tail", b[i:].hex())

