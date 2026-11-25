import json
import re
from pathlib import Path

t = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
for i in range(1, 4):
    lines = [l for l in (t / f'c3_patch12_veh_{i}.txt').read_text(errors='replace').splitlines()
             if l.startswith('MICRO_AV')]
    meta = json.loads((t / f'c3_patch12_veh_report_{i}.json').read_text())
    base = int(meta['base'], 16)
    last = lines[-1] if lines else ''
    fields = dict(re.findall(r'(addr|target|info0|rip|rsp|rax|rcx|rdx|r9|r12|r14)=0x([0-9a-f]+)', last))
    offs = {}
    for k in ('addr', 'rip'):
        if k in fields:
            v = int(fields[k], 16)
            offs[k] = hex(v - base) if base <= v < base + 0x1300000 else 'out_of_dll'
    print(f'run {i}: AVs={len(lines)} callbacks={(t / f"c3_patch12_count_{i}.txt").read_text()}')
    print(' ', last.split(' stack=')[0])
    print(' ', 'offsets', offs)
