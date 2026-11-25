p = r'D:\PROJETOS\shadowFILES\analysis\tools\s6_dsp_probe\src\main.rs'
s = open(p, encoding='utf-8').read()
lines = s.split('\n')
# lines are 0-based; convert target region lines 186..209 (1-based) into a single block
head = lines[:185]           # up to line 185
region = lines[185:209]      # lines 186..209
assert region[0].strip() == 'if mode == "latency" {', region[0]
assert region[14].strip() == 'if mode == "latency" {', region[14]
assert region[13].strip() == '}', region[13]
new_region = []
for i, ln in enumerate(region):
    if i in (13, 14):
        continue
    new_region.append(ln)
new_region.append('    }')
out = '\n'.join(head + new_region + lines[209:])
open(p, 'w', encoding='utf-8', newline='').write(out)
print('\n'.join(new_region))
