"""A12: exhaustive STATIC scan of indirect call/jmp thunks in dump + DLL.

READ-ONLY on all repo inputs. Outputs to temp only.
"""
import json
import re
import struct
import sys
from collections import defaultdict
from pathlib import Path

import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import (X86_OP_MEM, X86_OP_REG, X86_REG_RIP,
                          X86_INS_CALL, X86_INS_JMP, X86_INS_MOV,
                          X86_INS_MOVSXD, X86_INS_LEA)

ROOT = Path(r'D:\PROJETOS\shadowFILES')
DUMP = ROOT / 'soothe3_unpacked_mem.bin'
DLL = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.dll'
MAPF = ROOT / 'analysis/recovered_native/testdll/recovered_dsp_test.map'
OUT = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode\a12_results.json')

DUMP_BASE = 0x180000000       # RVA == offset in dump (per coordinator)
NTDLL_BASE_CAPTURED = 0x7ffaea750000
AV_TARGET_VA = NTDLL_BASE_CAPTURED + 0x17fe00   # 0x7ffaea8cfe00

print('[A12] loading dump ...', flush=True)
dump = DUMP.read_bytes()
pe = pefile.PE(str(DLL), fast_load=False)
dll = pe.__data__
IB = pe.OPTIONAL_HEADER.ImageBase

# ------------------------------------------------------------------ symbols
sym2rva = {}
rva2sym = []
for line in MAPF.read_text(errors='replace').splitlines():
    m = re.match(r'\s*000[12]:([0-9a-f]+)\s+(\S+)\s+([0-9a-fA-F]+)\s+\w', line)
    if m:
        sym = m.group(2)
        addr = int(m.group(3), 16)
        rva = addr - IB
        sym2rva[sym] = rva
        rva2sym.append((rva, sym))
rva2sym.sort()


def nearest_sym(rva):
    lo, hi = 0, len(rva2sym)
    while lo < hi:
        mid = (lo + hi) // 2
        if rva2sym[mid][0] <= rva:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return '?+0x%x' % rva
    s, d = rva2sym[lo - 1]
    return '%s+0x%x' % (s, rva - s)


# dump symbols: unit directories rva_XXXXXXXX -> dump offset XXXXXXXX
unit_starts = sorted(int(p.name[4:], 16) for p in
                     (ROOT / 'analysis/recovered_native/units').iterdir()
                     if p.is_dir() and re.fullmatch(r'rva_[0-9a-f]+', p.name))


def nearest_dumpsym(off):
    lo, hi = 0, len(unit_starts)
    while lo < hi:
        mid = (lo + hi) // 2
        if unit_starts[mid] <= off:
            lo = mid + 1
        else:
            hi = mid
    if lo == 0:
        return 'dump_?+0x%x' % off
    s = unit_starts[lo - 1]
    return 'dump_%x+0x%x' % (s, off - s)


# ------------------------------------------------------------------ helpers
def qwords_at(data, off):
    if 0 <= off <= len(data) - 8:
        return struct.unpack_from('<Q', data, off)[0]
    return None


def dll_off(rva):
    try:
        return pe.get_offset_from_rva(rva)
    except Exception:
        return None


def classify(v):
    if v is None:
        return 'unreadable'
    if v == 0:
        return 'NULL'
    if 0x7FF000000000 <= v < 0x800000000000:
        return 'STALE_USER_VA'
    if (v & 0xFFFFFF) == 0x17fe00:
        return 'LOW24_17FE00'
    if v == AV_TARGET_VA:
        return 'EXACT_AV_TARGET'
    if IB <= v < IB + len(dll):
        return 'DLL_VA'
    if 0 <= v < len(dump):
        return 'DUMP_OFFSET'
    return 'OTHER'


def readq(data_base, data, addr):
    """addr is an absolute address (VA for DLL, offset for dump)."""
    if data_base == 'dll':
        rva = addr - IB
        off = dll_off(rva)
        if off is None:
            return None
        return qwords_at(dll, off)
    else:
        return qwords_at(dump, addr)


# ------------------------------------------------------------------ disasm
MD = Cs(CS_ARCH_X86, CS_MODE_64)
MD.detail = True


