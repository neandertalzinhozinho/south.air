"""Extrai a saida de chamadas Codex (exec) como texto limpo, por timestamp.

Uso: py -I snap.py <saida_dir> <ts1> [<ts2> ...]   (ts no formato 02-24-03)
Desfaz o mojibake (UTF-8 lido como cp1252 pelo PowerShell) e normaliza CRLF -> LF.
Nao executa nada tirado dos registros: apenas le JSON.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402


TRUNC = __import__("re").compile("(…\\d+ tokens truncated…)")


def demojibake(s):
    """Desfaz por linha; o marcador de truncamento do Codex fica intacto."""
    parts = TRUNC.split(s)
    res = []
    allok = True
    for k, p in enumerate(parts):
        if k % 2 == 1:
            res.append("\n<<<TRUNCADO: " + p + ">>>\n")
            continue
        lines = p.split("\n")
        for i, ln in enumerate(lines):
            d, ok = _demoj(ln)
            if not ok:
                allok = False
                d = "<<<LINHA_NAO_DECODIFICADA>>>" + ln
            lines[i] = d
        res.append("\n".join(lines))
    return "".join(res), allok


def _demoj(s):
    out = bytearray()
    for ch in s:
        try:
            out += ch.encode("cp1252")
        except UnicodeEncodeError:
            if ord(ch) < 256:
                out.append(ord(ch))
            else:
                out += ch.encode("utf-8")
    try:
        return out.decode("utf-8"), True
    except UnicodeDecodeError:
        return s, False


def output_text(ev):
    o = ev["output"]
    try:
        lst = json.loads(o) if isinstance(o, str) and o.startswith("[") else None
    except Exception:
        lst = None
    if lst is None:
        import ast
        try:
            lst = ast.literal_eval(o)
        except Exception:
            lst = None
    if isinstance(lst, list):
        t = "".join(x.get("text", "") for x in lst if isinstance(x, dict))
    else:
        t = o
    return t


def main():
    outdir = sys.argv[1]
    os.makedirs(outdir, exist_ok=True)
    want = sys.argv[2:]
    evs = events.codex_events()
    for ev in evs:
        tsk = ev["ts"][11:19].replace(":", "-")
        if tsk not in want or not ev["ts"].startswith("2026-11-22"):
            continue
        t = output_text(ev)
        t2, ok = demojibake(t)
        t2 = t2.replace("\r\n", "\n")
        with open(os.path.join(outdir, tsk + ".txt"), "w", encoding="utf-8", newline="\n") as w:
            w.write(t2)
        print(tsk, "demojibake_ok" if ok else "DEMOJIBAKE_FALHOU", len(t2))


if __name__ == "__main__":
    main()
