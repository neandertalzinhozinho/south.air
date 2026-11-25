import pefile, os, math, collections
ROOT=r'D:\PROJETOS\shadowFILES'
A=os.path.join(ROOT,r'analysis\host_reference\startup_capture\original_before_load.vst3')
U=os.path.join(ROOT,r'analysis\startup_audit\final_candidate_uni46c.vst3')
D=os.path.join(ROOT,'soothe3_unpacked_mem.bin')
def rd(p,name):
    pe=pefile.PE(p,fast_load=True)
    for s in pe.sections:
        if s.Name.rstrip(b'\x00').decode('latin1')==name:
            f=open(p,'rb');f.seek(s.PointerToRawData);b=f.read(s.SizeOfRawData);f.close();return b
    return None
def H(b):
    c=collections.Counter(b);n=len(b)
    return -sum((v/n)*math.log2(v/n) for v in c.values() if v)
uT=rd(U,'.text'); f=open(D,'rb');f.seek(0x1000);dT=f.read(len(uT));f.close()
aT=rd(A,'.text')
print('uni46c .text == dump .text :',uT==dT)
n=min(len(aT),len(uT));print('buildA .text H=%.2f  uni46c .text H=%.2f  dump .text H=%.2f'%(H(aT),H(uT),H(dT)))
print('buildA .text zero%%=%.2f  uni46c=%.2f'%(100*aT.count(0)/len(aT),100*uT.count(0)/len(uT)))
pe=pefile.PE(U,fast_load=True)
for s in pe.sections:
    nm=s.Name.rstrip(b'\x00').decode('latin1')
    if nm in('.imports','.inits'):
        f=open(U,'rb');f.seek(s.PointerToRawData);b=f.read(s.SizeOfRawData);f.close()
        print('%s va=0x%X vsize=%d raw=%d'%(nm,s.VirtualAddress,s.Misc_VirtualSize,len(b)))
        print('   hex:',b[:96].hex())
        print('   ascii:',repr(b[:200]))
