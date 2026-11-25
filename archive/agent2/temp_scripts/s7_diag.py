import numpy as np
from PIL import Image
from pathlib import Path

D = Path(r'D:\PROJETOS\shadowFILES')
new = np.array(Image.open(D/'analysis/stage_reports/fase1/s7_gui/wrapperstub_c1_screen.bmp'))[:, :1049, :3]
ref = np.array(Image.open(D/'analysis/host_reference/reference_editor.png'))[:, :, :3]
uni = np.array(Image.open(D/'analysis/startup_audit/uni45_editor_capture.png'))[:, :1049, :3]
str7 = np.array(Image.open(D/'analysis/startup_audit/str7_editor_capture.png'))[:, :1049, :3]

def cmp(a, b, name):
    d = np.abs(a.astype(np.int64)-b.astype(np.int64))
    any_ = np.any(d>0, axis=2)
    print(f'{name:22s} px={int(any_.sum()):6d} sum={int(d.sum()):9d}')
    return d

cmp(new, ref, 'wrapperstub vs ref')
cmp(new, uni, 'wrapperstub vs uni45')
cmp(uni, ref, 'uni45 vs ref')
cmp(str7, ref, 'str7 vs ref')

d = np.abs(new.astype(np.int64)-ref.astype(np.int64)).sum(2)
hm = np.clip(d*8, 0, 255).astype(np.uint8)
Image.fromarray(hm).save(D/'analysis/stage_reports/fase1/s7_gui/diff_heat_wrapperstub_vs_ref.png')

# column / row profile of the diff
col = (d>0).sum(0); row = (d>0).sum(1)
top_cols = [(int(i), int(col[i])) for i in np.argsort(col)[-8:]]
top_rows = [(int(i), int(row[i])) for i in np.argsort(row)[-8:]]
print('busiest cols', sorted(top_cols))
print('busiest rows', sorted(top_rows))

# mean colour of the diff area inside the central canvas
ys, xs = np.where(d>0)
print('diff bbox', xs.min(), ys.min(), xs.max(), ys.max())
sub = d[d>0]
print('mean |delta| on diff px', sub.mean())
