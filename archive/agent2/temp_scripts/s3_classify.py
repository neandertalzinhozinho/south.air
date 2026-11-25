import json, os, collections
os.chdir(r'D:\PROJETOS\shadowFILES')
r=[open(f'analysis/startup_audit/post_create_candidate{s}_data.bin' if s else 'analysis/startup_audit/post_create_candidate_data.bin','rb').read() for s in ['','2','3']]
o=open('analysis/startup_audit/original_post_data.bin','rb').read()
fb=set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc=set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
N=len(r[0]); noise={i for i in range(N) if not(r[0][i]==r[1][i]==r[2][i])}
S={i for i in range(N) if r[0][i]!=o[i]} - (fb|fc|noise)
print('stable',len(S))
print('cand zero/oracle nz',sum(1 for i in S if r[0][i]==0 and o[i]!=0))
print('both nz',sum(1 for i in S if r[0][i] and o[i]))
print('cand nz/oracle zero',sum(1 for i in S if r[0][i] and o[i]==0))
blocks=collections.Counter(i>>16 for i in S)
for b,c in blocks.most_common(12): print(hex(b<<16),c)
# value-pair histogram for both-nz
hc=collections.Counter((r[0][i],o[i]) for i in S if r[0][i] and o[i])
print(hc.most_common(8))
print('oracle byte hist',collections.Counter(o[i] for i in S).most_common(8))
