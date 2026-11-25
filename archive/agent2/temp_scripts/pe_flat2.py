import struct, math, collections

p = r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d = open(p,'rb').read()
SIZE=len(d); IMAGEBASE=0x180000000
def u16(o): return struct.unpack_from('<H',d,o)[0]
def u32(o): return struct.unpack_from('<I',d,o)[0]
def u64(o): return struct.unpack_from('<Q',d,o)[0]
pe_off=u32(0x3c); opt=u16(pe_off+20); magic=u16(pe_off+24)
dd = pe_off+24+(112 if magic==0x20b else 96)
print('magic',hex(magic),'pe_off',hex(pe_off),'opt',opt)
for idx in range(16):
    va,sz=struct.unpack_from('<II',d,dd+8*idx)
    if va or sz: print('dir',idx,hex(va),hex(sz))

exp=struct.unpack_from('<II',d,dd)[0]
if exp:
    eo=exp
    chars,ts,maj,minr,name_rva,base,nfunc,nname,funcs,names,ords=struct.unpack_from('<IIHHIIIIIII',d,eo)
    print('EXPORTS base',base,'nfunc',nfunc,'nname',nname,'dllname',d[name_rva:d.index(b"\0",name_rva)].decode(errors='replace'))
    out=[]
    for i in range(min(nname,400)):
        nr=u32(names+4*i)
        out.append((d[nr:d.index(b"\0",nr)].decode(errors='replace'), u32(ords+2*i), u32(funcs+4*u32(ords+2*i))))
    for n,o,a in out[:80]: print(' ',n,'ord',o,hex(a+IMAGEBASE))

imp=struct.unpack_from('<II',d,dd+8)[0] if False else struct.unpack_from('<II',d,dd+8*1)[0]
print('IMPORTS at',hex(imp))
if imp:
    o=imp
    while o+20<=SIZE:
        ilt,ts,fwd,nm,iat=struct.unpack_from('<IIIII',d,o)
        if not (ilt or nm): break
        dll=d[nm:d.index(b"\0",nm)].decode(errors='replace')
        names=[]; t=ilt or iat
        while t and t+8<=SIZE:
            v=u64(t)
            if v==0: break
            if v&0x8000000000000000: names.append('ord%d'%(v&0xffff))
            else:
                no=(v&0x7fffffff)+2
                names.append(d[no:d.index(b"\0",no)].decode(errors='replace'))
            t+=8
        print(' ',dll,len(names),names[:8])
        o+=20
