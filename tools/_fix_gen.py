import pathlib

p = pathlib.Path("tools/gen_fft_golden.py")
t = p.read_text(encoding="utf-8")
t = t.replace('out.append("//!', 'out.append("//')
p.write_text(t, encoding="utf-8")
print("ok")
