import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
def rd(p): return open(p,'rb').read()
r1 = rd('analysis/startup_audit/oracleA_create_r1_data.bin')
r2 = rd('analysis/startup_audit/oracleA_create_r2_data.bin')
old = rd('analysis/startup_audit/original_post_data.bin')
c1 = rd('analysis/startup_audit/post_create_candidate_data.bin')
c2 = rd('analysis/startup_audit/post_create_candidate2_data.bin')
c3 = rd('analysis/startup_audit/post_create_candidate3_data.bin')
fb = set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc = set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
N = len(r1)
print('r1 nz', sum(1 for b in r1 if b), 'r2 nz', sum(1 for b in r2 if b), 'old nz', sum(1 for b in old if b))
d = lambda a,b: sum(1 for i in range(N) if a[i]!=b[i])
print('r1 vs r2 raw', d(r1,r2))
print('r1 vs old', d(r1,old))
noise = {i for i in range(N) if r1[i]!=r2[i]}
print('oracle create noise', len(noise), 'new outside fb/fc', len(noise-fb-fc))
mask = fb|fc|noise
for nm, x in [('cand1',c1),('cand2',c2),('cand3',c3)]:
    dd = {i for i in range(N) if x[i]!=r1[i]}
    print(nm, 'vs r1 raw', len(dd), 'outside oracle-create-floor', len(dd-mask))
# where is the noise concentrated?
import collections
b = collections.Counter(i>>16 for i in noise)
print('noise blocks', [(hex(k<<16),v) for k,v in b.most_common(6)])
# candidate remaining after union of both create floors (candidate run noise too)
cnoise = {i for i in range(N) if not(c1[i]==c2[i]==c3[i])}
full = fb|fc|noise|cnoise
for nm, x in [('cand1',c1)]:
    dd = {i for i in range(N) if x[i]!=r1[i]}
    print(nm, 'outside union floors', len(dd-full))
# compare janela2 heads
o2 = 0x23CC700-0x217F000
for nm,x in [('r1',r1),('r2',r2),('old',old),('c1',c1)]:
    print(nm, 'j2 head', x[o2:o2+24].hex())
