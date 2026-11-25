import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
a=open('analysis/startup_audit/post_create_candidate_data.bin','rb').read()
b=open('analysis/startup_audit/post_create_candidate2_data.bin','rb').read()
o=open('analysis/startup_audit/original_post_data.bin','rb').read()
fb=set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc=set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
n=[i for i in range(len(a)) if a[i]!=b[i]]
print('run1 vs run2 diff',len(n))
nd=set(n)
print('new run noise outside old cand floor',len([i for i in n if i not in fc]))
def stats(x,name):
    raw=[i for i in range(len(x)) if x[i]!=o[i]]
    print(name,'raw',len(raw),'outB',len([i for i in raw if i not in fb]),'outB+cand+newnoise',len([i for i in raw if i not in fb and i not in fc and i not in nd]))
stats(a,'run1')
stats(b,'run2')
print('meta', json.load(open('analysis/startup_audit/post_create_candidate2_meta.json'))['created'])
# region stats run2
def rng(x,name,off,n):
    s=[i for i in range(off,off+n) if x[i]!=o[i]]
    print(name,'raw',len(s),'nz_x',sum(1 for i in range(off,off+n) if x[i]),'nz_o',sum(1 for i in range(off,off+n) if o[i]))
rng(b,'j2',0x23CC700-0x217F000,9436); rng(b,'j1',0x26AF000-0x217F000,4096)
print('nz run2',sum(1 for x in b if x),'nz run1',sum(1 for x in a if x),'nz orac',sum(1 for x in o if x))
