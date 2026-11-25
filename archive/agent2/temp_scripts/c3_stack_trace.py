import json
import re
from pathlib import Path

t = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
for i in (1, 2, 3):
    line = [l for l in (t / f'c3_patch12_veh_{i}.txt').read_text(errors='replace').splitlines()
            if l.startswith('MICRO_AV')][-1]
    meta = json.loads((t / f'c3_patch12_veh_report_{i}.json').read_text())
    base = int(meta['base'], 16)
    stack_hex = line.split(' stack=')[1]
    qwords = [int(stack_hex[j:j+16], 16) for j in range(0, min(len(stack_hex), 0x400), 16)]
    print(f'--- run {i} base={base:#x} ---')
    for n, q in enumerate(qwords[:48]):
        tag = ''
        if base <= q < base + 0x1300000:
            tag = f'DLL+{q-base:#x}'
        elif q:
            tag = 'other'
        print(f'  +{n*8:04x}: {q:#018x} {tag}')
