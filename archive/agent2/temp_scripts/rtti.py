import struct, re, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
IB=0x180000000
def u32(o): return struct.unpack_from('<I',d,o)[0]
def i32(o): return struct.unpack_from('<i',d,o)[0]
def u64(o): return struct.unpack_from('<Q',d,o)[0]
# TypeDescriptor for Soothe3AudioProcessor
td=0x23ade18
print('td bytes', d[td:td+16].hex())
# find RTTI CompleteObjectLocator: signature 1, pTypeDescriptor RVA == td
cols=[]
for o in range(0x2180000, 0x2758000-28, 4):
    sig=u32(o)
    if sig in (0,1):
        off,cd,tdrva,chdr = struct.unpack_from('<IIIi', d, o+4)
        if tdrva == td:
            cols.append((o,sig,off,cd,tdrva,chdr))
print('COLs:',[(hex(a),s,hex(o),hex(c)) for a,s,o,c,t,h in cols])
# vtables in .rdata referencing COL VA
targets=set()
for a,s,o,c,t,h in cols:
    targets.add((a+IB)&0xffffffffffffffff)
print('targets',[hex(t) for t in targets])
for o in range(0x1d8c000, 0x217f000-8, 8):
    v=u64(o)
    if v in targets:
        print('VTABLE at', hex(o), 'VA', hex(o+IB))
        for j in range(12):
            print('   +%02x'%(j*8), hex(u64(o+j*8)))
