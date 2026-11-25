import sqlite3, json, sys
db = r'C:\Users\tromb\.local\share\opencode\opencode.db'
c = sqlite3.connect('file:' + db.replace('\\','/') + '?mode=ro', uri=True)
c.row_factory = sqlite3.Row
sid = sys.argv[1]
rows = list(c.execute("select id,type,seq,time_created,data from session_message where session_id=? order by seq", (sid,)))
print("MESSAGES", len(rows))
for r in rows:
    d = r['data']
    try:
        obj = json.loads(d)
    except Exception:
        obj = {'raw': d[:2000]}
    typ = r['type']
    if typ in ('user','assistant'):
        # extract text
        def parts(o):
            out=[]
            if isinstance(o, dict):
                for k in ('text','reasoning','content','parts','body'):
                    if k in o: out += parts(o[k])
            elif isinstance(o, list):
                for x in o: out += parts(x)
            elif isinstance(o, str):
                out.append(o)
            return out
        txt = '\n'.join(parts(obj))
        print('----', typ, r['seq'], 'len', len(txt))
        print(txt[:12000])
