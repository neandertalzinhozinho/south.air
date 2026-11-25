import sys
from pathlib import Path

def strings_near(data, needles, span=400, max_hits=40):
    out = []
    for n in needles:
        b = n.encode('utf-16-le')
        start = 0
        hits = 0
        while hits < max_hits:
            i = data.find(b, start)
            if i < 0:
                break
            chunk = data[max(0, i - span):i + span]
            txt = chunk.decode('utf-16-le', errors='ignore')
            printable = ''.join(ch if 31 < ord(ch) < 127 or ch in '\r\n\t' else '\u00b7' for ch in txt)
            out.append((n, hex(i), printable))
            start = i + 1
            hits += 1
    return out

p = Path(sys.argv[1])
data = p.read_bytes()
for needle, off, txt in strings_near(data, sys.argv[2:], span=int(sys.argv[3]) if len(sys.argv) > 3 else 400):
    print('###', needle, off)
    print(txt.replace('\u00b7', '.'))
    print()
