import re, os
from PIL import Image
pages=['kova/index.html','verde/verde.html','arbor/arbor.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html','index.html','about.html']
SKIP={'finning/assets/photos/excavator.png','apple-touch-icon.png'}
MINKB=120
# collect refs: resolved path -> list of (page, raw)
refs={}
for p in pages:
    s=open(p,encoding='utf-8').read(); base=os.path.dirname(p)
    for m in re.finditer(r'(?:src|href)="([^"]+\.png)"', s):
        raw=m.group(1); rp=raw.split('?')[0]
        tgt=(rp.lstrip('/') if rp.startswith('/') else os.path.normpath(os.path.join(base, rp)).replace(os.sep,'/'))
        refs.setdefault(tgt,[]).append((p,raw))

saved=0; conv=[]
for tgt,uses in refs.items():
    if tgt in SKIP or not os.path.exists(tgt): continue
    if os.path.getsize(tgt) < MINKB*1024: continue
    before=os.path.getsize(tgt)
    im=Image.open(tgt)
    if im.mode in ('P','RGBA','LA'): im=im.convert('RGBA')
    else: im=im.convert('RGB')
    w,h=im.size
    if max(w,h)>1600:
        sc=1600/max(w,h); im=im.resize((round(w*sc),round(h*sc)), Image.LANCZOS)
    out=tgt[:-4]+'.webp'
    im.save(out,'WEBP',quality=82,method=6)
    after=os.path.getsize(out)
    saved+=before-after
    conv.append((tgt,out,before,after))

# update refs in pages (swap .png -> .webp for converted raws)
convset={t for t,_,_,_ in conv}
for p in pages:
    s=open(p,encoding='utf-8').read(); orig=s
    for tgt,uses in refs.items():
        if tgt in convset:
            for pg,raw in uses:
                if pg==p:
                    s=s.replace('"'+raw+'"', '"'+raw[:-4]+'.webp"')
    if s!=orig: open(p,encoding='utf-8',mode='w').write(s)

# delete originals only if no .png ref to them remains anywhere
allhtml=''.join(open(p,encoding='utf-8').read() for p in pages)
deleted=0
for tgt,out,b,a in conv:
    name=os.path.basename(tgt)
    # any page still referencing this png basename?
    if name in allhtml:
        print("KEPT (still referenced):",tgt)
    else:
        os.remove(tgt); deleted+=1

print("converted %d images | saved %.1fMB | deleted %d originals"%(len(conv),saved/1024/1024,deleted))
for t,o,b,a in conv:
    print("  %5.0fKB -> %5.0fKB  %s"%(b/1024,a/1024,os.path.basename(o)))
