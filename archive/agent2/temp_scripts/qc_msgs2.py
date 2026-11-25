import sqlite3, json, sys, io
db = r'C:\Users\tromb\.local\share\opencode\opencode.db'
c = sqlite3.connect('file:' + db.replace('\\','/') + '?mode=ro', uri=True)
c.row_factory = sqlite3.Row
sid = sys.argv[1]
outpath = sys.argv[2]
f = io.open(outpath, 'w', encoding='utf-8', errors='replace')
rows = list(c.execute("select id,type,seq,time_created,data from session_message where session_id=? order by seq", (sid,)))
f.write("MESSAGES %d\n" % len(rows))
for r in rows:
    try: obj = json.loads(r['data'])
    except Exception: obj = {'raw': str(r['data'])[:2000]}
    if r['type'] not in ('user','assistant'): continue
    def parts(o):
        out=[]
        if isinstance(o, dict):
            for k in ('text','reasoning','content','parts','body'):
                if k in o: out += parts(o[k])
        elif isinstance(o, list):
            for x in o: out += parts(x)
        elif isinstance(o, str): out.append(o)
        return out
    txt = '\n'.join(parts(obj))
    f.write('==== %s seq=%s len=%d ====\n%s\n' % (r['type'], r['seq'], len(txt), txt))
f.close()
print('wrote', outpath)
