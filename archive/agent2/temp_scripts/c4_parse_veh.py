import re, json, struct, sys
from pathlib import Path
TMP = Path(r'C:\Users\tromb\AppData\Local\Temp\opencode')
run = sys.argv[1] if len(sys.argv) > 1 else '1'
rep = json.loads((TMP / f'c3_patch12_veh_report_{run}.json').read_text())
BASE = int(rep['base'], 16)
log = (TMP / f'c3_patch12_veh_{run}.txt').read_text(errors='replace')
mods = {}
for line in log.splitlines():
    m = re.match(r'MOD (\d+) base=(0x[0-9a-f]+) size=(0x[0-9a-f]+) \'(.*)\'', line)
    if m:
        mods[int(m.group(1))] = (int(m.group(2),16), int(m.group(3),16), m.group(4))
line = next(l for l in log.splitlines() if l.startswith('MICRO_AV'))
vals = dict(re.findall(r'(\w+)=(0x[0-9a-f]+)', line))
hexstr = re.search(r'stack=([0-9a-f]+)', line).group(1)
stack = bytes.fromhex(hexstr)
print('BASE', hex(BASE), 'regs', {k:v for k,v in vals.items() if k!='stack'})
print('MODS of interest:')
for i,(b,s,n) in sorted(mods.items()):
    if 'python' in n.lower() or 'vcruntime' in n.lower() or 'capture' in n.lower() or 'ntdll' in n.lower():
        print(' ',i,hex(b),hex(s),n)

def where(v):
    for i,(b,s,n) in sorted(mods.items()):
        if b <= v < b+s:
            return n.split('\\')[-1] + '+' + hex(v-b)
    return '-'
print('\nstack qwords (rsp=0x%x):' % int(vals['rsp'],16))
for i in range(0, 0x120, 8):
    v = struct.unpack_from('<Q', stack, i)[0]
    w = where(v)
    tag = ''
    if 'recovered' in w.lower() or '+' in w:
        tag = ' <== ' + w
    print('  +0x%03x 0x%016x %s%s' % (i, v, w, tag))
