lines=open(r"checks/decomp/0x180885040.c",encoding="utf-8",errors="replace").read().splitlines()
for i,l in enumerate(lines,1):
    if "8b2680" in l:
        print("---- around line",i)
        for j in range(max(0,i-60),min(len(lines),i+30)):
            print(j+1, lines[j])
