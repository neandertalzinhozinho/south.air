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
res=sorted({i for i in range(N) if c[0][i]!=r[0][i]}-(onoise|cnoise))
pages=collections.Counter(i>>12 for i in res)
print('pages',[(hex(k<<12),v) for k,v in pages.most_common(12)])
# diverging values (both nonzero)
div=[i for i in res if c[0][i] and r[0][i]]
print('div count',len(div))
# group contiguous div into words
def words(offs, x, y):
    out=[]
    for i in offs:
        if out and i-out[-1][1]==1: out[-1]=(out[-1][0],i)
        else: out.append((i,i))
    return out
for a,b in words(div,r[0],c[0])[:12]:
    print('div',hex(a),hex(b),'orac',r[0][a:b+1].hex(),'cand',c[0][a:b+1].hex())
print('extras',[hex(i) for i in res if c[0][i] and not r[0][i]][:30])
# janela1 residual detail
j1=[i for i in res if 0x530000<=i<0x531000]
print('janela1 residual',len(j1))
for a,b in words(j1,r[0],c[0]):
    print(' j1',hex(a),hex(b),'orac',r[0][a:b+1].hex(),'cand',c[0][a:b+1].hex())
