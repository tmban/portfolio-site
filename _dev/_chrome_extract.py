import re, os, hashlib
pages=['index.html','about.html','kova/index.html','verde/verde.html','arbor/arbor.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html']
def rel(p):
    d=p.count('/')
    return '../'*d
def getblock(s,tag,idv):
    return re.search(r'<'+tag+r' id="'+idv+r'">(.*?)</'+tag+r'>', s, re.S)

# --- 1. write shared files from the canonical (about.html) ---
about=open('about.html',encoding='utf-8').read()
css=getblock(about,'style','topnav-css').group(1)
js=getblock(about,'script','topnav-js').group(1)
os.makedirs('assets',exist_ok=True)
open('assets/site-nav.css','w',encoding='utf-8').write(css.strip()+'\n')
open('assets/site-nav.js','w',encoding='utf-8').write(js.strip()+'\n')
css_hash=hashlib.md5(getblock(about,'style','topnav-css').group(1).encode()).hexdigest()

# --- 2. swap in each page ---
for p in pages:
    s=open(p,encoding='utf-8').read(); orig=s
    r=rel(p)
    # JS: all pages identical -> external (defer)
    s=re.sub(r'<script id="topnav-js">.*?</script>',
             '<script id="topnav-js" src="'+r+'assets/site-nav.js" defer></script>', s, count=1, flags=re.S)
    # CSS: only swap pages whose topnav-css matches the canonical hash (the 7); leave index inline
    m=getblock(s,'style','topnav-css')
    if m and hashlib.md5(m.group(1).encode()).hexdigest()==css_hash:
        s=s[:m.start()]+'<link id="topnav-css" rel="stylesheet" href="'+r+'assets/site-nav.css">'+s[m.end():]
        cssnote='CSS->link'
    else:
        cssnote='CSS kept inline (page-specific)'
    open(p,'w',encoding='utf-8').write(s)
    print(p, '| JS->external |', cssnote)
print('shared files: assets/site-nav.css (%d B), assets/site-nav.js (%d B)'%(os.path.getsize('assets/site-nav.css'),os.path.getsize('assets/site-nav.js')))
