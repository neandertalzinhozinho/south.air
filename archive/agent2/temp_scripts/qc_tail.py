import io, sys
p = sys.argv[1]
out = sys.argv[2]
n = int(sys.argv[3])
t = io.open(p, encoding='utf-8', errors='replace').read()
io.open(out,'w',encoding='utf-8',errors='replace').write(t[-n:])
print('wrote', out, 'chars', min(n,len(t)))
