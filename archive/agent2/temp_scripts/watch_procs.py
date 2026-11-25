import subprocess, sys, time, os
from pathlib import Path

ROOT = Path(r"D:\PROJETOS\shadowFILES")
probe = ROOT / "analysis/scripts/fl_mixed_probe_v2.py"
target = ROOT / "analysis/startup_audit/pace_free/final_candidate_uni46c.vst3"

import ctypes
psapi = ctypes.WinDLL('psapi')
k32 = ctypes.WinDLL('kernel32')

def pids():
    snap = k32.CreateToolhelp32Snapshot(2, 0)
    buf = ctypes.create_string_buffer(600)
    out = {}
    if k32.Process32First(snap, buf):
        while True:
            pid = ctypes.c_uint32.from_buffer(buf, 8).value
            name = ctypes.c_char_p(ctypes.addressof(buf) + 44).value.decode(errors='ignore')
            out[pid] = name
            if not k32.Process32Next(snap, buf):
                break
    k32.CloseHandle(snap)
    return out

before = pids()
p = subprocess.Popen([sys.executable, str(probe), '--child', 'watch', str(target), 'V1'],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
seen = {}
t0 = time.time()
while time.time() - t0 < 25:
    now = pids()
    for pid, name in now.items():
        if pid not in before and pid not in seen:
            seen[pid] = name
            print(f"+{time.time()-t0:5.1f}s new pid={pid} {name}", flush=True)
    time.sleep(0.2)
p.kill()
print("total new:", len(seen))
