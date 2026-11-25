"""S7 recipe bisection: which of the 101 'extra' initialisers restore the
header and parameter-label painting in final_candidate_wrapperstub.vst3.

Run:  python s7_bisect.py <mode> [args]
      python s7_bisect.py run <name> <comma-separated extra indices|all|none>
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

R = Path(r'D:\PROJETOS\shadowFILES')
PROBE = R / 'analysis/tools/s7_gui_probe/target/debug/s7_gui_probe.exe'
CAND = R / 'analysis/startup_audit/final_candidate_wrapperstub.vst3'
OUT = R / 'analysis/stage_reports/fase1/s7_gui'
REF = np.array(Image.open(R / 'analysis/host_reference/reference_editor.png'))[:, :, :3]

PLAN = json.loads((R / 'analysis/startup_audit/uni46c_build_plan.json').read_text(encoding='utf-8'))
ORDER = [int(x, 16) for x in PLAN['full_order_rvas']]
BASE = [e['rva'] for e in json.loads((R / 'analysis/startup_audit/init_order_plus_tables.json').read_text(encoding='utf-8'))]
BASE_SET = set(BASE)
EXTRAS = [r for r in ORDER if r not in BASE_SET]
REGIONS = {
    'header': (slice(6, 33), slice(226, 1043)),
    'labels': (slice(152, 559), slice(22, 181)),
    'bands': (slice(550, 621), slice(0, 1049)),
    'canvas': (slice(50, 551), slice(210, 1049)),
}


def run(name, extra_idx):
    subset = set(EXTRAS[i] for i in extra_idx)
    order = [r for r in ORDER if r in BASE_SET or r in subset]
    rec = OUT / f'{name}_recipe.json'
    rec.write_text(json.dumps([{'rva': r} for r in order], indent=1), encoding='utf-8')
    log = OUT / f'{name}.jsonl'
    with open(log, 'w', encoding='utf-8') as f:
        subprocess.run([str(PROBE), str(CAND), str(rec), 'gui', str(OUT / name)], stdout=f, stderr=subprocess.STDOUT, timeout=300)
    bmp = OUT / f'{name}_c1_screen.bmp'
    if not bmp.exists():
        return {'name': name, 'inits': len(order), 'error': 'no capture'}
    a = np.array(Image.open(bmp))[:, :1049, :3]
    d = np.abs(a.astype(int) - REF.astype(int))
    out = {'name': name, 'inits': len(order), 'extras': len(extra_idx),
           'total': int(np.any(d > 0, axis=2).sum())}
    for k, (ys, xs) in REGIONS.items():
        out[k] = int(np.any(d[ys, xs] > 0, axis=2).sum())
    out['ok'] = out['header'] == 0 and out['labels'] == 0
    return out


if __name__ == '__main__':
    args = sys.argv[1:]
    if args[0] == 'list':
        print('extras', len(EXTRAS))
        print([hex(x) for x in EXTRAS[:8]])
        sys.exit(0)
    spec = args[2]
    if spec == 'all':
        idx = list(range(len(EXTRAS)))
    elif spec == 'none':
        idx = []
    else:
        idx = [int(x) for x in spec.split(',') if x != '']
    res = run(args[1], idx)
    print(json.dumps(res))
    with open(OUT / 'bisect_log.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(res) + '\n')
