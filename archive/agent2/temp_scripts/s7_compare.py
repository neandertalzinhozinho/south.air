import json, numpy as np
from PIL import Image
from pathlib import Path

D = Path(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1\s7_gui')
REF = Path(r'D:\PROJETOS\shadowFILES\analysis\host_reference\reference_editor.png')

def arr(p):
    return np.array(Image.open(p))[:, :, :3]

ref = arr(REF)
h, w = ref.shape[:2]
c1 = arr(D / 'wrapperstub_c1_screen.bmp')[:, :w]
c2 = arr(D / 'wrapperstub_c2_screen.bmp')[:, :w]
print('ref', ref.shape, 'c1', c1.shape)

def diff(a, b):
    d = np.abs(a.astype(np.int64) - b.astype(np.int64))
    any_ = np.any(d > 0, axis=2)
    return int(any_.sum()), int(d.sum())

print('c1 vs ref :', diff(c1, ref))
print('c2 vs ref :', diff(c2, ref))
print('c1 vs c2  :', diff(c1, c2))

regions = {
    'header_presets': (slice(6, 33), slice(226, 1043)),
    'parameter_labels': (slice(152, 559), slice(22, 181)),
    'band_tabs': (slice(550, 621), slice(0, 1049)),
    'central_dsp': (slice(50, 551), slice(210, 1049)),
}
d = np.abs(c1.astype(np.int64) - ref.astype(np.int64))
for name, (ys, xs) in regions.items():
    sub = d[ys, xs]
    print(f'{name:18s} px_diff={int(np.any(sub>0,axis=2).sum()):6d}  sum={int(sub.sum()):9d}  region_px={sub.shape[0]*sub.shape[1]}')

ys, xs = np.where(np.any(d > 0, axis=2))
print('bbox', xs.min(), ys.min(), xs.max(), ys.max())
Image.fromarray(c1).save(D / 'wrapperstub_editor_capture.png')
