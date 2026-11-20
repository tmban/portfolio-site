import re, os
pages=['kova/index.html','verde/verde.html','arbor/arbor.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html','index.html','about.html']
refs={}
for p in pages:
    s=open(p,encoding='utf-8').read()
    base=os.path.dirname(p)
    for m in re.finditer(r'(?:src|href)="([^"]+\.png)"', s):
        raw=m.group(1); rp=raw.split('?')[0]
        if rp.startswith('/'):
            tgt=rp.lstrip('/')
        else:
            tgt=os.path.normpath(os.path.join(base, rp)).replace(os.sep,'/')
        refs.setdefault(tgt,set()).add((p,raw))
rows=[]
for tgt,uses in refs.items():
    sz=os.path.getsize(tgt) if os.path.exists(tgt) else 0
    rows.append((sz,tgt,len(uses)))
rows.sort(reverse=True)
big=[r for r in rows if r[0]>200*1024]
print("PNG content images referenced: %d | >200KB: %d | total %.1fMB"%(len(rows),len(big),sum(r[0] for r in rows)/1024/1024))
for sz,t,n in rows:
    flag='  <-- convert' if sz>200*1024 else ''
    print("%7.0fKB  x%d  %s%s"%(sz/1024,n,t,flag))
