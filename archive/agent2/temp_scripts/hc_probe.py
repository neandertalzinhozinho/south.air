import ctypes
import os
from pathlib import Path

ROOT = Path('D:/PROJETOS/shadowFILES').resolve()
dll = ROOT / 'soultea3_plugin/build/Release/hostcheck_dll.dll'
vst = ROOT / 'soultea3_plugin/build/soultea3_clone_artefacts/Release/VST3/soultea3.vst3'

lib = ctypes.CDLL(str(dll))
lib.hc_run.restype = ctypes.c_int
lib.hc_run.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
buf = ctypes.create_string_buffer(1 << 20)
os.environ['HC_DEPTH'] = '5.0'
rc = lib.hc_run(str(vst.relative_to(ROOT)).replace('\\', '/').encode('ascii'), buf, len(buf))
print('rc', rc)
text = buf.value.decode('utf-8', errors='replace')
for line in text.splitlines():
    if line.strip().startswith('{'):
        print(line[:300])
