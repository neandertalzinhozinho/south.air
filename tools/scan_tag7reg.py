import re

d = open(r'dumpsooth/nyx_soothe3_dump.bin', 'rb').read()
pat = re.compile(rb'[\xb8-\xbf]\x07\x00\x00\x00')
hits = [m.start() for m in pat.finditer(d)]
print('mov reg,7 count', len(hits))
for h in hits[:60]:
    print(hex(h), d[h:h + 24].hex(' '))