def scan_region(data, start, end, base_addr, flavor, symfn):
    """Linear disassembly; find indirect transfer instructions."""
    out = []
    prev = None
    try:
        insns = MD.disasm(data[start:end], base_addr + start)
        for ins in insns:
            rec = None
            if ins.id in (X86_INS_CALL, X86_INS_JMP) and ins.operands:
                op = ins.operands[0]
                if op.type == X86_OP_MEM:
                    mem = op.mem
                    if mem.base == X86_REG_RIP:
                        target = ins.address + ins.size + mem.disp
                    else:
                        target = None
                    v = readq(flavor, data, target) if target is not None else None
                    rec = {
                        'kind': ('jmp_mem_rip' if ins.id == X86_INS_JMP else 'call_mem_rip')
                                if mem.base == X86_REG_RIP else
                                ('jmp_mem_reg' if ins.id == X86_INS_JMP else 'call_mem_reg'),
                        'ins': ins.mnemonic + ' ' + ins.op_str,
                        'target': hex(target) if target is not None else None,
                        'value': hex(v) if v is not None else None,
                        'vclass': classify(v),
                        'regs': ('base=' + (ins.reg_name(mem.base) or '-') +
                                 ' idx=' + (ins.reg_name(mem.index) or '-') +
                                 ' scale=' + str(mem.scale) +
                                 ' disp=' + hex(mem.disp & 0xffffffffffffffff)),
                    }
            # mov r64,[rip+disp]  followed by jmp r64
            if rec is None and ins.id in (X86_INS_MOV, X86_INS_MOVSXD) and ins.operands:
                dst, src = ins.operands[0], ins.operands[1]
                if (dst.type == X86_OP_REG and src.type == X86_OP_MEM and
                        src.mem.base == X86_REG_RIP):
                    regname = ins.reg_name(dst.reg)
                    # store pending; handled on next iteration
                    out.append({  # placeholder filtered later
                        '_pending': True, 'addr': hex(ins.address), 'reg': regname,
                        'target': ins.address + ins.size + src.mem.disp,
                        'flavor': flavor, 'sym': symfn(ins.address - (0 if flavor == 'dump' else IB)),
                        'ins': ins.mnemonic + ' ' + ins.op_str,
                    })
            if rec is not None:
                rva = ins.address - (0 if flavor == 'dump' else IB)
                rec.update({'addr': hex(ins.address), 'rva': hex(rva),
                            'sym': symfn(rva), 'bytes': ins.bytes.hex()})
                out.append(rec)
    except Exception as e:
        print('  disasm error', flavor, hex(start), repr(e), flush=True)
    return out


# pending mov->jmp resolution across all records
def resolve_mov_jmp(records, data, flavor):
    pend = [r for r in records if r.get('_pending')]
    direct = [r for r in records if not r.get('_pending')]
    byaddr = {int(r['addr'], 16): r for r in direct}
    res = []
    for p in pend:
        # look for a jmp reg within next 8 bytes at same flavor
        for delta in range(1, 9):
            nxt = byaddr.get(int(p['addr'], 16) + delta)
            if nxt and nxt['kind'] == 'jmp_mem_reg' and p['reg'] in nxt['ins'].split()[-1]:
                v = readq(flavor, data, p['target'])
                res.append({
                    'kind': 'mov_rip_jmp_reg',
                    'addr': p['addr'], 'rva': p['rva'], 'sym': p['sym'],
                    'ins': p['ins'] + ' ; ' + nxt['ins'],
                    'bytes': '', 'target': hex(p['target']),
                    'value': hex(v) if v is not None else None,
                    'vclass': classify(v),
                    'regs': p['reg'],
                })
                break
    return direct + res


print('[A12] scanning DLL executable sections ...', flush=True)
dll_thunks = []
for s in pe.sections:
    if s.Characteristics & 0x20000000:  # MEM_EXECUTE
        st, en = s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData
        dll_thunks += scan_region(dll, st, en, IB + s.VirtualAddress - s.PointerToRawData,
                                  'dll', nearest_sym)
dll_thunks = resolve_mov_jmp(dll_thunks, dll, 'dll')
print('[A12] DLL thunks:', len(dll_thunks), flush=True)

# dump code region (from scan_indirect_slots.py: .text 0x1000 .. 0x1CD5800)
print('[A12] scanning DUMP .text ...', flush=True)
dump_thunks = scan_region(dump, 0x1000, 0x1CD5800, 0, 'dump', nearest_dumpsym)
dump_thunks = resolve_mov_jmp(dump_thunks, dump, 'dump')
print('[A12] DUMP thunks:', len(dump_thunks), flush=True)

# ------------------------------------------------------------------ byte prescan (exhaustive)
print('[A12] byte-level prescan for FF /2 FF /4 ...', flush=True)
byte_candidates = defaultdict(int)
for pat in (b'\xff\x15', b'\xff\x25', b'\x41\xff\x24', b'\x49\xff\x24',
            b'\xff\x14', b'\xff\x24', b'\x48\x8b\x05', b'\x4c\x8b\x05'):
    i = 0
    while True:
        i = dump.find(pat, i)
        if i < 0:
            break
        byte_candidates[pat.hex()] += 1
        i += 1

# ------------------------------------------------------------------ mask scans
print('[A12] mask scans ...', flush=True)
mask_hits = defaultdict(list)


