import json, io
rows = []
for line in open(r'D:\PROJETOS\shadowFILES\analysis\stage_reports\fase1\s5_params_wrapperstub.jsonl', encoding='utf-8'):
    d = json.loads(line)
    if 'index' in d and 'title' in d:
        rows.append(d)
print('param rows:', len(rows))
for r in rows:
    if r.get('index') in (14, 16, 114, 115, 127, 128, 129, 130, 131, 132):
        print(json.dumps(r)[:320])
