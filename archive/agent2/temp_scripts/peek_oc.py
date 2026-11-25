import sqlite3, os, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

p = os.path.expanduser(r"~/.local/share/opencode/opencode.db")
c = sqlite3.connect("file:" + p + "?mode=ro", uri=True)
c.row_factory = sqlite3.Row

row = c.execute("select data from session_message where id=?", ("msg_1f444d068001WdtqYd46xFPWFQ",)).fetchone()
d = json.loads(row["data"])
out = []
for item in d.get("content", []):
    if item.get("type") == "text":
        out.append(item.get("text", ""))
open(os.path.join(os.path.dirname(__file__), "answer.txt"), "w", encoding="utf-8").write("\n=====\n".join(out))
print("written", sum(len(x) for x in out))
