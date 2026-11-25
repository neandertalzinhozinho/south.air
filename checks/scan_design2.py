import re
for f in ["0x18087fd60","0x18087f780","0x18087f0c0","0x18087b2a0"]:
    p=r"checks/decomp/%s.c"%f
    lines=open(p,encoding="utf-8",errors="replace").read().splitlines()
    print("=====",f)
    for i,l in enumerate(lines,1):
        if "param_2" in l and ("0x18" in l or "0x10" in l or "param_2[" in l or "*param_2" in l):
            print(i, l.strip()[:160])
