import json, struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

ROOT = Path(r'D:\PROJETOS\shadowFILES')
data = (ROOT/'soothe3_unpacked_mem.bin').read_bytes()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True

units = []
for rp in (ROOT/'analysis/recovered_native/units').glob('rva_*/roundtrip.json'):
    j = json.loads(rp.read_text())
    if not j.get('byte_identical'):
        continue
    units.append((int(j['start'],16), int(j['end_exclusive'],16)))
units.sort()
print('units', len(units), 'bytes', sum(e-s for s,e in units))

TGT_LO, TGT_HI = 0x7b0a900, 0x7b0ab00
indirect = {}
hits=[]
for s,e in units:
    code = data[s:e]
    va = 0x18CC0000+s
    for i in md.disasm(code, va):
        for op in i.operands:
            if op.type == X86_OP_MEM and op.mem.base == X86_REG_RIP:
                t = i.address + i.size + op.mem.disp - 0x18CC0000
                if TGT_LO <= t < TGT_HI:
                    hits.append((i.address-0x18CC0000, i.mnemonic, i.op_str, t, i.bytes.hex()))
                if i.mnemonic in ('call','jmp') and op.size == 8:
                    indirect.setdefault(t, []).append(i.address-0x18CC0000)

print('=== xrefs into 0x7b0a900..0x7b0ab00 ===')
for h in hits[:200]:
    print(f'{h[0]:#x}: {h[1]} {h[2]} -> {h[3]:#x}  bytes={h[4]}')
print('total hits',len(hits))
print('=== indirect call/jmp [rip+..] slots (count) ===')
for t,v in sorted(indirect.items()):
    print(f'{t:#x}: {len(v)} sites, first {[hex(x) for x in v[:4]]}')
