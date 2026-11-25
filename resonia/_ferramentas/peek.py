import json,sys
f=sys.argv[1]; types=sys.argv[2].split(',')
n=int(sys.argv[3]) if len(sys.argv)>3 else 2
seen={}
for line in open(f,encoding='utf-8'):
    o=json.loads(line); t=o.get('type')
    if t=='response_item': t='ri:'+o['payload'].get('type')
    if t in types and seen.get(t,0)<n:
        seen[t]=seen.get(t,0)+1
        s=json.dumps(o,ensure_ascii=False); print(t,len(s)); print(s[:1500]); print('=====')
