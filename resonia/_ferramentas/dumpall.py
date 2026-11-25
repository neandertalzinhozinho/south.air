import json,sys,glob,os
S=r"C:\Users\tromb\AppData\Local\Temp\claude\057552d9a8e68f6d\799fb4d7-038b-4f01-878d-c892aa22d410\scratchpad\dump"
os.makedirs(S,exist_ok=True)
base=r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao"
def outtext(o):
    if isinstance(o,str):
        try: o=json.loads(o)
        except: return o
    if isinstance(o,list):
        return '\n'.join(x.get('text','') if isinstance(x,dict) else str(x) for x in o)
    if isinstance(o,dict): return o.get('output') or json.dumps(o)
    return str(o)
for f in sorted(glob.glob(base+r"\codex\*.jsonl")):
    sid=os.path.basename(f)[8:27]
    calls={}; outs={}
    for line in open(f,encoding='utf-8'):
        o=json.loads(line); p=o.get('payload',{})
        if o.get('type')=='response_item':
            pt=p.get('type')
            if pt in('custom_tool_call','function_call'): calls[p['call_id']]=(o['timestamp'],p.get('name'),p.get('input') or p.get('arguments'))
            if pt in('custom_tool_call_output','function_call_output'): outs[p['call_id']]=p.get('output')
    for k,(ts,n,i) in calls.items():
        fn=os.path.join(S,f"cx_{ts.replace(':','-')}_{n}.txt")
        with open(fn,'w',encoding='utf-8') as w:
            w.write(i+"\n\n=====OUTPUT=====\n"+outtext(outs.get(k)))
for f in sorted(glob.glob(base+r"\claude\**\*.jsonl",recursive=True)):
    uses={}; res={}
    for line in open(f,encoding='utf-8'):
        o=json.loads(line); t=o.get('type')
        if t=='assistant':
            for b in o['message'].get('content',[]):
                if isinstance(b,dict) and b.get('type')=='tool_use': uses[b['id']]=(o['timestamp'],b['name'],b['input'])
        elif t=='user' and isinstance(o['message'].get('content'),list):
            for b in o['message']['content']:
                if isinstance(b,dict) and b.get('type')=='tool_result':
                    c=b.get('content'); 
                    if isinstance(c,list): c='\n'.join(x.get('text','') for x in c if isinstance(x,dict))
                    res[b['tool_use_id']]=(b.get('is_error'),c,o.get('toolUseResult'))
    for k,(ts,n,i) in uses.items():
        n2=n.replace('mcp__craft-anything__','ca_')
        r=res.get(k,(None,'',None))
        with open(os.path.join(S,f"cl_{ts.replace(':','-')}_{n2}.txt"),'w',encoding='utf-8') as w:
            if n in('Bash','PowerShell'): w.write(i.get('command',''))
            else: w.write(json.dumps(i,ensure_ascii=False,indent=1))
            w.write(f"\n\n=====OUTPUT err={r[0]}=====\n{r[1]}")
            if r[2] is not None and n in('Bash','PowerShell','Read'): w.write("\n=====TUR=====\n"+json.dumps(r[2],ensure_ascii=False)[:200000])
print(len(os.listdir(S)))
