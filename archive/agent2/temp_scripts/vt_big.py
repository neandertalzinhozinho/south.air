import struct, csv, collections
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x199b0000; T0,T1=0x1000,0x1d8bb7d
def vlen(vt):
    n=0
    while True:
        v=struct.unpack_from('<Q',d,vt+8*n)[0]
        if not (T0<=v-BASE<T1): break
        n+=1
        if n>2000: break
    return n
# candidate vt starts: every address whose prev qword is not a code ptr and current is
cands=[]
for o in range(0x1d8c000,0x2758000-8,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if T0<=v-BASE<T1:
        pv=struct.unpack_from('<Q',d,o-8)[0] if o>=8 else 0
        if not (T0<=pv-BASE<T1):
            n=vlen(o)
            if n>=20: cands.append((o,n))
print('vtables>=20:',len(cands))
refs=collections.defaultdict(set)
with open(r'D:\PROJETOS\soultree\docs\engine\xrefs.csv',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['kind']=='rip':
            refs[int(row['target'],16)].add(int(row['func'],16))
for vt,n in cands:
    fs=refs.get(vt)
    print(hex(vt),'len',n,'refs',[hex(x) for x in sorted(fs)][:6] if fs else [])
