import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
base = 'analysis/startup_audit/precreate261'
ai = open(f'{base}_after_inits_data.bin','rb').read()
ac = open(f'{base}_after_create_data.bin','rb').read()
o = open('analysis/startup_audit/original_post_data.bin','rb').read()
st = json.load(open('analysis/startup_audit/post_create_stability.json',encoding='utf-8'))
fb = set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc = set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
print('sizes', len(ai), len(ac), len(o))
d_pre = {i for i in range(len(o)) if ai[i]!=o[i]}
d_post = {i for i in range(len(o)) if ac[i]!=o[i]}
print('pre-create raw', len(d_pre), 'outside B', len(d_pre-fb), 'outside B+cand', len(d_pre-fb-fc))
print('post-create raw', len(d_post), 'outside B', len(d_post-fb))
# stable create set = offsets where cand nonzero oracle zero at post, from 3-run stability json
S = None
# recompute stable set from 3 runs as in the ledger
r=[open(f'analysis/startup_audit/post_create_candidate{s}_data.bin' if s else 'analysis/startup_audit/post_create_candidate_data.bin','rb').read() for s in ['','2','3']]
N=len(o)
noise={i for i in range(N) if not(r[0][i]==r[1][i]==r[2][i])}
mask=fb|fc|noise
S={i for i in range(N) if r[0][i]!=o[i]} - mask
extra={i for i in S if r[0][i]!=0 and o[i]==0}
print('stable', len(S), 'extra', len(extra))
print('extra zero pre-inits', sum(1 for i in extra if ai[i]==0), 'nonzero pre', sum(1 for i in extra if ai[i]!=0))
print('extra same value pre as post', sum(1 for i in extra if ai[i]==ac[i]), 'changed by create', sum(1 for i in extra if ai[i]!=ac[i]))
# the 128 pair bytes
pairs = [i for i in S if r[0][i]==o[i]+1]
print('cand=orac+1 count', len(pairs))
for i in pairs[:4]:
    print(hex(i), 'pre', ai[i], 'post', ac[i], 'orac', o[i], 'run1', r[0][i])
# missing writes
miss={i for i in S if r[0][i]==0 and o[i]!=0}
print('missing', len(miss), 'nonzero at after_inits', sum(1 for i in miss if ai[i]!=0))
# region split of extra vs pre-create zero
print('extra in 0x530000-0x594000', sum(1 for i in extra if 0x530000<=i<0x594000))
