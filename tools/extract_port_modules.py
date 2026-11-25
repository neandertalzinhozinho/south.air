#!/usr/bin/env python3
"""Extrai os kernels provados de `checks/*.rs` para `port/src/*.rs`.

Motivo: ate 2026-11-25 o codigo provado (J1..J6) e os testes viviam no mesmo
arquivo. O port do motor precisa do codigo como biblioteca, e os testes de
`checks/` precisam continuar rodando com `rustc --test`. Para nao duplicar
codigo (duas copias divergem), o codigo passa a viver em `port/src/<mod>.rs` e
o arquivo de teste aponta para ele com `#[path = "../port/src/<mod>.rs"]`.

O script e reprodutivel: le sempre o backup `checks/.build/pre_port/<arquivo>`
(criado na primeira execucao) e reescreve `checks/<arquivo>` + `port/src/<mod>.rs`.

Uso:
    py -3 tools/extract_port_modules.py           # extrai
    py -3 tools/extract_port_modules.py --verify  # confere que o backup existe

Nada aqui altera prova: o texto e movido byte a byte, exceto pelas linhas
`include!` de `j4_fft.rs`, que ficam no arquivo de teste (sao dados-ouro, nao
kernel).
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHECKS = ROOT / "checks"
PORT_SRC = ROOT / "port" / "src"
BACKUP = CHECKS / ".build" / "pre_port"

# arquivo de teste -> (modulo do port, imports extras no cabecalho do teste)
FILES = {
    "stage_j_core.rs": ("core_dsp", []),
    "stage_j_pipe.rs": ("pipe", ["use core::mem::size_of;"]),
    "stage_j_fft.rs": ("fft_layout", []),
    "stage_j_chan.rs": ("chan", ["use core::mem::size_of;"]),
    "stage_j_engine.rs": ("engine", []),
    "j4_fft.rs": ("fft_kernels", []),
}

HEADER = """//! Testes da etapa J — o kernel vive em `port/src/{module}.rs` (fonte única).
//!
//! Este arquivo contém **apenas** os testes. O código testado é compartilhado
//! com o crate `soultree_port` via `#[path]`, então não há duas cópias.
//!
//! Extraído de `checks/.build/pre_port/{source}` por
//! `tools/extract_port_modules.py` (movido byte a byte, sem edição).
//!
//! Teste: `rustc --edition 2021 --test checks\\{source} -o checks\\.build\\{stem}.exe`

#![allow(unused_imports)]

#[path = "../port/src/{module}.rs"]
mod {module};

pub use {module}::*;
"""


def read_text(path: Path) -> str:
    data = path.read_bytes()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1252")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def extract_fixture(lines: list[str], name: str) -> tuple[list[str], list[str]]:
    """Move fixtures de teste (dados-ouro inline) do kernel para o arquivo de teste.

    `stage_j_fft.rs` declara `Case`/`CASES` no meio do kernel; são casos
    medidos, não código do motor, e referenciam as tabelas de `fft_golden.rs`.
    """
    if name != "stage_j_fft.rs":
        return [], lines
    start = next(i for i, l in enumerate(lines) if l.startswith("pub struct Case {"))
    cases = next(i for i, l in enumerate(lines) if l.startswith("pub static CASES"))
    end = next(i for i in range(cases, len(lines)) if lines[i].strip() == "];")
    # leva junto o cabeçalho comentado imediatamente acima
    while start > 0 and (not lines[start - 1].strip() or lines[start - 1].lstrip().startswith("//")):
        start -= 1
    fixture = lines[start : end + 1]
    return fixture, lines[:start] + lines[end + 1 :]


def split_at_tests(lines: list[str], source: str) -> tuple[list[str], list[str]]:
    """Divide em (kernel, testes) no `#[cfg(test)]` que precede `mod tests`."""
    for i, line in enumerate(lines):
        if line.lstrip().startswith("mod tests {"):
            j = i
            while j > 0 and lines[j - 1].strip() != "#[cfg(test)]":
                j -= 1
                if i - j > 8:
                    break
            if j > 0 and lines[j - 1].strip() == "#[cfg(test)]":
                return lines[: j - 1], lines[j - 1 :]
            raise SystemExit(f"{source}: `mod tests` sem `#[cfg(test)]` adjacente")
    raise SystemExit(f"{source}: `mod tests` não encontrado")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    BACKUP.mkdir(parents=True, exist_ok=True)
    for name in FILES:
        src = CHECKS / name
        bak = BACKUP / name
        if not bak.exists():
            if args.verify:
                raise SystemExit(f"backup ausente: {bak}")
            if not src.exists():
                raise SystemExit(f"fonte ausente: {src}")
            shutil.copyfile(src, bak)

    if args.verify:
        print(f"backup ok: {BACKUP}")
        return 0

    for name, (module, extra_imports) in FILES.items():
        raw = read_text(BACKUP / name)
        lines = raw.splitlines(keepends=True)
        kernel, tests = split_at_tests(lines, name)

        # `include!` são vetores-ouro medidos; ficam no teste, não no kernel.
        includes = [ln for ln in kernel if ln.lstrip().startswith("include!(")]
        kernel = [ln for ln in kernel if not ln.lstrip().startswith("include!(")]

        fixture, kernel = extract_fixture(kernel, name)

        # kernel: remove a linha de comando de teste do doc (aponta para o .rs antigo)
        write_text(PORT_SRC / f"{module}.rs", "".join(kernel))

        head = HEADER.format(module=module, source=name, stem=Path(name).stem)
        if extra_imports:
            head += "\n" + "\n".join(extra_imports) + "\n"
        if includes:
            head += "\n" + "".join(includes)
        if fixture:
            head += "\n" + "".join(fixture)
        write_text(CHECKS / name, head + "\n" + "".join(tests))
        print(f"{name}: kernel -> port/src/{module}.rs ({len(kernel)} linhas), testes {len(tests)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
