import json,sys
f=sys.argv[1]
for line in open(f,encoding='utf-8'):
    o=json.loads(line); t=o.get('type')
    if t in('user','queue-operation','last-prompt','system','mode','cost-state'):
        ts=o.get('timestamp')
        if t=='user':
            c=o['message'].get('content')
            if isinstance(c,str): txt=c
            else: txt=' '.join(b.get('text','') for b in c if isinstance(b,dict) and b.get('type')=='text')
            if not txt: continue
            print(ts,'USER',o.get('isCompactSummary'),txt[:300].replace('\n','\n'))
        elif t=='queue-operation': print(ts,'QUEUE',o.get('operation'),str(o.get('content'))[:200].replace('\n','\n'))
        elif t=='system': print(ts,'SYSTEM',o.get('subtype'),str(o.get('content'))[:200])
        elif t=='last-prompt': pass
        else: print(ts,t,json.dumps(o)[:200])
