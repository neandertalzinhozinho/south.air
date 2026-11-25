"""IDAPython: batch-decompile RVAs from the soothe3 dump into docs/engine/decomp.

Read-only with respect to the dump; it only writes .c files into the project.

Usage:
    idat.exe -A -S"<abs path to this script>" -L"<log>" <db.bin>

IMPORTANT: this script does NOT call ida_auto.auto_wait(). On this 137 MB image
auto_wait() never returns (the DB has pending analysis that IDA keeps trying to
finish), which is why earlier batches produced no output at all. The database is
already analyzed from a previous session, so we decompile directly and append
each result to the report as soon as it is ready - a kill loses nothing.
"""
import idaapi
import ida_auto
import ida_funcs
import ida_hexrays
import ida_segment
import idautils
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\soultree")
OUT = ROOT / "docs" / "engine" / "decomp"
LIST = ROOT / "tools" / "ida" / "batch_list.txt"
REPORT = ROOT / "checks" / "ida_batch.txt"


def find_base():
    base = idaapi.get_imagebase()
    if base and idaapi.is_mapped(base + 0x863170):
        return base
    best = None
    seg = ida_segment.get_first_seg()
    while seg is not None:
        size = seg.end_ea - seg.start_ea
        if size > 0x1000000 and (best is None or size > best[1]):
            best = (seg.start_ea, size)
        nxt = ida_segment.get_next_seg(seg.start_ea)
        if nxt is None or nxt.start_ea == seg.start_ea:
            break
        seg = nxt
    return best[0] if best else base


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    base = find_base()
    rep = open(REPORT, "w", encoding="utf-8")

    def emit(line):
        rep.write(line + "\n")
        rep.flush()

    emit("base=0x%X" % base)
    if not ida_hexrays.init_hexrays_plugin():
        emit("HEXRAYS_NOT_AVAILABLE")
        rep.close()
        return

    addrs = []
    for raw in LIST.read_text(encoding="utf-8-sig").splitlines():
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        addrs.append(int(raw, 16))

    for rva in addrs:
        ea = base + rva
        fn = ida_funcs.get_func(ea)
        if fn is None:
            ida_funcs.add_func(ea)
            fn = ida_funcs.get_func(ea)
        if fn is None:
            emit("NOFUNC 0x%X" % rva)
            continue
        # .pdata creates the function but does NOT disassemble the body. Without
        # this the decompiler returns an empty function (or None) - that is what
        # happened to 0x8C33D0. plan_and_wait is bounded to this range; auto_wait()
        # on this 137 MB image never returns.
        if next(idautils.Heads(fn.start_ea, fn.end_ea), None) is None:
            try:
                ida_auto.plan_and_wait(fn.start_ea, fn.end_ea)
            except Exception as exc:  # noqa: BLE001
                emit("PLAN_FAIL 0x%X %s" % (rva, exc))
        try:
            cfunc = ida_hexrays.decompile(fn.start_ea)
        except Exception as exc:  # noqa: BLE001
            emit("FAIL 0x%X %s" % (rva, exc))
            continue
        if cfunc is None:
            emit("FAIL 0x%X decompile=None" % rva)
            continue
        text = str(cfunc)
        # "ida_" prefix: the bare %08X.c names in docs/engine/decomp belong to
        # Ghidra output (808B3ED0.c, 80879CF0.c, ...) and must not be overwritten.
        name = "ida_%08X.c" % (fn.start_ea - base)
        (OUT / name).write_text(
            "// %s @ 0x%X\n%s" % (idaapi.get_func_name(fn.start_ea), fn.start_ea, text),
            encoding="utf-8")
        sig = ""
        for ln in text.splitlines():
            s = ln.strip()
            if "(" in s and not s.startswith("//") and not s.startswith("*") and "=" not in s and ";" not in s:
                sig = s
                break
        emit("0x%X  %6d B  %s  file=%s" % (rva, fn.end_ea - fn.start_ea, sig, name))

    emit("DONE")
    rep.close()


main()
