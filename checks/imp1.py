data=open("dumpsooth/nyx_soothe3_dump.bin","rb").read()
import re
for pat in (b"ucrtbase", b"api-ms-win-crt-math", b"powf", b"pow\x00", b"libm", b"VCRUNTIME"):
    idx=[m.start() for m in re.finditer(re.escape(pat), data)][:5]
    print(pat, [hex(i) for i in idx])
