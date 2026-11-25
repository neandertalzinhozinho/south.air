import json, hashlib, struct
import numpy as np
from pathlib import Path
import pefile

ROOT = Path(r'D:\PROJETOS\shadowFILES')
PA = ROOT / 'analysis/host_reference/startup_capture/original_before_load.vst3'
PB = ROOT / 'analysis/startup_audit/final_candidate_wrapperstub.vst3'

print('=== secoes (RVA range) ===')
for tag, p in (('A', PA), ('B', PB)):
    pe = pefile.PE(str(p), fast_load=True)
    print(f'-- {tag}  ImageBase=0x{pe.OPTIONAL_HEADER.ImageBase:X}  nsec={pe.FILE_HEADER.NumberOfSections}')
    for s in pe.sections:
        nm = s.Name.rstrip(b'\0').decode('latin1')
        lo = pe.OPTIONAL_HEADER.ImageBase + s.VirtualAddress
        hi = lo + max(s.Misc_VirtualSize, s.SizeOfRawData)
        hit = ' <== 0x1a6e220' if lo <= 0x180000000 + 0x1a6e220 < hi else ''
        hit2 = ' <== 0x1a292d0' if lo <= 0x180000000 + 0x1a292d0 < hi else ''
        print(f'   {nm:<10} RVA 0x{s.VirtualAddress:08X}  size 0x{max(s.Misc_VirtualSize,s.SizeOfRawData):08X}{hit}{hit2}')
    pe.close()

print('\n=== hipotese: hash do caminho do modulo ===')
for tag, p in (('A', PA), ('B', PB)):
    for s in (str(p), str(p).lower(), p.name, str(p).replace('\\', '/')):
        b = s.encode('utf-8')
        print(f'  {tag} {s[-46:]:<46} md5={hashlib.md5(b).hexdigest()[:16]} sha1={hashlib.sha1(b).hexdigest()[:16]}')

print('\n=== contexto das ilhas de entropia ===')
C = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase0\captures')
Ad = np.fromfile(C / 'A_r1_data.bin', dtype=np.uint8)
Bd = np.fromfile(C / 'B_r1_data.bin', dtype=np.uint8)
for o in (0x5522F0, 0x576B20, 0x578970, 0x589370):
    print(f'\n--- +0x{o:07X} ---')
    for k in range(0, 64, 16):
        print(f'  A 0x{o+k:07X} {Ad[o+k:o+k+16].tobytes().hex()}')
    for k in range(0, 64, 16):
        print(f'  B 0x{o+k:07X} {Bd[o+k:o+k+16].tobytes().hex()}')
