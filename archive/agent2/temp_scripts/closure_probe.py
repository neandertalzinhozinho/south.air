import json
p = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\dsp\dependency_build.json'
d = json.load(open(p, encoding='utf-8'))
print('type', type(d), 'len', len(d))
print('sample keys:', list(d[0].keys()))
for rec in d:
    s = str(rec.get('start',''))
    if s.lower() in ('0x71360','0x715c0','0x71400','0x6f360','0x72180','0x24140b','0x6f45e','0x71380'):
        print('\n===', s, '===')
        print(json.dumps(rec, indent=1)[:4000])
