"""Audit: every instruction address cited in PLANO 17.2/17.3 must exist with
the stated mnemonic in the dump. Reads the raw image, no disassembler needed
beyond capstone for a single instruction."""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

d = re_lib.data()
md = Cs(CS_ARCH_X86, CS_MODE_64)

CLAIMS = [
    (0x95AA, "mov", "0x1310: arg3 -> rdx (destino fora do lugar)"),
    (0x9640, "vaddss", "0x1310: soma escalar"),
    (0x9646, "vmovss", "0x1310: store em [rdx]"),
    (0x6200, "vmulss", "0x1220: multiplica por escalar"),
    (0x6205, "vmovss", "0x1220: store em [rdx]"),
    (0x9020, "vaddss", "0x12E0: soma escalar"),
    (0x9025, "vmovss", "0x12E0: store em [rcx]"),
    (0x3495, "test", "0x1100: testa o modo"),
    (0x349E, "cmp", "0x1100: compara modo com 4"),
    (0x3500, "vminss", "0x1100: variante min"),
    (0x3640, "vmaxss", "0x1100: variante max"),
    (0x87C961, "movss", "caller 1: param_3 = 250.0f"),
    (0x87C91F, "movaps", "caller 1: param_4 = xmm15"),
    (0x87C9B9, "movss", "caller 1: param_5 = xmm15 (stack)"),
    (0x87CA13, "movss", "caller 1: xmm15 := 2.0f"),
    (0x87CB10, "movss", "caller 2: param_3 = 1000.0f"),
    (0x87CB18, "movaps", "caller 2: param_4 = xmm15"),
    (0x87CBEB, "movss", "caller 2: param_5 = xmm15 (stack)"),
    (0x87CB07, "movss", "caller 2: xmm15 := 2.0f"),
    (0x27C280, "vmovups", "0x277C00: loop vetorial de copia (ramo do expoente 1.0)"),
]

bad = 0
for addr, want, why in CLAIMS:
    ins = list(md.disasm(d[addr:addr + 16], addr))
    if not ins:
        print("FAIL 0x%X  nao decodifica   (%s)" % (addr, why))
        bad += 1
        continue
    got = ins[0].mnemonic
    ok = got == want
    if not ok:
        bad += 1
    print("%s 0x%X  esperado=%-9s obtido=%-9s  %s"
          % ("OK  " if ok else "FAIL", addr, want, got, why))

print()
print("claims=%d  failures=%d" % (len(CLAIMS), bad))
