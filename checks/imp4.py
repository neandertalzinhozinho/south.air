import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
def u32(o): return struct.unpack_from("<I",data,o)[0]
def u64(o): return struct.unpack_from("<Q",data,o)[0]
def resolve(a):
    # find ff 25 within +-8 of a
    for i in range(a-8,a+8):
        if data[i]==0xff and data[i+1]==0x25:
            slot=i+6+struct.unpack_from("<i",data,i+2)[0]
            return slot
    return None
for fn in (0x1C9A5A1,0x1C9AA01,0x1C9A9FB):
    s=resolve(fn); print(hex(fn),"slot",hex(s) if s else None)
# map slot->name using INT array of math dll
intb=0x2176878; iat=0x1D8D790
names={}
k=0
while True:
    rva=u64(intb+k*8)
    if rva==0: break
    nm=rva+2; end=data.find(b"\x00",nm)
    names[iat+k*8]=data[nm:end].decode("ascii","replace"); k+=1
for fn in (0x1C9A5A1,0x1C9AA01,0x1C9A9FB):
    s=resolve(fn); print(hex(fn),"->",names.get(s,"?"))
