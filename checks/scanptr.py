import struct
data=open(r"dumpsooth/nyx_soothe3_dump.bin","rb").read()
print("size",len(data))
# image base used by data pointers is 0x199B0000 for RVA 0? check: find known .rdata ptr e.g. 0x2077580 -> VA?
targets={"0x880390":0x880390,"0x619D90":0x619D90,"0x873440":0x873440,"0x8780D0":0x8780D0}
for name,rva in targets.items():
    for base in (0x199B0000,0x180000000):
        pat=struct.pack("<Q",base+rva)
        idx=[]; start=0
        while True:
            i=data.find(pat,start)
            if i<0: break
            idx.append(i); start=i+1
            if len(idx)>12: break
        print(name,hex(base+rva),"qword hits",len(idx),[hex(x) for x in idx][:8])
        pat4=struct.pack("<I",(base+rva)&0xffffffff)
        idx=[]; start=0
        while True:
            i=data.find(pat4,start)
            if i<0: break
            idx.append(i); start=i+1
            if len(idx)>12: break
        print("   dword hits",len(idx),[hex(x) for x in idx][:8])
