import json, struct

d = json.load(open(r"D:\PROJETOS\shadowFILES\analysis\parameter_table.json", encoding="utf-8"))
for p in d["parameters"][:5]:
    raw = bytes.fromhex(p["raw_record_hex"])
    rid = struct.unpack_from("<I", raw, 0x00)[0]
    name = raw[0x04:0x04+36].split(b"\0")[0].decode("ascii", "replace")
    mn = struct.unpack_from("<d", raw, 0x28)[0]
    mx = struct.unpack_from("<d", raw, 0x30)[0]
    ini = struct.unpack_from("<d", raw, 0x38)[0]
    fl = struct.unpack_from("<Q", raw, 0x40)[0]
    print("id=%d name=%-16s min=%g max=%g init=%g flags=0x%x | json: min=%g max=%g init=%g flags=%s" % (
        rid, name, mn, mx, ini, fl,
        p["minimum"], p["maximum"], p["initial_or_default_candidate"], p["flags_raw_u64"]))
