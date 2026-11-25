import re
for f in ["0x18087fd60","0x18087f780","0x18087f0c0","0x180877d90","0x18087b2a0"]:
    p=r"checks/decomp/%s.c"%f
    txt=open(p,encoding="utf-8",errors="replace").read()
    lines=txt.splitlines()
    print("=====",f,"lines",len(lines))
    for i,l in enumerate(lines,1):
        if re.search(r"(2bd8|2bf0|0xf0|0x108|0x210|\+ 0x40|0x40\))", l):
            print(i, l.strip()[:150])
