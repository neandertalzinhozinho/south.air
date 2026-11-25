import io
lines=open(r"checks/decomp/0x180885040.c",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(lines,1):
    if "8b2680" in l.lower():
        print("---- line",i,"----")
        for j in range(max(0,i-18), min(len(lines), i+10)):
            print(lines[j])
