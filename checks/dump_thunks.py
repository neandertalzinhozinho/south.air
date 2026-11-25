import re
txt=open(r"checks/thunk_semantics.txt",encoding="utf-8",errors="replace").read()
parts=re.split(r"thunk (0x[0-9A-F]+)",txt)
want={"0x10A0","0x10D0","0x1010","0x1280","0x1220"}
for i in range(1,len(parts),2):
    if parts[i] in want:
        print("thunk",parts[i])
        print(parts[i+1][:2500])
