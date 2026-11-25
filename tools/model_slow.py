import struct, sys

def load_secs(p):
    secs = {}; cur = None
    for line in open(p):
        line = line.rstrip()
        if line.startswith('#'): continue
        if len(line) >= 8 and all(c in '0123456789abcdef' for c in line.lower()):
            secs[cur].append(int(line, 16))
        elif line:
            cur = line; secs[cur] = []
    return secs

def f(b): return struct.unpack('<f', struct.pack('<I', b))[0]
def bits(x): return struct.unpack('<I', struct.pack('<f', x))[0]

MASK = [0x80000000 ^ bits(0.0) if i % 2 == 0 else 0 for i in range(8)]
# xor MASK: flip sign bit on even lanes
def xor_mask(v):
    r = []
    for i, x in enumerate(v):
        r.append(f(bits(x) ^ MASK[i]) if i % 2 == 0 else x)
    return r

def shuf(a, b, imm):
    s = [(imm >> 0) & 3, (imm >> 2) & 3, (imm >> 4) & 3, (imm >> 6) & 3]
    r = [0.0] * 8
    for lane in range(2):
        base = lane * 4
        r[base + 0] = a[base + s[0]]
        r[base + 1] = a[base + s[1]]
        r[base + 2] = b[base + s[2]]
        r[base + 3] = b[base + s[3]]
    return r

def add(a, b): return [x + y for x, y in zip(a, b)]
def sub(a, b): return [x - y for x, y in zip(a, b)]
def mul(a, b): return [x * y for x, y in zip(a, b)]
def addsub(a, b): return [a[i] - b[i] if i % 2 == 0 else a[i] + b[i] for i in range(8)]
def fma213(dst, s2, s3): return [s2[i] * dst[i] + s3[i] for i in range(8)]
def fma231(dst, a, b): return [a[i] * b[i] + dst[i] for i in range(8)]
def fmaaddsub231(dst, s1, s2): return addsub(mul(s1, s2), dst)
def fmaaddsub213(dst, s1, s2): return addsub(mul(s1, dst), s2)

if __name__ == '__main__':
    g = load_secs(r'D:\PROJETOS\soultree\checks\.build\split19.bits')
    src = [f(b) for b in g['SRC']]
    out = [f(b) for b in g['OUT']]
    tw = [f(b) for b in g['TW50']]
    n = len(out) - 2
    length = n // 2
    low = 1
    high = length - 8
    half = [0.5] * 8

    def pair(d, p): return [d[2 * p], d[2 * p + 1]]
    def quad(d, i): return d[i:i + 4]

    a2 = pair(src, low + 1); a1 = pair(src, low)
    xmm7 = a2 + a1
    h6 = quad(src, 2 * (high + 6))
    a4 = pair(src, low + 3); a3 = pair(src, low + 2)
    xmm2 = a4 + a3
    y4 = xmm7 + xmm2
    h4 = quad(src, 2 * (high + 4))
    y7i = h6 + h4
    t = mul(half, y7i)
    y8 = fmaaddsub213(half, y4, t)
    y7 = fma231(xor_mask(t), y4, half)
    tw0 = quad(tw, 0); tw1 = quad(tw, 4)
    y3 = tw0 + tw1
    y2 = shuf(y3, y3, 0xb1)
    y5 = [1.0] * 8   # cos block 0
    y6 = [-0.0] * 8  # sin block 0
    y4b = fmaaddsub231(mul(y6, y2), y3, y5)
    y2b = shuf(y4b, y4b, 0xa0)
    y3b = shuf(y4b, y4b, 0xf5)
    y4c = mul(xor_mask(y2b), shuf(y8, y8, 0xb1))
    y8t = fma213(y8, y3b, y4c)
    y2d = add(y7, y8t)
    y7c = addsub(xor_mask(y7), y8t)

    # stores: low+1<-y2d[0:2], low<-y2d[2:4], low+3<-y2d[4:6], low+2<-y2d[6:8]
    got = {}
    got[low + 1] = y2d[0:2]
    got[low] = y2d[2:4]
    got[low + 3] = y2d[4:6]
    got[low + 2] = y2d[6:8]
    print('LOW first half (my model vs OUT):')
    for p in [1, 2, 3, 4]:
        w = pair(out, p)
        g_ = got[p]
        print('pair %d model % .9e % .9e  want % .9e % .9e' % (p, g_[0], g_[1], w[0], w[1]))
    # high stores
    gotH = {}
    gotH[high + 4] = y7c[4:6]
    gotH[high + 5] = y7c[6:8]
    gotH[high + 6] = y7c[0:2]
    gotH[high + 7] = y7c[2:4]
    print('HIGH first half:')
    for p in [high + 4, high + 5, high + 6, high + 7]:
        w = pair(out, p)
        g_ = gotH[p]
        print('pair %d model % .9e % .9e  want % .9e % .9e' % (p, g_[0], g_[1], w[0], w[1]))
