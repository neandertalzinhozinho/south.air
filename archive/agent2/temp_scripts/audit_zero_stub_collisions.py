#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
C4c - Auditoria exaustiva de zero-stubs colidentes (SOMENTE LEITURA).

Cruza:
  (a) simbolos dump_X que o mapa resolve para support_asm.obj (zero-stubs),
  (b) unidades reais com span [start,end) do closure dependency_build.json,
  (c) todas as referencias dump_X nos .asm das unidades e no support.asm.

Para cada zero-stub dump_X com X dentro de um span real:
  endereco_correto = unit_base + (X - unit_start)
  onde unit_base = RVA reconstruido de Audio_<unit_start> no mapa.

Saida: JSON + relatorio texto em C:\\Users\\tromb\\AppData\\Local\\Temp\\opencode
"""

import bisect
import collections
import glob
import json
import os
import re

ROOT = r'D:\PROJETOS\shadowFILES\analysis\recovered_native'
MAP_FILE = os.path.join(ROOT, 'testdll', 'recovered_dsp_test.map')
SUPPORT = os.path.join(ROOT, 'testdll', 'support.asm')
DEP_FILE = os.path.join(ROOT, 'dsp', 'dependency_build.json')
UNITS_DIR = os.path.join(ROOT, 'units')
OUT_DIR = r'C:\Users\tromb\AppData\Local\Temp\opencode'

IMAGE_BASE = 0x180000000

FACTORY = [0x8637d0, 0x863af3, 0x86ec10, 0x277c00, 0x278047,
           0x279db4, 0x8701c0, 0x879210, 0x87a020, 0x8798f0]

# preenchido em main(): source-RVA -> RVA reconstruido
unit_bases_global = {}

# ---------------------------------------------------------------------------
# (a) Mapa
# ---------------------------------------------------------------------------
def parse_map():
    sym = {}            # name -> dict(rva, obj, type)
    with open(MAP_FILE, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            t = line.split()
            if len(t) < 5:
                continue
            sec, name, va, typ, obj = t[0], t[1], t[2], t[3], t[4]
            if not re.fullmatch(r'[0-9a-fA-F]{4}:[0-9a-fA-F]{8}', sec):
                continue
            if not re.fullmatch(r'[0-9a-fA-F]{16}', va):
                continue
            if not obj.endswith('.obj'):
                continue
            rva = int(va, 16) - IMAGE_BASE
            sym[name] = dict(rva=rva, obj=obj, type=typ, sec=sec)
    return sym

# ---------------------------------------------------------------------------
# support.asm: classifica os dump PROCs (zero-stub xorps/xor/ret vs jmp)
# ---------------------------------------------------------------------------
def parse_support_procs():
    kinds = {}          # dump name -> 'zero' | 'jmp' | 'other'
    jmp_target = {}
    cur = None
    body = []
    with open(SUPPORT, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            m = re.match(r'\s*(\w+)\s+PROC\b', line, re.I)
            if m:
                cur = m.group(1)
                body = []
                continue
            if re.match(r'\s*\w+\s+ENDP\b', line, re.I):
                if cur:
                    text = ' '.join(x.strip().lower() for x in body)
                    if cur.startswith('dump_'):
                        if 'xorps' in text and 'xor' in text and 'ret' in text:
                            kinds[cur] = 'zero'
                        elif re.search(r'\bjmp\s+dump_', text):
                            kinds[cur] = 'jmp'
                            mm = re.search(r'\bjmp\s+(dump_[0-9a-fA-F]+)', text)
                            if mm:
                                jmp_target[cur] = mm.group(1)
                        else:
                            kinds[cur] = 'other'
                    cur = None
                continue
            if cur:
                body.append(line)
    return kinds, jmp_target

# ---------------------------------------------------------------------------
# (b) dependency_build.json
# ---------------------------------------------------------------------------
def parse_spans():
    spans = []
    with open(DEP_FILE, encoding='utf-8', errors='replace') as fh:
        data = json.load(fh)
    for e in data:
        spans.append(dict(start=int(e['start'], 16),
                          end=int(e['end'], 16),
                          out=e.get('assembler_output', '').strip(),
                          status=e.get('status', ''),
                          byte_identical=e.get('byte_identical', None)))
    spans.sort(key=lambda s: (s['start'], s['end']))
    return spans

# ---------------------------------------------------------------------------
# unidades .asm: referencias dump_X com RVA fonte (label ins_XXXX)
# ---------------------------------------------------------------------------
REF_RE = re.compile(
    r'^\s*(call|jmp|j[a-z]+|loop[a-z]*|dq|dd|dw|db)\s+(dump_([0-9a-fA-F]+))\b',
    re.I)
INS_RE = re.compile(r'^\s*ins_([0-9a-fA-F]+)\s*:', re.I)

def kind_of(mnem):
    m = mnem.lower()
    if m.startswith('call'):
        return 'call'
    if m == 'jmp':
        return 'jmp'
    if m.startswith('j') or m.startswith('loop'):
        return 'jcc'
    if m in ('dq', 'dd', 'dw', 'db'):
        return 'data'
    return 'other'

def parse_units():
    """refs: list of dict(file,line,mnem,kind,dump,x,ins_rva,unit_start)"""
    refs = []
    files = glob.glob(os.path.join(UNITS_DIR, 'rva_*', '*.asm'))
    for f in files:
        mdir = re.search(r'[\\/]rva_([0-9a-fA-F]+)[\\/]', f)
        unit_start = int(mdir.group(1), 16) if mdir else None
        cur_ins = None
        with open(f, encoding='utf-8', errors='replace') as fh:
            for ln_no, line in enumerate(fh, 1):
                mi = INS_RE.match(line)
                if mi:
                    cur_ins = int(mi.group(1), 16)
                mr = REF_RE.match(line)
                if mr:
                    mnem, sym, xh = mr.group(1), mr.group(2), mr.group(3)
                    refs.append(dict(file=os.path.relpath(f, ROOT),
                                     full=f, line=ln_no, mnem=mnem,
                                     kind=kind_of(mnem), dump=sym,
                                     x=int(xh, 16), ins_rva=cur_ins,
                                     unit_start=unit_start,
                                     unit_base=unit_bases_global.get(unit_start)))
    return refs, files

def parse_support_refs():
    """referencias dump_X no support.asm (exceto EXTERN/PUBLIC/PROC/ENDP)."""
    refs = []
    with open(SUPPORT, encoding='utf-8', errors='replace') as fh:
        for ln_no, line in enumerate(fh, 1):
            s = line.strip()
            if re.match(r'^(EXTERN|PUBLIC)\b', s, re.I):
                continue
            m = re.match(r'^\s*(call|jmp|j[a-z]+|loop[a-z]*|dq|dd|dw|db)\s+(dump_[0-9a-fA-F]+)\b',
                         line, re.I)
            if m:
                mnem, sym = m.group(1), m.group(2)
                x = int(sym[5:], 16)
                refs.append(dict(file='testdll/support.asm', full=SUPPORT,
                                 line=ln_no, mnem=mnem, kind=kind_of(mnem),
                                 dump=sym, x=x, ins_rva=None, unit_start=None))
    return refs

# ---------------------------------------------------------------------------
# Lookup de span
# ---------------------------------------------------------------------------
class SpanIndex:
    def __init__(self, spans, unit_bases, asm_label_by_file):
        self.spans = spans
        self.starts = [s['start'] for s in spans]
        self.unit_bases = unit_bases
        self.asm_label = asm_label_by_file

    def candidates(self, x):
        out = []
        hi = bisect.bisect_right(self.starts, x)
        for i in range(hi):
            s = self.spans[i]
            if s['end'] > x:
                out.append(s)
        return out

    def best(self, x):
        cands = self.candidates(x)
        if not cands:
            return None
        # prefere span que tenha ins_<x> no .asm correspondente
        def score(s):
            u = s['start']
            asm = self.asm_label.get(u)
            has_label = asm and (x in asm)
            has_base = u in self.unit_bases
            return (1 if has_label else 0, 1 if has_base else 0,
                    -(s['end'] - s['start']))
        cands.sort(key=score, reverse=True)
        return cands[0]

# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    print('[1/6] mapa ...')
    sym = parse_map()
    print('      simbolos:', len(sym))

    print('[2/6] support.asm PROCs ...')
    kinds, jmp_target = parse_support_procs()
    zcnt = collections.Counter(kinds.values())
    print('      dump PROCs:', dict(zcnt))

    print('[3/6] dependency_build.json ...')
    spans = parse_spans()
    print('      spans:', len(spans))

    print('[4/6] mapa source-RVA -> RVA reconstruido (Audio_/dump_ em dsp_entry.obj) ...')
    unit_bases = {}
    for name, d in sym.items():
        if d['obj'] != 'dsp_entry.obj':
            continue
        m = re.match(r'(?:Audio|dump)_([0-9a-fA-F]+)$', name)
        if m:
            unit_bases.setdefault(int(m.group(1), 16), d['rva'])
    print('      bases:', len(unit_bases))
    unit_bases_global.update(unit_bases)

    print('[5/6] referencias nos .asm das unidades ...')
    refs, ufiles = parse_units()
    srefs = parse_support_refs()
    print('      unit files:', len(ufiles), 'refs unidades:', len(refs),
          'refs support:', len(srefs))

    # ins_ labels por unit_start (para scoring)
    asm_label = {}
    for f in ufiles:
        md = re.search(r'[\\/]rva_([0-9a-fA-F]+)[\\/]', f)
        if not md:
            continue
        u = int(md.group(1), 16)
        lbl = set()
        with open(f, encoding='utf-8', errors='replace') as fh:
            for line in fh:
                mi = INS_RE.match(line)
                if mi:
                    lbl.add(int(mi.group(1), 16))
        asm_label.setdefault(u, set()).update(lbl)

    sidx = SpanIndex(spans, unit_bases, asm_label)

    print('[6/6] cruzando ...')

    # zero-stubs: dump_X no mapa->support_asm.obj E classificados 'zero'
    zero = {}
    for name, d in sym.items():
        if d['obj'] == 'support_asm.obj' and kinds.get(name) == 'zero':
            m = re.match(r'dump_([0-9a-fA-F]+)$', name)
            if m:
                zero[name] = int(m.group(1), 16)
    jmpstub = {n: int(n[5:], 16) for n in kinds if kinds[n] == 'jmp'}

    # indice de referencias por dump
    refs_by_dump = collections.defaultdict(list)
    for r in refs + srefs:
        refs_by_dump[r['dump']].append(r)

    collisions = []
    for name, x in zero.items():
        s = sidx.best(x)
        if not s:
            continue
        us = s['start']
        base = unit_bases.get(us)
        if base is None:
            # tenta achar base via span que comeca em us ou label Audio
            continue
        correct = base + (x - us)
        rlist = refs_by_dump.get(name, [])
        # prova de que existe codigo real em X: label ins_X no .asm da unidade
        target_has_ins = x in asm_label.get(us, set())
        target_alias = sym.get('dump_%x' % x)
        collisions.append(dict(
            stub=name, x=x, span_start=us, span_end=s['end'],
            unit_base=base, correct_rva=correct,
            span_out=s['out'], offset=x - us,
            target_has_ins_label=target_has_ins,
            target_map_alias_rva=(target_alias['rva'] if target_alias and
                                  target_alias['obj'] == 'dsp_entry.obj' else None),
            in_factory=(x in FACTORY),
            nrefs=len(rlist),
            refs=[dict(file=r['file'], line=r['line'], mnem=r['mnem'],
                       kind=r['kind'], ins_rva=r['ins_rva'],
                       site_rebuilt_rva=(
                           r['unit_base'] + (r['ins_rva'] - r['unit_start']))
                       if (r['ins_rva'] is not None and
                           r['unit_start'] is not None and
                           r['unit_base'] is not None) else None)
                  for r in rlist]))

    # ------- alcance da cadeia do factory (BFS por unidades) -----------------
    # WebSocket: ponto de partida = unidades cujo start esta em FACTORY (ou o
    # span que contem cada X de FACTORY). Segue referencias dump_X: se X cai
    # numa unidade real, entra nessa unidade e continua.
    fact_units = set()
    for x in FACTORY:
        s = sidx.best(x)
        if s:
            fact_units.add(s['start'])
    visited = set(fact_units)
    queue = list(fact_units)
    reachable = {}       # stub -> caminho (lista de unidades)
    paths = {u: [u] for u in fact_units}
    while queue:
        u = queue.pop(0)
        fr = [f for f in ufiles if re.search(r'[\\/]rva_([0-9a-fA-F]+)[\\/]', f)
              and int(re.search(r'[\\/]rva_([0-9a-fA-F]+)[\\/]', f).group(1), 16) == u]
        for f in fr:
            with open(f, encoding='utf-8', errors='replace') as fh:
                for line in fh:
                    m = REF_RE.match(line)
                    if not m:
                        continue
                    x = int(m.group(3), 16)
                    s = sidx.best(x)
                    if not s:
                        continue
                    nx = s['start']
                    dname = 'dump_%x' % x
                    if dname in zero and dname not in reachable:
                        reachable[dname] = paths[u] + [nx]
                    if nx not in visited:
                        visited.add(nx)
                        paths[nx] = paths[u] + [nx]
                        queue.append(nx)

    # ------- estatisticas ---------------------------------------------------
    kinds_ref = collections.Counter()
    for c in collisions:
        for r in c['refs']:
            kinds_ref[r['kind']] += 1

    # diagnostico: quantos zero-stubs tem X dentro de algum span real / label
    zero_in_span = sum(1 for x in zero.values() if sidx.best(x) is not None)
    zero_with_ins = sum(1 for x in zero.values()
                        if (sidx.best(x) and
                            x in asm_label.get(sidx.best(x)['start'], set())))
    zero_with_refs = sum(1 for n in zero if refs_by_dump.get(n))

    # validacao do fix conhecido: 12 sites em 0x46066f..0x4606e8 (dump_277f56)
    known_fix = []
    known_fix_dumps = set()
    for r in refs:
        if r['unit_start'] == 0x277f56 and r['ins_rva'] is not None:
            if 0x277f66 <= r['ins_rva'] <= 0x277fdf:
                known_fix.append(dict(dump=r['dump'], line=r['line'],
                                      mnem=r['mnem'],
                                      rebuilt=r['unit_base'] + (r['ins_rva'] - 0x277f56)
                                      if r['unit_base'] is not None else None,
                                      is_zero=(r['dump'] in zero),
                                      is_collision=any(c['stub'] == r['dump'] for c in collisions)))
                known_fix_dumps.add(r['dump'])
    for c in collisions:
        c['already_fixed'] = c['stub'] in known_fix_dumps
        c['confirmed'] = c['target_has_ins_label']

    summary = dict(
        map_symbols=len(sym),
        support_dump_procs=len(kinds),
        zero_stubs=len(zero),
        jmp_stubs=len(jmpstub),
        spans=len(spans),
        unit_bases=len(unit_bases),
        unit_asm_files=len(ufiles),
        unit_refs=len(refs),
        support_refs=len(srefs),
        collisions=len(collisions),
        collisions_with_refs=sum(1 for c in collisions if c['nrefs'] > 0),
        collisions_confirmed=sum(1 for c in collisions if c['target_has_ins_label']),
        collisions_borderline=sum(1 for c in collisions if not c['target_has_ins_label']),
        collisions_already_fixed=sum(1 for c in collisions if c['already_fixed']),
        confirmed_with_refs=sum(1 for c in collisions if c['confirmed'] and c['nrefs'] > 0),
        collision_refs_kinds=dict(kinds_ref),
        zero_stubs_x_in_span=zero_in_span,
        zero_stubs_x_with_ins_label=zero_with_ins,
        zero_stubs_with_any_ref=zero_with_refs,
        known_fix_sites=len(known_fix),
        known_fix_collisions=sum(1 for k in known_fix if k['is_collision']),
        factory_collisions=sum(1 for c in collisions if c['in_factory']),
        factory_reachable_stubs=len(reachable),
        factory_units_visited=len(visited),
    )

    # saida
    jout = os.path.join(OUT_DIR, 'c4c_collisions.json')
    with open(jout, 'w', encoding='utf-8') as fh:
        json.dump(dict(summary=summary, collisions=collisions,
                       factory_reachable=reachable,
                       factory_units=sorted(visited),
                       known_fix=known_fix,
                       jmp_stubs=sorted(jmpstub)), fh, indent=2)
    print('\nJSON:', jout)

    tout = os.path.join(OUT_DIR, 'c4c_collisions_report.txt')
    with open(tout, 'w', encoding='utf-8') as fh:
        fh.write('=== C4c - AUDITORIA DE ZERO-STUBS COLIDENTES ===\n\n')
        for k, v in summary.items():
            fh.write('%-32s %s\n' % (k, v))
        fh.write('\n=== TABELA stub_X -> endereco_real (RVA rebuild) ===\n')
        fh.write('%-18s %-10s %-10s %-10s %-10s %-6s %-5s %-5s %-6s %s\n' %
                 ('stub', 'X', 'span_start', 'unit_base', 'correct', 'offset',
                  'conf', 'fixed', 'factory', 'nrefs'))
        for c in sorted(collisions, key=lambda c: c['x']):
            fh.write('%-18s 0x%-8x 0x%-9x 0x%-9x 0x%-9x 0x%-5x %-5s %-5s %-6s %d\n' %
                     (c['stub'], c['x'], c['span_start'], c['unit_base'],
                      c['correct_rva'], c['offset'],
                      'SIM' if c['confirmed'] else 'nao',
                      'SIM' if c['already_fixed'] else '',
                      'SIM' if c['in_factory'] else '', c['nrefs']))
        fh.write('\n=== ALCANCE DA CADEIA DO FACTORY ===\n')
        cm = {c['stub']: c for c in collisions}
        for d, path in sorted(reachable.items(), key=lambda kv: int(kv[0][5:], 16)):
            c = cm.get(d)
            fh.write('%-18s correct=%-10s conf=%-5s fixed=%-5s via %s\n' %
                     (d, ('0x%x' % c['correct_rva']) if c else '-',
                      'SIM' if (c and c['confirmed']) else 'nao',
                      'SIM' if (c and c['already_fixed']) else '',
                      ' -> '.join('0x%x' % u for u in path)))
        fh.write('\n=== VALIDACAO FIX CONHECIDO (dump_277f56, 0x46066f..0x4606e8) ===\n')
        for k in known_fix:
            fh.write('   %-18s line=%-6d %-4s rebuilt=%-10s zero=%-5s collision=%s\n' %
                     (k['dump'], k['line'], k['mnem'],
                      ('0x%x' % k['rebuilt']) if k['rebuilt'] is not None else '-',
                      k['is_zero'], k['is_collision']))
        fh.write('\n=== SITES DE REFERENCIA (colisoes) ===\n')
        for c in sorted(collisions, key=lambda c: c['x']):
            if not c['refs']:
                continue
            fh.write('\n%s  X=0x%x  correct=0x%x\n' %
                     (c['stub'], c['x'], c['correct_rva']))
            for r in c['refs']:
                fh.write('   %-6s %s:%d  ins=%s  rebuilt=%s\n' %
                         (r['mnem'], r['file'], r['line'],
                          ('0x%x' % r['ins_rva']) if r['ins_rva'] is not None else '-',
                          ('0x%x' % r['site_rebuilt_rva']) if r['site_rebuilt_rva'] is not None else '-'))
    print('TXT :', tout)

    print('\n=== RESUMO ===')
    for k, v in summary.items():
        print('%-32s %s' % (k, v))

if __name__ == '__main__':
    main()
