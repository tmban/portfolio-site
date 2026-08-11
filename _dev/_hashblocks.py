import re, hashlib
pages=['index.html','about.html','kova/index.html','verde/verde.html','arbor/arbor.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html']
def block(s, tag, idv):
    m=re.search(r'<'+tag+r' id="'+idv+r'">(.*?)</'+tag+r'>', s, re.S)
    return m.group(1) if m else None
for idv,tag in [('topnav-css','style'),('topnav-js','script')]:
    hashes={}
    for p in pages:
        s=open(p,encoding='utf-8').read()
        b=block(s,tag,idv)
        h=hashlib.md5(b.encode()).hexdigest()[:10] if b is not None else 'MISSING'
        hashes.setdefault(h,[]).append(p)
    print(idv, '->', 'IDENTICAL across all' if len(hashes)==1 else 'DIFFERS')
    for h,ps in hashes.items(): print('   ',h, len(ps),'pages')
# fira-override (marker-wrapped)
hashes={}
for p in pages:
    s=open(p,encoding='utf-8').read()
    m=re.search(r'<style id="fira-override">(.*?)</style>', s, re.S)
    h=hashlib.md5(m.group(1).encode()).hexdigest()[:10] if m else 'MISSING'
    hashes.setdefault(h,[]).append(p)
print('fira-override ->', 'IDENTICAL' if len(hashes)==1 else 'DIFFERS')
for h,ps in hashes.items(): print('   ',h,len(ps),[x.split('/')[0] for x in ps])
