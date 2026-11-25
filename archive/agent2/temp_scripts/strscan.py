import re, sys
from pathlib import Path

p = Path(sys.argv[1])
d = p.read_bytes()

def asc_strings():
    for m in re.finditer(rb'[\x20-\x7e]{4,}', d):
        s = m.group().decode('ascii', 'ignore')
        yield m.start(), s

def utf16_strings():
    for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', d):
        s = m.group().decode('utf-16-le', 'ignore')
        yield m.start(), s

terms = [t.lower() for t in sys.argv[2:]] or ['pipe']
seen = set()
for gen, kind in ((asc_strings, 'a'), (utf16_strings, 'w')):
    for off, s in gen():
        ls = s.lower()
        if any(t in ls for t in terms):
            key = (kind, s)
            if key in seen:
                continue
            seen.add(key)
            print(f"{kind} {off:#010x}  {s[:200]}")
