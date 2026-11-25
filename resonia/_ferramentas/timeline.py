import json,sys,glob,os
base=r"D:\PROJETOS\soultree FORK\resonia\_fontes_recuperacao\claude"
out=open(sys.argv[1],'w',encoding='utf-8')
for f in sorted(glob.glob(base+r"\**\*.jsonl",recursive=True)):
    uses={}; results={}; blobuses={}; blobres={}
    for line in open(f,encoding='utf-8'):
        o=json.loads(line); t=o.get('type')
        if t=='assistant':
            for b in o['message'].get('content',[]):
                if isinstance(b,dict) and b.get('type')=='tool_use':
                    uses[b['id']]=(o.get('timestamp'),b['name'],b['input'],o.get('isSidechain'))
        elif t=='user':
            c=o['message'].get('content')
            if isinstance(c,list):
                for b in c:
                    if isinstance(b,dict) and b.get('type')=='tool_result':
                        results[b['tool_use_id']]=(b.get('is_error'),b.get('content'),o.get('toolUseResult'))
        elif t=='api-request-blob':
            m=o.get('message',{}); c=m.get('content')
            if isinstance(c,list):
                for b in c:
                    if isinstance(b,dict) and b.get('type')=='tool_use': blobuses[b['id']]=(b['name'],b['input'])
                    if isinstance(b,dict) and b.get('type')=='tool_result': blobres[b['tool_use_id']]=b
    print(os.path.basename(f),'uses',len(uses),'results',len(results),'blobuses',len(blobuses),'blob-only',len(set(blobuses)-set(uses)),'blobres-only',len(set(blobres)-set(results)),file=out)
    for k in set(blobuses)-set(uses): print('  BLOBONLY',blobuses[k][0],json.dumps(blobuses[k][1])[:200],file=out)
    for k,(ts,name,inp,sc) in sorted(uses.items(),key=lambda x:x[1][0]):
        r=results.get(k); err=r[0] if r else 'NORESULT'
        if name in('Write','Edit','MultiEdit','Read'):
            s=f"{inp.get('file_path')} " + (f"len={len(inp.get('content',''))}" if name=='Write' else (f"old={len(inp.get('old_string',''))} new={len(inp.get('new_string',''))} all={inp.get('replace_all')}" if name=='Edit' else f"off={inp.get('offset')} lim={inp.get('limit')}"))
        elif name in('Bash','PowerShell'): s=inp.get('command','').replace('\n','\n')[:300]
        else: s=json.dumps(inp,ensure_ascii=False)[:200]
        rc=''
        if r:
            c=r[1]
            if isinstance(c,list): c=' '.join(x.get('text','') for x in c if isinstance(x,dict))
            rc=str(c).replace('\n','\n')[:150]
        print(f"{ts} {'SC' if sc else '  '} {name:10} err={err} | {s} || {rc}",file=out)
