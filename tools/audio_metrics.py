#!/usr/bin/env python3
"""Phase 4 metrics: compare two WAVs (original oracle vs Resonia port).

Usage: py tools/audio_metrics.py <original.wav> <resonia.wav> [label]

Reports RMS of each, RMS of the difference, null-test depth (dB), peak error and
the best integer latency (cross-correlation) so a misaligned render is obvious.
Pure stdlib (wave + struct + math) so it runs anywhere.
"""
import sys, wave, struct, math


def read(path):
    """Minimal RIFF reader: PCM16, IEEE float32 and WAVE_FORMAT_EXTENSIBLE."""
    with open(path, 'rb') as f:
        data = f.read()
    if data[:4] != b'RIFF' or data[8:12] != b'WAVE':
        raise SystemExit(f'{path}: not a WAV')
    pos = 12
    fmt = None
    body = None
    while pos + 8 <= len(data):
        cid = data[pos:pos + 4]
        size = struct.unpack_from('<I', data, pos + 4)[0]
        chunk = data[pos + 8:pos + 8 + size]
        if cid == b'fmt ':
            fmt = chunk
        elif cid == b'data':
            body = chunk
        pos += 8 + size + (size & 1)
    if fmt is None or body is None:
        raise SystemExit(f'{path}: missing fmt/data chunk')
    tag = struct.unpack_from('<H', fmt, 0)[0]
    ch = struct.unpack_from('<H', fmt, 2)[0]
    sr = struct.unpack_from('<I', fmt, 4)[0]
    bits = struct.unpack_from('<H', fmt, 14)[0]
    if tag == 0xFFFE and len(fmt) >= 26:
        tag = struct.unpack_from('<H', fmt, 24)[0]  # SubFormat GUID first 2 bytes
    if tag == 3 or (tag == 0xFFFE and bits == 32):
        vals = struct.unpack('<%df' % (len(body) // 4), body)
        scale = 1.0
    elif tag == 1 and bits == 16:
        vals = struct.unpack('<%dh' % (len(body) // 2), body)
        scale = 1.0 / 32768.0
    elif tag == 1 and bits == 32:
        vals = struct.unpack('<%di' % (len(body) // 4), body)
        scale = 1.0 / 2147483648.0
    else:
        raise SystemExit(f'{path}: unsupported format tag={tag} bits={bits}')
    out = [[] for _ in range(ch)]
    for i, v in enumerate(vals):
        out[i % ch].append(v * scale)
    return out, sr


def rms(x):
    if not x:
        return 0.0
    return math.sqrt(sum(v * v for v in x) / len(x))


def db(v):
    return 20 * math.log10(v) if v > 1e-12 else -240.0


def best_lag(a, b, max_lag=8192):
    n = min(len(a), len(b))
    best, best_lag = -1.0, 0
    for lag in range(0, max_lag):
        s = 0.0
        # sparse correlation for speed
        step = max(1, n // 20000)
        m = 0
        for i in range(0, n - lag, step):
            s += a[i] * b[i + lag]
            m += 1
        if m and s > best:
            best, best_lag = s, lag
    return best_lag


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    a, sr_a = read(sys.argv[1])
    b, sr_b = read(sys.argv[2])
    label = sys.argv[3] if len(sys.argv) > 3 else ''
    if sr_a != sr_b:
        raise SystemExit(f'sample rate mismatch {sr_a} vs {sr_b}')
    ch = min(len(a), len(b))
    n = min(len(a[0]), len(b[0]))
    lag = best_lag(a[0][:n], b[0][:n])
    print(f'# {label or sys.argv[1]} vs {sys.argv[2]}  ({sr_a} Hz, {ch} ch, {n} frames)')
    print(f'latency (best lag)      : {lag} samples')
    for c in range(ch):
        x = a[c][:n]
        y = b[c][:n]
        # align
        if lag and lag < n:
            x = x[:n - lag]
            y = y[lag:]
        d = [u - v for u, v in zip(x, y)]
        r_d = rms(d)
        r_o = rms(x)
        print(f'ch{c}: original {db(r_o):7.2f} dBFS | port {db(rms(y)):7.2f} dBFS | '
              f'diff {db(r_d):7.2f} dBFS | null {db(r_d) - db(r_o):6.2f} dB')


if __name__ == '__main__':
    main()
