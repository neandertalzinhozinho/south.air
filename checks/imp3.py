import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def u32(o): return struct.unpack_from("<I",data,o)[0]
def u64(o): return struct.unpack_from("<Q",data,o)[0]
intb=0x2176878
for k in range(0,22):
    rva=u64(intb+k*8)
    if rva==0: print(k,"null"); continue
    nm=rva+2
    end=data.find(b"\x00",nm)
    print(k,hex(rva),data[nm:end].decode("ascii","replace"))
