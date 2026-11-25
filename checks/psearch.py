import re
d=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
print(len(d))
def find(s):
    out=[]
    b=s.encode("ascii")
    i=d.find(b)
    while i!=-1 and len(out)<20:
        out.append(hex(i))
        i=d.find(b,i+1)
    print(s, out)
for s in [b"depth",b"sharpness",b"selectivity",b"mix",b"output",b"sidechain",b"delta",b"attack",b"release",b"knee",b"ratio"]:
    find(s.decode())
