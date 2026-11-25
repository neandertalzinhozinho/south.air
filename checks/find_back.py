import re
lines=[l.rstrip() for l in open(r"checks/873440.dis",encoding="utf-8",errors="replace")]
for l in lines:
    m=re.match(r"\s*([0-9A-F]{8})\s+(j\w+)\s+(0x[0-9a-f]+)",l)
    if m:
        src=int(m.group(1),16); tgt=int(m.group(3),16)
        if src>=0x876000 and tgt<0x874200:
            print(l)
