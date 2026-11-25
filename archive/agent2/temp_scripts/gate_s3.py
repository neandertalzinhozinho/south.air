import json, os, collections
os.chdir(r'D:\PROJETOS\shadowFILES')
rd=lambda p: open(p,'rb').read()
r=[rd(f'analysis/startup_audit/oracleA_create_r{i}_data.bin') for i in (1,2,3)]
c=[rd('analysis/startup_audit/post_create_candidate_data.bin'),
   rd('analysis/startup_audit/post_create_candidate2_data.bin'),
   rd('analysis/startup_audit/post_create_candidate3_data.bin')]
N=len(r[0])
onoise={i for i in range(N) if not(r[0][i]==r[1][i]==r[2][i])}
cnoise={i for i in range(N) if not(c[0][i]==c[1][i]==c[2][i])}
print('oracle create floor (3 runs)',len(onoise))
print('candidate create floor (3 runs)',len(cnoise))
mask=onoise|cnoise
print('union',len(mask))
def cmp(x,ref,name):
    d={i for i in range(N) if x[i]!=ref[i]}
    rem=d-mask
    print(name,'raw',len(d),'outside union',len(rem))
    print('  cand0/oracnz',sum(1 for i in rem if x[i]==0),'both nz',sum(1 for i in rem if x[i] and ref[i]),'candnz/orac0',sum(1 for i in rem if x[i] and ref[i]==0))
    b=collections.Counter(i>>16 for i in rem)
    print('  blocks',[(hex(k<<16),v) for k,v in b.most_common(5)])
    return rem
s1=cmp(c[0],r[0],'cand1 vs r1')
cmp(c[1],r[0],'cand2 vs r1')
cmp(c[2],r[0],'cand3 vs r1')
# cross check: oracle runs vs each other outside mask (must be 0)
for i in (1,2):
    dd={j for j in range(N) if r[i][j]!=r[0][j]}
    print('r%d vs r1 outside mask'%(i+1), len(dd-mask))
print('j2 fields across runs:')
off=0x23CC700-0x217F000
for nm,x in [('r1',r[0]),('r2',r[1]),('r3',r[2]),('c1',c[0]),('c2',c[1]),('c3',c[2])]:
    print(nm, 'ptr',x[off:off+8].hex(),'f8',x[off+8:off+12].hex(),'fc',x[off+12:off+16].hex(),'f10',x[off+16:off+20].hex())
