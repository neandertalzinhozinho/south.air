from pathlib import Path
t=Path("docs/engine/dsp-spec.md").read_text(encoding="utf-8")
for l in t.splitlines():
    if "0x3FE6A09E667F3BCC" in l:
        print(repr(l))
