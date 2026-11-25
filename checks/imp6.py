import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def u64(o): return struct.unpack_from("<Q",data,o)[0]
intb=0x2176878; iat=0x1D8D790
names={}; k=0
while True:
    rva=u64(intb+k*8)
    if rva==0: break
    nm=rva+2; end=data.find(b"\x00",nm)
    names[iat+k*8]=data[nm:end].decode("ascii","replace"); k+=1
base=0x1C9A000
for i in range(base,0x1C9A800):
    if data[i]==0xff and data[i+1]==0x25:
        slot=i+6+struct.unpack_from("<i",data,i+2)[0]
        if 0x1D8D700 <= slot <= 0x1D8E000:
            if i==0x1C9A5A1: print("MATCH",hex(i),"slot",hex(slot),names.get(slot,"?"))
print("--- stubs near 0x1C9A5A1 ---")
for i in range(0x1C9A580,0x1C9A5C0):
    if data[i]==0xff and data[i+1]==0x25:
        slot=i+6+struct.unpack_from("<i",data,i+2)[0]
        print(hex(i),"slot",hex(slot),names.get(slot,"?"))
