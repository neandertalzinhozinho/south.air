import idaapi
import ida_bytes
import ida_funcs
import ida_segment
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\soultree")
OUT = ROOT / "checks" / "ida_diag.txt"

lines = []
lines.append("get_imagebase=0x%X" % idaapi.get_imagebase())

seg = ida_segment.get_first_seg()
while seg is not None:
    lines.append("SEG 0x%X..0x%X  size=0x%X  name=%s" % (
        seg.start_ea, seg.end_ea, seg.end_ea - seg.start_ea,
        ida_segment.get_segm_name(seg)))
    nxt = ida_segment.get_next_seg(seg.start_ea)
    if nxt is None or nxt.start_ea == seg.start_ea:
        break
    seg = nxt

for rva in (0x8B3ED0, 0x8C3C20, 0x8BF650, 0x8C1440):
    for base in (0x180000000, 0x199B0000, 0):
        ea = base + rva
        if not idaapi.is_mapped(ea):
            lines.append("rva=0x%X base=0x%X ea=0x%X NOT MAPPED" % (rva, base, ea))
            continue
        fn = ida_funcs.get_func(ea)
        seg = ida_segment.getseg(ea)
        lines.append(
            "rva=0x%X base=0x%X ea=0x%X seg=%s code=%s func=%s" % (
                rva, base, ea,
                ("0x%X" % seg.start_ea) if seg else "none",
                ida_bytes.is_code(ida_bytes.get_flags(ea)),
                ("0x%X..0x%X" % (fn.start_ea, fn.end_ea)) if fn else "none"))

# count functions anywhere
n = 0
first = last = None
ea = 0
while True:
    fn = ida_funcs.get_next_func(ea)
    if fn is None:
        break
    n += 1
    if first is None:
        first = fn.start_ea
    last = fn.start_ea
    ea = fn.start_ea + 1
lines.append("total funcs=%d first=%s last=%s" % (
    n,
    ("0x%X" % first) if first else "none",
    ("0x%X" % last) if last else "none"))

OUT.write_text("\n".join(lines), encoding="utf-8")
