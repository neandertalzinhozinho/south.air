import numpy as np, pefile, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86_const import X86_REG_RIP

P = r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\final_candidate_uni46c.vst3"
pe = pefile.PE(P, fast_load=True)
raw = open(P, "rb").read()
BASE = 0x180000000

secs = {}
for s in pe.sections:
    n = s.Name.rstrip(b"\x00").decode()
    secs[n] = (s.VirtualAddress, s.Misc_VirtualSize, s.PointerToRawData, s.SizeOfRawData)

text_va, text_vs, text_pr, text_rs = secs[".text"]
text = raw[text_pr:text_pr + text_vs]

LO, HI = 0x217F000, 0x2760000
disp = np.frombuffer(text[3:], dtype="<i4")
base_idx = np.arange(len(disp), dtype=np.int64)
cand = []
for L in range(5, 12):
    start = base_idx - (L - 4)
    ok = start >= 0
    tgt = start + L + disp
    ok &= (tgt >= LO) & (tgt < HI)
    for i in np.nonzero(ok)[0]:
        cand.append((int(start[i]) + text_va, int(tgt[i])))

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
out = []
seen = set()
for rva, _t in cand:
    if rva in seen:
        continue
    off = rva - text_va
    if off < 0 or off + 15 > len(text):
        continue
    it = md.disasm(text[off:off + 15], BASE + rva)
    try:
        ins = next(it)
    except StopIteration:
        continue
    for op in ins.operands:
        if op.type == 3 and op.mem.base == X86_REG_RIP:
            t = (ins.address + ins.size + op.mem.disp) - BASE
            if LO <= t < HI:
                seen.add(rva)
                out.append((rva, t, ins.mnemonic + " " + ins.op_str))

print("verified refs", len(out))
json.dump([{"rva": hex(a), "target": hex(t), "insn": s} for a, t, s in out],
          open(r"D:\PROJETOS\shadowFILES\analysis\startup_audit\pace_free\state_xrefs.json", "w"), indent=1)

from collections import Counter
c = Counter(t for _, t, _ in out)
print("distinct targets", len(c))
print("top", [(hex(k), v) for k, v in c.most_common(15)])
