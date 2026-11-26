"""Mostra o comando completo (input) e a saida de eventos Claude pelos timestamps dados (HH:MM:SS)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402

want = sys.argv[1:]
show_out = os.environ.get("SHOWOUT") == "1"
for e in sorted(events.claude_events(), key=lambda e: e["ts"]):
    if e["ts"][11:19] in want:
        print("=" * 20, e["ts"], e["name"])
        inp = e["input"]
        print(inp.get("command") if "command" in inp else inp)
        if show_out:
            print("----- RESULT -----")
            print(e["result"])
