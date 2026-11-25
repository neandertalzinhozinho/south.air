import pefile, os, struct
ROOT=r'D:\PROJETOS\shadowFILES'
def slot(path, rva, n=8):
    pe=pefile.PE(path,fast_load=True); f=open(path,'rb')
    for s in pe.sections:
        va=s.VirtualAddress; sz=max(s.Misc_VirtualSize,s.SizeOfRawData)
        if va<=rva<va+sz:
            f.seek(s.PointerToRawData+(rva-va)); b=f.read(n); f.close()
            return s.Name.rstrip(b'\x00').decode('latin1'), b
    f.close(); return None,None
alvos={ 'buildA':os.path.join(ROOT,r'analysis\host_reference\startup_capture\original_before_load.vst3'),
        'uni45':os.path.join(ROOT,r'analysis\startup_audit\final_candidate_uni45.vst3'),
        'uni46c':os.path.join(ROOT,r'analysis\startup_audit\final_candidate_uni46c.vst3'),
        'v7d':os.path.join(ROOT,r'analysis\startup_audit\vars\v7d.bin'),
        'fixed.pe':os.path.join(ROOT,'soothe3_unpacked_fixed.pe') }
for rva,nome in ((0x79CC440,'TLS.AddressOfCallBacks'),(0x79CC428,'TLS dir start'),(0x79CC430,'TLS dir+8'),(0x79CC438,'TLS dir+0x10')):
    print('--- rva 0x%X %s'%(rva,nome))
    for k,p in alvos.items():
        if not os.path.exists(p): print('   %-8s ausente'%k); continue
        s,b=slot(p,rva)
        v=struct.unpack('<Q',b)[0] if b and len(b)==8 else None
        print('   %-8s %-10s %s'%(k,s,('0x%016X'%v) if v is not None else 'n/d'))
pe=pefile.PE(os.path.join(ROOT,'soothe3_unpacked_mem.bin'),fast_load=True) if 0 else None
