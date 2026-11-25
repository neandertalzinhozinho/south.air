#!/usr/bin/env python3
"""Emit the Rust mirror of the Stage C descriptor tables."""
import json
from pathlib import Path

BASE = Path(r"D:\PROJETOS\soultree")
rows = json.loads((BASE / "checks" / "stage_c_table.json").read_text())

o = []
o.append("// Tabela estatica reconstruida de 0x85E6C0 (jump table 0x85FFA0) + 0x563E40.")
o.append("// Descriptor = 24 B: { i32 code; i32 pad; i64 idx; i32 kind; i32 pad }")
o.append("#[repr(C)]")
o.append("#[derive(Clone, Copy, Debug)]")
o.append("pub struct BandDesc {")
o.append("    pub code: i32,")
o.append("    pub _pad0: i32,")
o.append("    pub idx: i64,")
o.append("    pub kind: i32,")
o.append("    pub _pad1: i32,")
o.append("}")
o.append("const _: () = assert!(core::mem::size_of::<BandDesc>() == 24);")
o.append("")
o.append("const EMPTY: &[BandDesc] = &[];")
o.append("")
for r in rows:
    if r["case"] == 0:
        continue
    o.append("// caso %d -> vetor %s (%d elementos)" % (r["case"], r["vec"], len(r["desc"])))
    o.append("static CASE_%02d: &[BandDesc] = &[" % r["case"])
    for c, i, k in r["desc"]:
        o.append("    BandDesc { code: %d, _pad0: 0, idx: %d, kind: %d, _pad1: 0 }," % (c, i, k))
    o.append("];")
    o.append("")
o.append("/// 0x85E6C0(case): case = dword [arg3+0] ou [arg3+8]; 0x85E6CE cmp ecx,0x16 / ja 0x85EBA7.")
o.append("pub fn select_band_table(case: i32) -> &'static [BandDesc] {")
o.append("    match case {")
for r in rows:
    if r["case"] == 0:
        continue
    o.append("        %d => CASE_%02d," % (r["case"], r["case"]))
o.append("        _ => EMPTY, // caso 0 e > 0x16: 0x85EBA7 -> 0x2752208 (vector vazio)")
o.append("    }")
o.append("}")
txt = "\n".join(o) + "\n"
(BASE / "checks" / "stage_c_rust.rs").write_text(txt, encoding="utf-8")
print(txt)
