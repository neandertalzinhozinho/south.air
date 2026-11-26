"""Carrega eventos de ferramentas das sessoes (Claude Code e Codex) como DADOS.

Nada aqui executa comandos tirados dos registros: apenas le JSON.
"""
import glob
import json
import os

BASE = r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao"
APP = "D:\\PROJETOS\\soultree\\app\\"


def _text_of(c):
    if isinstance(c, list):
        return "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
    return c if isinstance(c, str) else ("" if c is None else str(c))


def claude_events():
    """Lista de dicts: ts, session, sidechain, name, input, is_error, result_text, tur."""
    evs = []
    for f in sorted(glob.glob(os.path.join(BASE, "claude", "**", "*.jsonl"), recursive=True)):
        uses = {}
        res = {}
        for line in open(f, encoding="utf-8"):
            o = json.loads(line)
            t = o.get("type")
            if t == "assistant":
                for b in o["message"].get("content", []):
                    if isinstance(b, dict) and b.get("type") == "tool_use":
                        uses[b["id"]] = (o.get("timestamp"), b["name"], b["input"], bool(o.get("isSidechain")))
            elif t == "user" and isinstance(o["message"].get("content"), list):
                for b in o["message"]["content"]:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        res[b["tool_use_id"]] = (b.get("is_error"), _text_of(b.get("content")), o.get("toolUseResult"))
        for k, (ts, name, inp, sc) in uses.items():
            r = res.get(k)
            evs.append(dict(src="claude", file=os.path.basename(f), id=k, ts=ts, sidechain=sc, name=name, input=inp,
                            has_result=r is not None, is_error=bool(r and r[0]), result=r[1] if r else None,
                            tur=r[2] if r else None))
    return evs


def codex_events():
    evs = []
    for f in sorted(glob.glob(os.path.join(BASE, "codex", "*.jsonl"))):
        calls = {}
        outs = {}
        for line in open(f, encoding="utf-8"):
            o = json.loads(line)
            p = o.get("payload", {})
            if o.get("type") == "response_item":
                pt = p.get("type")
                if pt in ("custom_tool_call", "function_call"):
                    calls[p["call_id"]] = (o["timestamp"], p.get("name"), p.get("input") or p.get("arguments"))
                elif pt in ("custom_tool_call_output", "function_call_output"):
                    outs[p["call_id"]] = p.get("output")
        for k, (ts, name, inp) in calls.items():
            out = outs.get(k)
            if isinstance(out, str):
                try:
                    out = json.loads(out)
                except Exception:
                    pass
            evs.append(dict(src="codex", file=os.path.basename(f), id=k, ts=ts, name=name, input=inp,
                            output=_text_of(out) if not isinstance(out, dict) else json.dumps(out)))
    return evs
