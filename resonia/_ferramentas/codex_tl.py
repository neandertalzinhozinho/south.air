import json,sys,glob,os
base=r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao\codex"
out=open(sys.argv[1],'w',encoding='utf-8')
for f in sorted(glob.glob(base+r"\*.jsonl")):
    calls={}; outs={}
    meta=None
    msgs=[]
    for line in open(f,encoding='utf-8'):
        o=json.loads(line); t=o.get('type'); p=o.get('payload',{})
        if t=='session_meta': meta=(p.get('timestamp'),p.get('cwd'))
        if t=='response_item':
            pt=p.get('type')
            if pt in('custom_tool_call','function_call'): calls[p.get('call_id')]=(o['timestamp'],p.get('name'),p.get('input') or p.get('arguments'))
            if pt in('custom_tool_call_output','function_call_output'): outs[p.get('call_id')]=p.get('output')
            if pt=='message' and p.get('role')=='user':
                txt=' '.join(c.get('text','') for c in p.get('content',[]) if isinstance(c,dict))
                msgs.append((o['timestamp'],txt))
    print('#####',os.path.basename(f),meta,file=out)
    for ts,m in msgs: print('  USERMSG',ts,m[-600:].replace('\n','\n'),file=out)
    for k,(ts,n,i) in calls.items():
        o=outs.get(k); o=str(o)
        print(f"{ts} {n} | {str(i)[:700]!r} || {o[:300]!r}",file=out)
