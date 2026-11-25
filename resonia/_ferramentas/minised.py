"""Interpretador minimo de GNU sed (subconjunto usado nas sessoes), em memoria.

Suporta: s/// (flags g), enderecos N, N,M, /re/,/re/; comandos c\ e i\ (forma GNU
de uma linha), varios -e, BRE e ERE (-E). Nao executa nada externo.
"""
import re


def _conv_regex(pat, ere):
    out = []
    i = 0
    n = len(pat)
    while i < n:
        ch = pat[i]
        if ch == "[":
            # copia a expressao de colchetes literalmente (barra e literal dentro)
            j = i + 1
            if j < n and pat[j] == "^":
                j += 1
            if j < n and pat[j] == "]":
                j += 1
            while j < n and pat[j] != "]":
                j += 1
            body = pat[i:j + 1]
            out.append(body.replace("\\", "\\\\") if "\\" in body else body)
            i = j + 1
            continue
        if ch == "\\" and i + 1 < n:
            nx = pat[i + 1]
            i += 2
            if ere:
                if nx == "n":
                    out.append("\\n")
                elif nx in "bBwWsS":
                    out.append("\\" + nx)
                elif nx.isdigit():
                    out.append("\\" + nx)
                else:
                    out.append(re.escape(nx))
            else:
                if nx in "(){}|?+":
                    out.append(nx)
                elif nx == "n":
                    out.append("\\n")
                elif nx in "bBwWsS":
                    out.append("\\" + nx)
                elif nx.isdigit():
                    out.append("\\" + nx)
                else:
                    out.append(re.escape(nx))
            continue
        if not ere and ch in "(){}|?+":
            out.append("\\" + ch)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def _split_delim(s, i, d):
    """Le ate o delimitador d nao escapado; '\\d' vira d literal (marcado)."""
    buf = []
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            if s[i + 1] == d:
                buf.append("\x00LIT" + d + "\x00")
            else:
                buf.append(s[i:i + 2])
            i += 2
            continue
        if ch == d:
            return "".join(buf), i + 1
        buf.append(ch)
        i += 1
    raise ValueError("delimitador nao fechado")


def _finish_pat(p, ere):
    # delimitador escapado -> literal
    parts = re.split("\x00LIT(.)\x00", p)
    out = []
    for k, part in enumerate(parts):
        if k % 2 == 1:
            out.append(re.escape(part))
        else:
            out.append(_conv_regex(part, ere))
    return "".join(out)


def _repl_func(rep):
    parts = re.split("\x00LIT(.)\x00", rep)
    toks = []
    for k, part in enumerate(parts):
        if k % 2 == 1:
            toks.append(("lit", part))
            continue
        i = 0
        while i < len(part):
            ch = part[i]
            if ch == "\\" and i + 1 < len(part):
                nx = part[i + 1]
                if nx.isdigit():
                    toks.append(("grp", int(nx)))
                elif nx == "n":
                    toks.append(("lit", "\n"))
                elif nx == "t":
                    toks.append(("lit", "\t"))
                else:
                    toks.append(("lit", nx))
                i += 2
            elif ch == "&":
                toks.append(("grp", 0))
                i += 1
            else:
                toks.append(("lit", ch))
                i += 1

    def f(m):
        return "".join(v if t == "lit" else (m.group(v) or "") for t, v in toks)
    return f


def _text_arg(t):
    # texto de a/i/c: processa escapes GNU (\n -> nova linha, \x -> x)
    out = []
    i = 0
    while i < len(t):
        if t[i] == "\\" and i + 1 < len(t):
            nx = t[i + 1]
            out.append("\n" if nx == "n" else ("\t" if nx == "t" else nx))
            i += 2
        else:
            out.append(t[i])
            i += 1
    return "".join(out)


def parse(script, ere=False):
    cmds = []
    i = 0
    s = script
    while i < len(s):
        while i < len(s) and s[i] in " \t\n;":
            i += 1
        if i >= len(s):
            break
        addr = []
        for _ in range(2):
            if s[i].isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                addr.append(("line", int(s[i:j])))
                i = j
            elif s[i] == "/":
                p, i = _split_delim(s, i + 1, "/")
                addr.append(("re", re.compile(_finish_pat(p, ere))))
            if i < len(s) and s[i] == "," and len(addr) == 1:
                i += 1
                continue
            break
        c = s[i]
        if c == "s":
            d = s[i + 1]
            p, i = _split_delim(s, i + 2, d)
            r, i = _split_delim(s, i, d)
            flags = ""
            while i < len(s) and s[i] in "gpI0123456789":
                flags += s[i]
                i += 1
            cmds.append(dict(cmd="s", addr=addr, re=re.compile(_finish_pat(p, ere)), rep=_repl_func(r), g="g" in flags))
        elif c in "ci":
            if s[i + 1] != "\\":
                raise ValueError("forma de c/i nao suportada")
            text = s[i + 2:]
            # forma de uma linha: o texto vai ate o fim do script desta expressao
            nl = text.find("\n")
            if nl >= 0:
                text, rest = text[:nl], text[nl:]
            else:
                rest = ""
            cmds.append(dict(cmd=c, addr=addr, text=_text_arg(text)))
            s = rest
            i = 0
            continue
        else:
            raise ValueError("comando sed nao suportado: %r" % c)
    return cmds


def run(content, scripts, ere=False):
    """Aplica uma invocacao de sed (lista de expressoes -e) ao conteudo."""
    cmds = []
    for sc in scripts:
        cmds.extend(parse(sc, ere))
    had_final_nl = content.endswith("\n")
    lines = content.split("\n")
    if had_final_nl:
        lines = lines[:-1]
    out = []
    active = {}
    total_changes = 0
    for ln, line in enumerate(lines, start=1):
        ps = line
        deleted = False
        pre = []
        for k, c in enumerate(cmds):
            a = c["addr"]
            sel = True
            end_of_range = False
            if len(a) == 1:
                t, v = a[0]
                sel = (ln == v) if t == "line" else bool(v.search(line))
                end_of_range = sel
            elif len(a) == 2:
                if not active.get(k):
                    t, v = a[0]
                    start = (ln == v) if t == "line" else bool(v.search(line))
                    if start:
                        active[k] = True
                        sel = True
                        t2, v2 = a[1]
                        if t2 == "line" and v2 <= ln:
                            active[k] = False
                            end_of_range = True
                    else:
                        sel = False
                else:
                    sel = True
                    t2, v2 = a[1]
                    if (t2 == "line" and ln >= v2) or (t2 == "re" and v2.search(line)):
                        active[k] = False
                        end_of_range = True
            else:
                end_of_range = True
            if not sel:
                continue
            if c["cmd"] == "s":
                new, nsub = c["re"].subn(c["rep"], ps, count=0 if c["g"] else 1)
                if nsub:
                    total_changes += nsub
                ps = new
            elif c["cmd"] == "i":
                pre.append(c["text"])
                total_changes += 1
            elif c["cmd"] == "c":
                deleted = True
                total_changes += 1
                if end_of_range or len(a) < 2:
                    pre.append(c["text"])
                break
        out.extend(pre)
        if not deleted:
            out.append(ps)
    res = "\n".join(out)
    if had_final_nl:
        res += "\n"
    return res, total_changes