def scan_values(data, tag, limit=200000):
    # chunked to avoid materialising ~17M Python ints from the 137 MB dump
    CHUNK = 1 << 20  # 1 MiB, multiple of 8
    for base in range(0, len(data) - 7, CHUNK):
        end = min(base + CHUNK, len(data))
        end -= (end - base) % 8
        n = (end - base) // 8
        vals = struct.unpack_from('<%dQ' % n, data, base)
        for i, v in enumerate(vals):
            off = base + i * 8
            if (v & 0xFFFFFF) == 0x17fe00:
                mask_hits['low24_17fe00_' + tag].append((off, v))
            if v == AV_TARGET_VA:
                mask_hits['exact_av_target_' + tag].append((off, v))
            if (v & 0xFFFFFFFFFFFF0000) == (AV_TARGET_VA & 0xFFFFFFFFFFFF0000):
                mask_hits['av_page_' + tag].append((off, v))
            if (v & 0xFFFF) == 0xfe00 and ((v >> 16) & 0xFF) == 0x17:
                mask_hits['bytes_00fe17_' + tag].append((off, v))
            if 0x7FF000000000 <= v < 0x800000000000 and (v & 0xFFFF) == 0xfe00:
                mask_hits['user_fe00_' + tag].append((off, v))
            if (v & 0xFFFF000000000000) == 0xFFFF000000000000 and (v & 0xFFFFFF) == 0x17fe00:
                mask_hits['kernel_ffff_low24_' + tag].append((off, v))


scan_values(dump, 'dump')
scan_values(dll, 'dll')

# raw 8-byte pattern scan (unaligned) 00 FE 17 ?? ?? ?? FF FF
rawpat = re.compile(b'\x00\xfe\x17...\xff\xff', re.DOTALL)
raw_hits = {'dump': [], 'dll': []}
for tag, data in (('dump', dump), ('dll', dll)):
    for m in rawpat.finditer(data):
        if len(raw_hits[tag]) < 500:
            raw_hits[tag].append((m.start(), data[m.start():m.start() + 8].hex()))

# ------------------------------------------------------------------ report
def slim(recs, maxn=100000):
    return recs[:maxn]


results = {
    'meta': {
        'dump_len': hex(len(dump)), 'dll_len': hex(len(dll)), 'imagebase': hex(IB),
        'ntdll_base_captured': hex(NTDLL_BASE_CAPTURED),
        'av_target_va': hex(AV_TARGET_VA),
        'dll_thunk_count': len(dll_thunks), 'dump_thunk_count': len(dump_thunks),
        'byte_candidates': dict(byte_candidates),
    },
    'dll_thunks': slim(dll_thunks),
    'dump_thunks': slim(dump_thunks),
    'mask_hits': {k: v[:1000] for k, v in mask_hits.items()},
    'raw_pattern_hits': raw_hits,
    'key_symbols': {s: hex(sym2rva[s]) for s in
                    ('dump_8701c0', 'dump_879210', 'dump_8798f0', 'dump_87a020',
                     'dump_1c84a0', 'dump_1c84d0', 'dump_1100', 'dump_3480') if s in sym2rva},
}
OUT.write_text(json.dumps(results, indent=1))
print('[A12] wrote', OUT, flush=True)

# ------------------------------------------------------------------ console summary
print('\n=== meta ===')
print(json.dumps(results['meta'], indent=1))
print('\n=== key symbols ===')
print(json.dumps(results['key_symbols'], indent=1))
for k, v in mask_hits.items():
    print('\n=== %s : %d hits ===' % (k, len(v)))
    for off, val in v[:30]:
        print('   off=%#x val=%#018x sym=%s' % (off, val,
              nearest_sym(off - IB) if k.endswith('dll') else nearest_dumpsym(off)))
for k, v in raw_hits.items():
    print('\n=== raw pattern %s: %d hits, first 20 ===' % (k, len(v)))
    for off, hx in v[:20]:
        print('   %#x %s' % (off, hx))
print('\n=== DLL thunks by class ===')
c = defaultdict(int)
for r in dll_thunks:
    c[r['vclass']] += 1
print(dict(c))
print('\n=== DUMP thunks by class ===')
c = defaultdict(int)
for r in dump_thunks:
    c[r['vclass']] += 1
print(dict(c))
print('\n=== DLL stale/thunk entries (first 60) ===')
n = 0
for r in dll_thunks:
    if r['vclass'] in ('STALE_USER_VA', 'LOW24_17FE00', 'EXACT_AV_TARGET', 'NULL'):
        print(' ', r['sym'], r['kind'], r['ins'], '->', r['target'], r['value'], r['vclass'])
        n += 1
        if n >= 60:
            break
print('\n=== DUMP stale/thunk entries (first 60) ===')
n = 0
for r in dump_thunks:
    if r['vclass'] in ('STALE_USER_VA', 'LOW24_17FE00', 'EXACT_AV_TARGET'):
        print(' ', r['sym'], r['kind'], r['ins'], '->', r['target'], r['value'], r['vclass'])
        n += 1
        if n >= 60:
            break
