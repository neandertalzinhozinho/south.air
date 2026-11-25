from pathlib import Path
import hashlib

ROOT = Path(r"D:\PROJETOS\shadowFILES")
mem = ROOT / "soothe3_unpacked_mem.bin"
pe_fixed = ROOT / "soothe3_unpacked_fixed.pe"
plugin = ROOT / "analysis" / "startup_audit" / "pace_free" / "final_candidate_uni46c.vst3"

print("mem size", mem.stat().st_size)
with open(mem, "rb") as f:
    head = f.read(64)
print("mem head", head[:32].hex(), "MZ?", head[:2] == b"MZ")

with open(pe_fixed, "rb") as f:
    h2 = f.read(2)
print("pe_fixed MZ?", h2 == b"MZ", pe_fixed.stat().st_size)

RVAS = {
    "caller_18ea150": 0x18EA150,
    "connector_19be440": 0x19BE440,
    "tpipe_open_198bd90": 0x198BD90,
    "selfcrc_330370": 0x330370,
    "fail_exit_19bf519": 0x19BF519,
    "fatal_17f1300": 0x17F1300,
    "onexit_cb_181f760": 0x181F760,
}

pdata = plugin.read_bytes()
mdata = mem.read_bytes()
p2 = pe_fixed.read_bytes() if pe_fixed.exists() else b""

print(f"{'label':<24} {'file':<34} {'mem':<34} same?")
for label, rva in RVAS.items():
    fo = rva  # image dump: header-inclusive linear mapping
    a = pdata[rva:rva + 16] if rva + 16 <= len(pdata) else b""
    b = mdata[fo:fo + 16] if fo + 16 <= len(mdata) else b""
    print(f"{label:<24} {a.hex():<34} {b.hex():<34} {a == b}")

# global diff statistics over .text
import struct, pefile
pe = pefile.PE(str(plugin), fast_load=True)
for s in pe.sections:
    name = s.Name.rstrip(b"\0").decode("latin1")
    if name not in (".text", "IPPCODE"):
        continue
    va, raw, rs = s.VirtualAddress, s.PointerToRawData, s.SizeOfRawData
    fseg = pdata[raw:raw + rs]
    mseg = mdata[va:va + len(fseg)]
    if len(mseg) != len(fseg):
        print(name, "mem too short", len(mseg), len(fseg))
        continue
    diff = sum(1 for x, y in zip(fseg, mseg) if x != y)
    print(f"{name}: bytes={len(fseg):,} diff={diff:,} ({diff/len(fseg)*100:.2f}%)")
