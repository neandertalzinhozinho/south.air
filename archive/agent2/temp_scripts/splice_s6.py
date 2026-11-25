p = r'D:\PROJETOS\shadowFILES\analysis\tools\s6_dsp_probe\src\main.rs'
s = open(p, encoding='utf-8').read()
new = open(r'C:\Users\tromb\AppData\Local\Temp\opencode\s6_multi_block.rs', encoding='utf-8').read()
needle = '    if mode == "multi" {'
start = s.index(needle)
endmark = '    }\n}\n'
end = s.index(endmark, start)
old = s[start:end + len('    }\n')]
print('old block chars:', len(old))
s2 = s[:start] + new + s[end + len('    }\n'):]
open(p, 'w', encoding='utf-8', newline='').write(s2)
print('new file chars:', len(s2))
