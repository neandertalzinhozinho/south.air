"""Lista chamadas diretas (E8 rel32) e jmp (E9) para os RVAs dados, no .text do dump.
Uso: py -I tools/find_callers.py 0x8ACC40 [0x...]
Só leitura do dump (offset de arquivo = RVA)."""
import re, struct, sys
d = open(r'dumpsooth/nyx_soothe3_dump.bin', 'rb').read()
lo, hi = 0x1000, 0x1C00000
for t in (int(a, 16) for a in sys.argv[1:]):
    out = []
    for op in (b'\xe8', b'\xe9'):
        for m in re.finditer(re.escape(op), d[lo:hi]):
            a = lo + m.start()
            if a + 5 + struct.unpack_from('<i', d, a + 1)[0] == t:
                out.append(('call' if op == b'\xe8' else 'jmp') + ' ' + hex(a))
    print(hex(t), out)
