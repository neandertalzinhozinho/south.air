import re
lines=[l.rstrip() for l in open(r"checks/873440.dis",encoding="utf-8",errors="replace")]
jumps=[]
for l in lines:
    m=re.match(r"\s*([0-9A-F]{8})\s+(j\w+|loop\w*)\s+(0x[0-9a-f]+)",l)
    if m:
        src=int(m.group(1),16); tgt=int(m.group(3),16)
        if tgt<src:
            jumps.append((src,tgt,l.strip()))
print("backward jumps:",len(jumps))
for s,t,l in jumps:
    print(l)
