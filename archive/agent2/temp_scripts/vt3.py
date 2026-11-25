import struct, sys
sys.path.insert(0, r'D:\PROJETOS\soultree\tools')
import re_lib
p=r'D:\PROJETOS\soultree\dumpsooth\nyx_soothe3_dump.bin'
d=open(p,'rb').read()
BASE=0x199b0000
T0,T1=0x1000,0x1d8bb7d
runs=[];cur=[]
for o in range(0x1d8c000,0x2758000,8):
    v=struct.unpack_from('<Q',d,o)[0]
    if T0<=v-BASE<T1:
        if not cur: cur=[o]
        cur.append(v)
    else:
        if len(cur)-1>=5: runs.append(cur[0])
        cur=[]
print('vtables>=5:',len(runs))
# load xrefs map target->funcs
import csv, collections
refs=collections.defaultdict(set)
with open(r'D:\PROJETOS\soultree\docs\engine\xrefs.csv',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['kind']=='rip':
            refs[int(row['target'],16)].add(int(row['func'],16))
found=[]
for vt in runs:
    fs=refs.get(vt)
    if fs: found.append((vt,sorted(fs)))
print('with ctor refs:',len(found))
for vt,fs in found[:40]:
    print(hex(vt),[hex(x) for x in fs])
