import pathlib

p = pathlib.Path('checks/j4_fft.rs')
t = p.read_text(encoding='utf-8')
t = t.replace('include!("j4_stage_golden.rs");\ninclude!("fft_golden.rs");',
              'include!("j4_golden_6.rs");\ninclude!("j4_golden_7.rs");\ninclude!("fft_golden.rs");')
t = t.replace('J4_', 'J6_')
p.write_text(t, encoding='utf-8')
print('ok', t.count('J6_'))
