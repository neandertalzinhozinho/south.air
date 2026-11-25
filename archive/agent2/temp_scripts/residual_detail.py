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
mask=onoise|cnoise
rem={i for i in range(N) if c[0][i]!=r[0][i]}-mask
print('residual',len(rem))
J1=(0x530000,0x1000); J2=(0x23CC700-0x217F000,9436)
inJ1=[i for i in rem if J1[0]<=i<J1[0]+J1[1]]
print('in janela1',len(inJ1),'in janela2',len([i for i in rem if J2[0]<=i<J2[0]+J2[1]]))
print('rest',len(rem)-len(inJ1))
srt=sorted(rem); rng=[]; st=pr=srt[0]
for x in srt[1:]:
    if x==pr+1: pr=x
    else: rng.append((st,pr)); st=pr=x
rng.append((st,pr))
print('ranges',len(rng))
for s,e in sorted(rng,key=lambda t:t[1]-t[0],reverse=True)[:10]:
    print(' ',hex(s),hex(e),e-s+1)
# values sample
print('sample oracle/cand:')
for i in srt[:8]:
    print(' ',hex(i),'orac',hex(r[0][i]),'cand',c[0][i])
# 0x532408 area across oracle runs and candidate runs
for off in (0x532408,0x5328d8):
    print('off',hex(off),'r1',r[0][off:off+16].hex(),'r2',r[1][off:off+16].hex(),'r3',r[2][off:off+16].hex(),'c1',c[0][off:off+16].hex())
# how many of the 95,679 extras are inside oracle floor?
S={i for i in range(N) if c[0][i]!=r[0][i]}-(cnoise)
extra={i for i in S if c[0][i] and r[0][i]==0}
print('extras vs r1 (cand floor only)',len(extra),'masked by oracle floor',sum(1 for i in extra if i in onoise))
# what does oracle have at 0x5301c0..0x5305c0 (CRC table) in r1
print('crc r1 head',r[0][0x5301c0:0x530200].hex())
print('crc c1 head',c[0][0x5301c0:0x530200].hex())
