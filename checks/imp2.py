import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
target=0x217A81E
pat=struct.pack("<I",target)
idx=[]; s=0
while True:
    i=data.find(pat,s)
    if i<0: break
    idx.append(i); s=i+1
    if len(idx)>20: break
print([hex(i) for i in idx])
for i in idx:
    desc=i-12
    oft,tds,fc,name,ft=struct.unpack_from("<IIIII",data,desc)
    if name==target:
        print("desc at",hex(desc),"OFT",hex(oft),"FT",hex(ft))
