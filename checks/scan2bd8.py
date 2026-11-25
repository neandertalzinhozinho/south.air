import re, subprocess, sys
# scan disassembly of key functions for 0x2bd8/0x2bf0 references
import glob, os
for f in glob.glob("checks/*.dis"):
    txt=open(f,encoding="utf-8",errors="replace").read()
    if "0x2bd8" in txt or "0x2bf0" in txt:
        hits=[l.strip() for l in txt.splitlines() if ("0x2bd8" in l or "0x2bf0" in l)]
        print(f, len(hits))
        for h in hits[:8]:
            print("   ", h)
