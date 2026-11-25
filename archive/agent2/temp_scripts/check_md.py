import sys
p = r'D:\PROJETOS\shadowFILES\continuidade.md'
lines = open(p, encoding='utf-8').read().splitlines()
keys = ['Causa raiz provável', 'hipótese única', 'PACE-free (oráculo)', 'Rev. 12 —', 'Rev. 13 —', 'Fase 0/1 aprovada']
for i, l in enumerate(lines, 1):
    if any(k in l for k in keys):
        print(i, l[:110])
print('total', len(lines))
