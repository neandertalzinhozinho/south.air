"""Lista, para cada Edit/Write/Read do Claude, as chaves de toolUseResult e o tamanho de originalFile."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import events  # noqa: E402

for e in sorted(events.claude_events(), key=lambda e: e["ts"]):
    if e["name"] not in ("Edit", "Write", "Read"):
        continue
    t = e["tur"]
    fp = e["input"].get("file_path", "")
    if not isinstance(t, dict):
        print(e["ts"], e["name"], os.path.basename(fp), "tur=", type(t).__name__)
        continue
    of = t.get("originalFile")
    extra = ""
    if e["name"] == "Read":
        f = t.get("file") or {}
        extra = "start=%s num=%s total=%s" % (f.get("startLine"), f.get("numLines"), f.get("totalLines"))
    print(e["ts"], e["name"], fp.replace("D:\\PROJETOS\\soultree\\app\\", ""), sorted(t.keys()),
          "originalFile=%s" % (len(of) if isinstance(of, str) else of), extra)
