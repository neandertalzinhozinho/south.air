import math, struct, wave, os, random
out = r'D:\PROJETOS\soultree\checks\audio'
os.makedirs(out, exist_ok=True)
SR = 48000
DUR = 3.0
N = int(SR*DUR)

def write(name, chans):
    p = os.path.join(out, name)
    with wave.open(p, 'wb') as w:
        w.setnchannels(len(chans)); w.setsampwidth(2); w.setframerate(SR)
        frames = bytearray()
        for i in range(len(chans[0])):
            for c in chans:
                v = max(-1.0, min(1.0, c[i]))
                frames += struct.pack('<h', int(v*32767))
        w.writeframes(bytes(frames))
    print('wrote', p, len(chans[0]), 'frames', len(chans), 'ch')

# 1. impulse
imp = [0.0]*N
imp[100] = 0.9
write('impulse.wav', [imp, list(imp)])

# 2. log sine sweep 20 Hz -> 20 kHz
def sweep():
    x = [0.0]*N
    f0, f1 = 20.0, 20000.0
    T = DUR
    k = math.log(f1/f0)
    for i in range(N):
        t = i/SR
        phase = 2*math.pi*f0*T/k*(math.exp(k*t/T)-1)
        x[i] = 0.5*math.sin(phase)
    return x
sw = sweep()
write('sweep.wav', [sw, list(sw)])

# 3. pink-ish noise + resonant sines at 100/1k/5k/12k
random.seed(7)
noise = [random.uniform(-1,1)*0.05 for _ in range(N)]
# simple pink filter
pink = [0.0]*N
b0=b1=b2=b3=b4=b5=b6=0.0
for i in range(N):
    w = noise[i]
    b0 = 0.99886*b0 + w*0.0555179
    b1 = 0.99332*b1 + w*0.0750759
    b2 = 0.96900*b2 + w*0.1538520
    b3 = 0.86650*b3 + w*0.3104856
    b4 = 0.55000*b4 + w*0.5329522
    b5 = -0.7616*b5 - w*0.0168980
    pink[i] = (b0+b1+b2+b3+b4+b5+b6+w*0.5362)*0.11
    b6 = w*0.115926
for f in (100.0, 1000.0, 5000.0, 12000.0):
    for i in range(N):
        pink[i] += 0.12*math.sin(2*math.pi*f*i/SR)
write('resonances.wav', [pink, list(pink)])

# 4. mono
write('resonances_mono.wav', [pink])

# 5. stereo phase / side signal
side = [0.0]*N
for i in range(N):
    side[i] = 0.4*math.sin(2*math.pi*3000*i/SR)
l = [pink[i]*0.8 + side[i] for i in range(N)]
r = [pink[i]*0.8 - side[i] for i in range(N)]
write('stereo_side.wav', [l, r])
