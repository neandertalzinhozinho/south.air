import json
p = r'D:\PROJETOS\shadowFILES\analysis\recovered_native\dsp\dependency_build.json'
d = json.load(open(p, encoding='utf-8'))
def h(x): return int(x,16) if isinstance(x,str) else int(x)
targets = [(0x71360,0x713eb),(0x6f360,0x6f660),(0x715c0,0x71864),(0x24140b,0x2414b0),(0x71400,0x715bc)]
for lo,hi in targets:
    print(f'\n=== overlaps with 0x{lo:x}..0x{hi:x} ===')
    for rec in d:
        a,b = h(rec['start']), h(rec['end'])
        if a < hi and b > lo:
            print(f"  0x{a:x}..0x{b:x} ({b-a:5d}B) {rec.get('assembler_output','')} status={rec.get('status')} pin={rec.get('pinned')}")
