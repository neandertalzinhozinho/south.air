import struct, collections, os
ROOT=r'D:\PROJETOS\shadowFILES'
D=os.path.join(ROOT,'soothe3_unpacked_mem.bin')
DELTA=0xCC0000; PREF=0x180000000; IMG=0x82A4F00
f=open(D,'rb')
def words(rva,size):
    f.seek(rva); b=f.read(size); n=len(b)//8
    return struct.unpack('<%dQ'%n, b[:n*8])
def teste(tag,rva,size):
    vals=words(rva,size)
    cand=[v for v in vals if 0x10000<=v<0x800000000000 and (v&0xFFF) and v>0x1000000]
    cr=[v for v in cand if v>0xFFFFFFFF]          # >32 bits
    hits_asis=sum(1 for v in cr if 0<=v-0x18CC0000<IMG)
    hits_neg =sum(1 for v in cr if 0<=v-DELTA-PREF<IMG)
    hits_pref=sum(1 for v in cr if 0<=v-PREF<IMG)
    print('%-12s qwords=%7d  >32bit=%6d' % (tag,len(vals),len(cr)))
    print('   como esta (base 0x18CC0000): %6d  %.1f%%' % (hits_asis,100.0*hits_asis/max(1,len(cr))))
    print('   -0xCC0000 -> pref 0x180000000: %6d  %.1f%%' % (hits_neg,100.0*hits_neg/max(1,len(cr))))
    print('   sem ajuste (pref direto):     %6d  %.1f%%' % (hits_pref,100.0*hits_pref/max(1,len(cr))))
teste('.rdata',0x1D8C000,0x3F2CE8)
teste('.data',0x217F000,0x5D8DF8)
teste('.data001',0x79CD000,0x2828)
f.close()
print()
print('0x2068C158 - 0x79CC158 = 0x%X' % (0x2068C158-0x79CC158))
print('0x1AD97E70 - 0x20D7E70 = 0x%X' % (0x1AD97E70-0x20D7E70))
print('0x1B36E7E0 - 0x26AE7E0 = 0x%X' % (0x1B36E7E0-0x26AE7E0))
