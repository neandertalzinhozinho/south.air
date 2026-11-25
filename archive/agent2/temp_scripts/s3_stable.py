import json, os
os.chdir(r'D:\PROJETOS\shadowFILES')
a=open('analysis/startup_audit/post_create_candidate_data.bin','rb').read()
b=open('analysis/startup_audit/post_create_candidate2_data.bin','rb').read()
o=open('analysis/startup_audit/original_post_data.bin','rb').read()
fb=set(json.load(open('analysis/startup_audit/noise_floor_original.json'))['volatile_offsets'])
fc=set(json.load(open('analysis/startup_audit/noise_floor_candidate.json'))['volatile_offsets'])
d1={i for i in range(len(a)) if a[i]!=o[i]}
d2={i for i in range(len(b)) if b[i]!=o[i]}
noise={i for i in range(len(a)) if a[i]!=b[i]}
mask=fb|fc|noise
S=(d1|d2)-mask
print('d1',len(d1),'d2',len(d2),'noise',len(noise),'stable S',len(S),'d1 only',len(d1-d2),'d2 only',len(d2-d1))
print('d1-S masked',len(d1-mask),'d2 masked',len(d2-mask))
J2=(0x23CC700-0x217F000,9436); J1=(0x26AF000-0x217F000,4096)
def part(name,off,n):
    s={i for i in S if off<=i<off+n}
    print(name,'stable',len(s),'cand0 oracle!=0',sum(1 for i in s if a[i]==0),'both nz',sum(1 for i in s if a[i] and o[i]))
part('janela2',*J2); part('janela1',*J1)
rest={i for i in S if not(J2[0]<=i<J2[0]+J2[1] or J1[0]<=i<J1[0]+J1[1])}
print('rest stable',len(rest),'cand0',sum(1 for i in rest if a[i]==0))
# cluster stable divergence into ranges
srt=sorted(S); ranges=[]; st=pr=srt[0]
for x in srt[1:]:
    if x==pr+1: pr=x
    else: ranges.append((st,pr)); st=pr=x
ranges.append((st,pr))
print('ranges',len(ranges),'largest:')
for s,e in sorted(ranges,key=lambda r:r[1]-r[0],reverse=True)[:8]:
    print(' ',hex(s),hex(e),e-s+1)
# noise ranges
srt=sorted(noise); nr=[]; st=pr=srt[0]
for x in srt[1:]:
    if x==pr+1: pr=x
    else: nr.append((st,pr)); st=pr=x
nr.append((st,pr))
print('noise ranges',len(nr),'largest:')
for s,e in sorted(nr,key=lambda r:r[1]-r[0],reverse=True)[:8]:
    print(' ',hex(s),hex(e),e-s+1)
