# -*- coding: utf-8 -*-
import re, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = ['index.html','about.html','kova/index.html','arbor/arbor.html',
         'verde/verde.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html']

# match a full <img ...> tag
tag_re = re.compile(r'<img\b[^>]*>', re.IGNORECASE)

def fix(tag):
    if re.search(r'\bloading\s*=', tag, re.IGNORECASE):
        return tag  # already has loading
    # insert loading="lazy" + decoding="async" right after <img
    return tag[:4] + ' loading="lazy" decoding="async"' + tag[4:]

for rel in pages:
    fp = os.path.join(BASE, rel)
    with open(fp,'r',encoding='utf-8') as f: html=f.read()
    added = [0]
    def repl(m):
        new = fix(m.group(0))
        if new != m.group(0): added[0]+=1
        return new
    html = tag_re.sub(repl, html)
    with open(fp,'w',encoding='utf-8') as f: f.write(html)
    print(f'{rel}: +{added[0]} lazy')
