"""Referências a um RVA no dump: ponteiro absoluto (VA base 0x199B0000 ou
0x180000000) e lea/mov RIP-relativo. Só leitura. Uso: py -I tools/find_refs_va.py 0x861DB0"""
import re, struct, sys
d = open(r'dumpsooth/nyx_soothe3_dump.bin', 'rb').read()
for t in (int(a, 16) for a in sys.argv[1:]):
    res = []
    for base in (0x199B0000, 0x180000000):
        for m in re.finditer(re.escape(struct.pack('<Q', base + t)), d):
            res.append(f'ptr64@{m.start():#x}')
    for m in re.finditer(rb'[\x48\x4c]\x8d[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]', d[0x1000:0x1C00000]):
        a = 0x1000 + m.start()
        if a + 7 + struct.unpack_from('<i', d, a + 3)[0] == t:
            res.append(f'lea@{a:#x}')
    print(hex(t), res[:20])
