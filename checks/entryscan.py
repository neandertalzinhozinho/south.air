import re
lines=[l.rstrip() for l in open(r"checks/873440.dis",encoding="utf-8",errors="replace")]
for l in lines:
    m=re.match(r"\s*([0-9A-F]{8})\s+(j\w+)\s+(0x[0-9a-f]+)",l)
    if m:
        s=int(m.group(1),16); t=int(m.group(3),16)
        if s < 0x873E6D and t >= 0x874190:
            print(l.strip())
print("---- targets inside 873e6d..874190 ----")
for l in lines:
    m=re.match(r"\s*([0-9A-F]{8})\s+(j\w+)\s+(0x[0-9a-f]+)",l)
    if m:
        s=int(m.group(1),16); t=int(m.group(3),16)
        if 0x873E6D <= t <= 0x874190:
            print(l.strip())
