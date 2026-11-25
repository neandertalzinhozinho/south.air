import struct
data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
base=0x1C9A980
b=data[base:base+0x160]
for i in range(0,len(b)-6,6):
    pass
# find ff25
for i in range(len(b)-6):
    if b[i]==0xff and b[i+1]==0x25:
        disp=struct.unpack_from("<i",b,i+2)[0]
        tgt=base+i+6+disp
        print(hex(base+i),"jmp ->",hex(tgt))
