import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
r=[open(f'analysis/startup_audit/post_create_candidate{s}_data.bin' if s!='' else 'analysis/startup_audit/post_create_candidate_data.bin','rb').read() for s in ['','2','3']]
o=open('analysis/startup_audit/original_post_data.bin','rb').read()
fb=set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc=set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
N=len(r[0])
noise=set()
for i in range(N):
    if not (r[0][i]==r[1][i]==r[2][i]): noise.add(i)
print('3-run noise',len(noise))
mask=fb|fc|noise
for k,x in enumerate(r):
    d={i for i in range(N) if x[i]!=o[i]}
    print('run',k+1,'raw',len(d),'masked',len(d-mask))
d1={i for i in range(N) if r[0][i]!=o[i]}
print('stable masked set',len(d1-mask))
J2=(0x23CC700-0x217F000,9436); J1=(0x26AF000-0x217F000,4096)
S=d1-mask
print('j2',len([i for i in S if J2[0]<=i<J2[0]+J2[1]]),'j1',len([i for i in S if J1[0]<=i<J1[0]+J1[1]]))
print('nz',[sum(1 for b in x if b) for x in r])
