#!/usr/bin/env python3
"""Gera o mapa completo indice -> offset do bloco de estado (Etapa G).

Fontes, todas lidas do dump (nenhum nome inventado):
  * tabela de despacho  0x8683CC (143 bytes) -> 0x868348 (33 dwords)
  * tabela de descritores 0x238E9B0 (passo 0x68): indice em +0x10, nome em +0x14
  * funcao 0x867D80: handler -> store, lido instrucao a instrucao

O estado comeca em engine+0x54 (provado: 0086369D / 008638CA / 00870941), entao
"state+off" aqui e sempre disp_da_instrucao - 0x54.
"""
import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import re_lib

d = re_lib.data()

BYT = 0x8683CC
TGT = 0x868348
DESC = 0x238E9B0
DESC_STRIDE = 0x68

# handler -> (delta em relacao ao estado | texto, tipo, valor)
HANDLERS = {
    0x867F6E: (0x00, "f32", "xmm8"),
    0x867E88: (0x57, "u8", "r8b"),
    0x867EC8: (0xB0, "i32", "min(r9d-1,7)"),
    0x867F07: ("engine+0x50 (fora do estado)", "i32", "r9d"),
    0x867F10: (0x58, "u8", "r8b"),
    0x867F7B: (0x04, "f32", "xmm8"),
    0x867FBD: (0x08, "f32", "xmm8"),
    0x867FFF: (0x0C, "f32", "xmm8"),
    0x867FAB: (0x10, "f32", "xmm6"),
    0x867FB4: (0x14, "f32", "xmm6"),
    0x867FED: (0x18, "f32", "xmm6"),
    0x867FF6: (0x1C, "f32", "xmm6"),
    0x868009: (0x20, "f32", "xmm6"),
    0x868012: (0x24, "f32", "xmm6"),
    0x86801B: (0x51, "u8", "r8b"),
    0x868038: (0x53, "u8", "r8b"),
    0x868055: (0x52, "u8", "r8b"),
    0x868061: (0x28, "f32", "xmm8"),
    0x86806E: (0x3C, "f32", "xmm8"),
    0x867F55: (0xAC, "i32", "min(r9d-1,7)"),
    0x8681CD: (0x4C, "f32", "xmm8<0.999 ? xmm6 : 60.0f"),
    0x8681F2: (0x40, "f32", "powf(10, 0.05*xmm6)"),
    0x868219: (0x44, "f32", "0.01*xmm6"),
    0x868230: (0x48, "f32", "powf(10, 0.05*xmm6)"),
    0x868257: (0x54, "u8", "r8b"),
    0x868263: (0x55, "u8", "r8b"),
    0x8682F4: (0x2C, "f32", "xmm8"),
    0x868301: (0x30, "f32", "xmm8"),
    0x86830E: (0x34, "f32", "xmm8"),
    0x86831B: (0x38, "f32", "xmm8"),
}

# (delta no registro, tipo, valor) para as tabelas internas
BAND_SUB = [
    (0x00, "u8", "r8b"),
    (0x01, "u8", "r8b"),
    (0x04, "f32", "xmm6 (frequencia)"),
    (0x08, "f32", "24*xmm8 - 12"),
    (0x0C, "f32", "x<=0?0 : 2*asinh(1/(2x))/ln2"),
    (0x10, "f32", "expf(ln6 + xmm8*(ln128-ln6))"),
    (0x14, "f32", "xmm6"),
    (0x18, "i32", "r9d"),
    (0x1C, "i32", "r9d"),
]
GROUP_SUB = [
    (0x00, "f32", "xmm8"),
    (0x04, "u8", "r8b"),
    (0x05, "u8", "r8b"),
    (0x06, "u8", "r8b"),
    (0x07, "u8", "r8b"),
]


def name(idx):
    b = DESC + idx * DESC_STRIDE
    raw = d[b + 0x14:b + 0x14 + 0x2C].split(b"\x00")[0]
    return raw.decode("latin-1")


def main():
    byt = d[BYT:BYT + 143]
    tgt = [struct.unpack_from("<I", d, TGT + i * 4)[0] for i in range(33)]
    lines = []
    lines.append("idx  nome                       handler   store            tipo  valor")
    for i in range(143):
        h = tgt[byt[i]]
        assert struct.unpack_from("<I", d, DESC + i * DESC_STRIDE + 0x10)[0] == i
        if h == 0x86807E:
            b, r = divmod(i - 19, 9)
            off, typ, val = BAND_SUB[r]
            store = "state+0x%X (b=%d,r=%d)" % (0xB8 + 0x20 * b + off, b, r)
        elif h == 0x86826F:
            g, r = divmod(i - 98, 5)
            off, typ, val = GROUP_SUB[r]
            store = "state+0x%X (g=%d,r=%d)" % (0x1B8 + 8 * g + off, g, r)
        elif h == 0x868328:
            off, typ, val = (0x1D + i, "u8", "r8b")
            store = "state+0x%X" % off
        else:
            off, typ, val = HANDLERS[h]
            store = off if isinstance(off, str) else "state+0x%02X" % off
            if isinstance(off, str):
                store = off
        lines.append("%3d  %-26s 0x%06X  %-16s %-5s %s"
                     % (i, name(i), h, store, typ, val))
    out = Path(__file__).resolve().parent.parent / "checks" / "param_map.txt"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:4]))
    print("...")
    print("\n".join(lines[-3:]))
    print("linhas:", len(lines) - 1)


if __name__ == "__main__":
    main()
