#!/usr/bin/env python3
"""Compara o despejo do Rust com o modelo Python e com o medido do plugin."""
import pathlib
import struct
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import full_model as F  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent


def f32(v):
    return struct.unpack("<f", struct.pack("<I", v))[0]


def read_bits(p):
    return [int(l, 16) for l in p.read_text().splitlines() if l.strip()]


def main():
    d = F.load("rand")
    src = [f32(v) for v in d["SRC"]]
    tw = [f32(v) for v in d["TW38"]]
    idx = d["IDX"]
    ws_meas = [f32(v) for v in d["WS"]]
    kd = [f32(v) for v in d["KD"]]

    ws1_py = F.P1.pass1_model(src, idx)
    ws1_rs = [f32(v) for v in read_bits(ROOT / "checks" / ".build" / "rust_ws1.bits")]

    print("pass1: max|rust-python| =", max(abs(ws1_rs[i] - ws1_py[i]) for i in range(512)))
    bad = [i for i in range(512) if abs(ws1_rs[i] - ws1_py[i]) > 1e-5]
    print("       indices divergentes:", bad[:12], "total", len(bad))

    ws2_py = F.pass3a_all(F.pass2_all(ws1_py), tw)
    ws2_rs = [f32(v) for v in read_bits(ROOT / "checks" / ".build" / "rust_ws2.bits")]
    print("ws final: max|rust-python| =", max(abs(ws2_rs[i] - ws2_py[i]) for i in range(512)))
    print("ws final: max|python-medido| =", max(abs(ws2_py[i] - ws_meas[i]) for i in range(512)))
    print("ws final: max|rust-medido| =", max(abs(ws2_rs[i] - ws_meas[i]) for i in range(512)))
    bad = [i for i in range(512) if abs(ws2_rs[i] - ws2_py[i]) > 1e-5]
    print("       indices divergentes:", bad[:12], "total", len(bad))

    kd_rs = [f32(v) for v in read_bits(ROOT / "checks" / ".build" / "rust_kd.bits")]
    kd_py = F.pass3b(ws2_py, tw)
    print("kd: max|rust-python| =", max(abs(kd_rs[i] - kd_py[i]) for i in range(512)))
    print("kd: max|python-medido| =", max(abs(kd_py[i] - kd[i]) for i in range(512)))
    print("kd: max|rust-medido| =", max(abs(kd_rs[i] - kd[i]) for i in range(512)))


if __name__ == "__main__":
    main()
