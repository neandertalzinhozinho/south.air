"""Agente 5 — auditoria v2: refs stale delta>0 + frames de prologo (SOMENTE LEITURA)."""
import datetime
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r'D:\PROJETOS\shadowFILES')
UNITS = ROOT / 'analysis/recovered_native/units'
CLOSURE = ROOT / 'analysis/recovered_native/dsp/dependency_build.json'
DUMP = (ROOT / 'soothe3_unpacked_mem.bin').read_bytes()
MD = Cs(CS_ARCH_X86, CS_MODE_64)
closure = json.loads(CLOSURE.read_text())
starts = {int(r['start'], 16) for r in closure if r.get('byte_identical')}

meta = {}
for mf in UNITS.glob('rva_*/roundtrip.json'):
    d = json.loads(mf.read_text())
    s = int(d['start'], 16)
    e = int(d.get('end_exclusive') or d['end'], 16)
    meta[s] = {'dir': mf.parent, 'start': s, 'end': e, 'mtime': mf.stat().st_mtime,
               'bidem': bool(d.get('byte_identical'))}

# janela estavel da reextracao original: 03:02:13..03:07:57 (exclui 6 toques as 03:36)
def in_window(t):
    dt = datetime.datetime.fromtimestamp(t)
    return dt.strftime('%Y-%m-%d') == '2026-11-21' and (
        dt.hour == 3 and (dt.minute == 2 and dt.second >= 13 or dt.minute in (3, 4, 5, 6)
                          or dt.minute == 7 and dt.second <= 57))

reext = sorted([u for u in meta.values() if in_window(u['mtime'])], key=lambda x: x['start'])
print('reextraidas (janela estavel 03:02:13-03:07:57):', len(reext))
print('  byte_identical:', sum(1 for u in reext if u['bidem']))

# frame do prologo: primeiro sub rsp,imm nos primeiros 64 bytes nao-CC
def prologue_frame(s, e, scanbytes=96):
    b = DUMP[s:e]
    off = 0
    while off < len(b) and b[off] == 0xCC:
        off += 1
    code = b[off:off + scanbytes]
    first = None
    for ins in MD.disasm(code, s + off):
        if ins.mnemonic == 'sub' and ins.op_str.startswith('rsp'):
            m = re.search(r'0x([0-9a-fA-F]+)|([0-9a-fA-F]+)h', ins.op_str)
            if m:
                v = int(m.group(1) or m.group(2), 16)
                if m.group(2):
                    v = int(m.group(2), 16)
                first = (v, ins.bytes.hex(), ins.address, ins.mnemonic + ' ' + ins.op_str)
                break
        if ins.address - (s + off) > 64:
            break
    return first, b[:24].hex()

cache = {}
def frame_of(s):
    if s not in cache:
        u = meta.get(s)
        if not u:
            cache[s] = (None, '')
        else:
            cache[s] = prologue_frame(u['start'], u['end'])
    return cache[s]

STALE_RE = re.compile(r'\bdump_([0-9a-fA-F]+)\s*\+\s*0?([0-9a-fA-F]+)h\b')
rows = []
stale_refs_all = 0
for u in reext:
    asm = u['dir'] / 'dsp_entry.asm'
    if not asm.exists():
        continue
    txt = asm.read_text(errors='replace')
    pf, cb = frame_of(u['start'])
    for m in STALE_RE.finditer(txt):
        base = int(m.group(1), 16)
        delta = int(m.group(2), 16)
        if delta == 0:
            continue  # +00h eh inofensivo
        tgt = base + delta
        if tgt not in starts or tgt not in meta:
            continue
        stale_refs_all += 1
        tf, tb = frame_of(tgt)
        fd = abs(pf[0] - tf[0]) if (pf and tf) else None
        rows.append({
            'caller': u['start'], 'target': tgt, 'base': base, 'delta': delta,
            'ref': m.group(0), 'cf': pf[0] if pf else None, 'tf': tf[0] if tf else None,
            'fd': fd, 'cb': cb, 'tb': tb,
            'cinst': pf[2] if pf else None, 'cins': pf[3] if pf else None,
            'tbytes': DUMP[tgt:tgt + 16].hex(),
            'csize': u['end'] - u['start'],
            'tsize': meta[tgt]['end'] - tgt,
        })

print('refs stale delta>0 p/ start exato do closure:', stale_refs_all)
print('unidades reextraidas afetadas:', len({r['caller'] for r in rows}))
print('distribuicao |frame_caller - frame_target|:', Counter(r['fd'] for r in rows).most_common(20))
print('refs com frame differente:', sum(1 for r in rows if r['fd'] not in (None, 0)))

rows.sort(key=lambda r: (-(r['fd'] or -1), -r['delta'], r['caller']))
print('\n===== TOP 20 PORTADAS DE REF STALE COM MAIOR DELTA DE FRAME =====')
for r in rows[:20]:
    print(f"\ncaller {r['caller']:#x} size={r['csize']:#x} -> target {r['target']:#x} "
          f"size={r['tsize']:#x}  ref='{r['ref']}' (base {r['base']:#x}+{r['delta']:#x})")
    print(f"  frame caller={r['cf'] and hex(r['cf'])} target={r['tf'] and hex(r['tf'])} "
          f"delta={r['fd'] and hex(r['fd'])}  caller_inst={r['cins']} bytes_caller={r['cb']}")
    print(f"  bytes_target(orig)={r['tbytes']}")

# caso conhecido do CONTINUIDADE: call 0x238800 -> dump_2383e8+0x418
print('\n===== CASO CONHECIDO 0x238800 / dump_2383e8+0x418 =====')
for u in reext:
    asm = u['dir'] / 'dsp_entry.asm'
    txt = asm.read_text(errors='replace') if asm.exists() else ''
    if 'dump_2383e8+0418h' in txt or 'dump_2383e8+418h' in txt:
        print('  ainda presente em', u['dir'].name)
        for ln in txt.splitlines():
            if 'dump_2383e8+0' in ln or 'dump_2383e8+4' in ln:
                print('   ', ln.strip())
print('  frame de dump_2383e8:', frame_of(0x2383e8)[0])
print('  frame de 0x238800:', frame_of(0x238800)[0])

# consistencia prologo/epilogo: primeiro sub vs ultimo add, em unidades pequenas (<2KB)
print('\n===== SUB rsp vs ADD rsp (unidades reextraidas < 2KB, amostra) =====')
mis = []
for u in reext:
    if u['end'] - u['start'] > 0x800:
        continue
    b = DUMP[u['start']:u['end']]
    subs, adds = [], []
    for ins in MD.disasm(b, u['start']):
        m = re.match(r'rsp,\s*(?:0x([0-9a-f]+)|([0-9a-f]+)h)', ins.op_str)
        if not m:
            continue
        v = int(m.group(1), 16) if m.group(1) else int(m.group(2), 16)
        if ins.mnemonic == 'sub':
            subs.append(v)
        elif ins.mnemonic == 'add':
            adds.append(v)
    if subs and adds and subs[0] != adds[-1]:
        mis.append((u['start'], subs[0], adds[-1], b[:16].hex(), b[-16:].hex()))
print('unidades <2KB com sub_inicial != add_final:', len(mis))
for x in sorted(mis, key=lambda z: -abs(z[1] - z[2]))[:12]:
    print(f"  {x[0]:#x} sub={x[1]:#x} add={x[2]:#x} delta={x[1]-x[2]:+#x} ini={x[3]} fim={x[4]}")
