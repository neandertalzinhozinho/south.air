#!/usr/bin/env python3
"""Normalize the flat virtual dump of soothe3 into a PE file.

The dump has file offsets equal to RVAs, but the section headers still hold the
original (disk) PointerToRawData/SizeOfRawData. Any tool that maps by section
headers reads the wrong bytes. This script rewrites the section table so that
raw == virtual, then validates the result.
"""
import struct
import sys
from pathlib import Path


def main() -> int:
    src = Path(sys.argv[1] if len(sys.argv) > 1 else r"D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin")
    dst = Path(sys.argv[2] if len(sys.argv) > 2 else src.with_name("soothe3_unpacked.dll"))

    data = bytearray(src.read_bytes())
    if data[:2] != b"MZ":
        print(f"error: {src} is not a PE (no MZ)")
        return 1

    pe_off = struct.unpack_from("<I", data, 0x3C)[0]
    if data[pe_off:pe_off + 4] != b"PE\0\0":
        print("error: missing PE signature")
        return 1

    num_sections = struct.unpack_from("<H", data, pe_off + 6)[0]
    opt_size = struct.unpack_from("<H", data, pe_off + 20)[0]
    magic = struct.unpack_from("<H", data, pe_off + 24)[0]
    if magic != 0x20B:
        print(f"error: expected PE32+ (0x20B), got {magic:#x}")
        return 1

    size_of_image = struct.unpack_from("<I", data, pe_off + 24 + 56)[0]
    size_of_headers = struct.unpack_from("<I", data, pe_off + 24 + 60)[0]
    sect_off = pe_off + 24 + opt_size

    # The dump is a flat image: file size must be at least SizeOfImage.
    if len(data) < size_of_image:
        data.extend(b"\0" * (size_of_image - len(data)))
    del data[size_of_image:]

    print(f"PE32+ sections={num_sections} size_of_image={size_of_image:#x} headers={size_of_headers:#x}")
    for i in range(num_sections):
        off = sect_off + i * 40
        name = bytes(data[off:off + 8]).rstrip(b"\0").decode(errors="replace")
        vsize, va, rawsize, rawptr = struct.unpack_from("<IIII", data, off + 8)
        old = (rawsize, rawptr)
        struct.pack_into("<II", data, off + 16, vsize, va)  # SizeOfRawData, PointerToRawData
        print(f"  {name:10s} rva={va:#010x} vsize={vsize:#010x} raw {old[0]:#x}@{old[1]:#x} -> {vsize:#x}@{va:#x}")

    # Clear the checksum: it is invalid after rewriting and tools only warn.
    struct.pack_into("<I", data, pe_off + 24 + 64, 0)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)
    print(f"wrote {dst} ({len(data)} bytes)")

    # Validate with pefile and capstone.
    try:
        import pefile
        pe = pefile.PE(str(dst), fast_load=True)
        print("pefile ok:", hex(pe.OPTIONAL_HEADER.ImageBase), "entry", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))
    except ImportError:
        print("pefile not installed; skipped pefile validation")
        return 0

    try:
        from capstone import Cs, CS_ARCH_X86, CS_MODE_64
    except ImportError:
        print("capstone not installed; skipped disassembly validation")
        return 0

    text = next((s for s in pe.sections if s.Name.rstrip(b"\0") == b".text"), None)
    if text is None:
        print("error: no .text section")
        return 1
    code = text.get_data()[:32]
    md = Cs(CS_ARCH_X86, CS_MODE_64)
    insns = list(md.disasm(code, pe.OPTIONAL_HEADER.ImageBase + text.VirtualAddress, count=4))
    for ins in insns:
        print(f"  {ins.address:#x}: {ins.mnemonic} {ins.op_str}")
    if not insns:
        print("error: .text does not disassemble")
        return 1
    print("PASS: normalized PE maps .text correctly")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
