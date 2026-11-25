"""Aplica o formato '*** Begin Patch / *** Update File / @@' do Codex a um texto (em memoria).

Uso como modulo: apply(texto, patch_js_text, caminho_alvo) -> novo texto.
Cada bloco @@ e localizado pela sequencia de linhas de contexto e removidas, a partir do
fim do bloco anterior (igualdade exata; se falhar, igualdade ignorando espacos finais).
"""
import json
import re


def extract_patch(js):
    m = re.search(r'const patch = ("(?:[^"\\]|\\.)*");', js, re.S)
    return json.loads(m.group(1))


def sections(patch):
    """Devolve {arquivo: [blocos]}, cada bloco = lista de (tipo, linha)."""
    out = {}
    cur = None
    chunk = None
    for ln in patch.split("\n"):
        if ln.startswith("*** Update File: "):
            cur = ln[len("*** Update File: "):]
            out.setdefault(cur, [])
            chunk = None
            continue
        if ln.startswith("*** Begin Patch") or ln.startswith("*** End Patch"):
            continue
        if ln.startswith("@@"):
            chunk = []
            out[cur].append(chunk)
            continue
        if chunk is None:
            continue
        t = ln[:1]
        if t in (" ", "+", "-"):
            chunk.append((t, ln[1:]))
        elif ln == "":
            chunk.append((" ", ""))
        else:
            raise ValueError("linha de patch inesperada: %r" % ln)
    return out


def apply(text, chunks):
    lines = text.split("\n")
    pos = 0
    report = []
    for ch in chunks:
        old = [l for t, l in ch if t in (" ", "-")]
        new = [l for t, l in ch if t in (" ", "+")]
        found = -1
        mode = ""
        for cmp, nm in ((lambda a, b: a == b, "exato"), (lambda a, b: a.rstrip() == b.rstrip(), "rstrip")):
            for i in range(pos, len(lines) - len(old) + 1):
                if all(cmp(lines[i + k], old[k]) for k in range(len(old))):
                    found = i
                    mode = nm
                    break
            if found >= 0:
                break
        if found < 0:
            raise ValueError("bloco nao encontrado: %r" % old[:3])
        report.append("bloco na linha %d (%s), -%d +%d" % (found + 1, mode, len(old), len(new)))
        lines[found:found + len(old)] = new
        pos = found + len(new)
    return "\n".join(lines), report
