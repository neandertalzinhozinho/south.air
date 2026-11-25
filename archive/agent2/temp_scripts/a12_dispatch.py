"""A12 part 2: enumerate jump-table dispatchers (jmp [reg+idx*8]) in dump + DLL."""
import re
import struct
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_REG_RIP

ROOT = Path(r'D:\PROJETOS\shadowFILES')
dump = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
pe = pefile.PE(str(ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'))
dll = pe.__data__
IB = pe.OPTIONAL_HEADER.ImageBase
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True

# symbol maps
sym2rva = {}
for line in (ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.map').read_text(errors='replace').splitlines():
    m = re.match(r'\s*000[12]:[0-9a-f]+\s+(\S+)\s+([0-9a-fA-F]+)\s+\w', line)
    if m:
        sym2rva[m.group(1)] = int(m.group(2), 16) - IB
rsyms = sorted((v, k) for k, v in sym2rva.items())


def nsym(rva):
    import bisect
    i = bisect.bisect_right([x[0] for x in rsyms], rva) - 1
    if i < 0:
        return '?+0x%x' % rva
    return '%s+0x%x' % (rsyms[i][1], rva - rsyms[i][0])


def dq(data, off):
    return struct.unpack_from('<Q', data, off)[0] if 0 <= off <= len(data) - 8 else None


def dd(data, off):
    return struct.unpack_from('<I', data, off)[0] if 0 <= off <= len(data) - 4 else None


def scan(data, sections, flavor):
    """sections: list of (start_file_off, end_file_off, base_address)."""
    out = []
    for st, en, base in sections:
        try:
            for ins in MD.disasm(data[st:en], base + st):
                if ins.id == 0x29 or (ins.mnemonic == 'jmp' and ins.operands and
                                       ins.operands[0].type == X86_OP_MEM and
                                       ins.operands[0].mem.scale in (2, 4, 8) and
                                       ins.operands[0].mem.base != X86_REG_RIP):
                    addr = ins.address
                    # search previous 32 bytes for movsxd rax,[rip] and lea r10,[rip]
                    prev = data[max(0, addr - base - 48):addr - base]
                    idx_target = tbl_target = None
                    for p in MD.disasm(prev, addr - base - len(prev) + base):
                        if p.mnemonic in ('movsxd', 'mov') and p.operands and p.operands[-1].type == X86_OP_MEM \
                                and p.operands[-1].mem.base == X86_REG_RIP:
                            idx_target = p.address + p.size + p.operands[-1].mem.disp
                        if p.mnemonic == 'lea' and len(p.operands) == 2 and p.operands[1].type == X86_OP_MEM \
                                and p.operands[1].mem.base == X86_REG_RIP:
                            tbl_target = p.address + p.size + p.operands[1].mem.disp
                    rva = addr - base if flavor == 'dll' else addr
                    if flavor == 'dll':
                        idxv = dd(dll, pe.get_offset_from_rva(idx_target - IB)) if idx_target else None
                        slots = []
                        if tbl_target:
                            to = pe.get_offset_from_rva(tbl_target - IB)
                            slots = [dq(dll, to + 8*k) for k in range(8)] if to is not None else []
                    else:
                        idxv = dd(dump, idx_target) if idx_target else None
                        slots = [dq(dump, tbl_target + 8*k) for k in range(8)] if tbl_target else []
                    out.append({
                        'addr': hex(addr), 'rva': hex(rva),
                        'sym': nsym(rva) if flavor == 'dll' else 'dump+0x%x' % rva,
                        'ins': ins.mnemonic + ' ' + ins.op_str,
                        'idx_slot': hex(idx_target) if idx_target else None,
                        'idx_value': hex(idxv) if idxv is not None else None,
                        'table': hex(tbl_target) if tbl_target else None,
                        'slots': [hex(x) if x is not None else None for x in slots],
                        'selected': hex(slots[idxv & 7]) if (slots and idxv is not None and idxv & 7 < len(slots)) else None,
                    })
        except Exception as e:
            print('err', flavor, repr(e))
    return out

print('[A12] DLL dispatchers ...', flush=True)
ds = scan(dll, [(s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData,
                 IB + s.VirtualAddress - s.PointerToRawData)
                for s in pe.sections if s.Characteristics & 0x20000000], 'dll')
print('[A12] DUMP dispatchers ...', flush=True)
us = scan(dump, [(0x1000, 0x1CD5800, 0)], 'dump')
print('DLL dispatchers:', len(ds), 'DUMP dispatchers:', len(us))

out = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\a12_dispatch.json')
out.write_text(__import__('json').dumps({'dll': ds, 'dump': us}, indent=1))
print('wrote', out)

for tag, arr in (('DLL', ds), ('DUMP', us)):
    print('\n=== %s dispatchers ===' % tag)
    for x in arr:
        print('%s %-26s idx_slot=%s idx=%s table=%s sel=%s' %
              (x['rva'], x['sym'], x['idx_slot'], x['idx_value'], x['table'], x['selected']))
