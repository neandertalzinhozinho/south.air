import subprocess, sys
from pathlib import Path
ROOT = Path(r"D:\PROJETOS\soultree")
addr = sys.argv[1]
out = ROOT / "checks" / ("m_%s.dis" % addr.lower().replace("0x", ""))
p = subprocess.run([sys.executable, str(ROOT / "tools" / "show_func.py"), addr],
                   cwd=str(ROOT), capture_output=True)
txt = p.stdout.decode("utf-8", errors="replace")
if p.stderr:
    txt += "\n; STDERR:\n" + p.stderr.decode("utf-8", errors="replace")
out.write_text(txt, encoding="utf-8")
print(out, len(txt))
