import re, os

PROJ = {
 'arbor':  ('arbor/arbor.html',   'arbor.html',   'Arbor'),
 'plio':   ('plio/plio.html',     'plio.html',    'Plio'),
 'kova':   ('kova/index.html',    'index.html',   'Kova'),
 'verde':  ('verde/verde.html',   'verde.html',   'Verde'),
 'finning':('finning/finning.html','finning.html','Finning'),
 'onbuy':  ('onbuy/onbuy.html',   'onbuy.html',   'OnBuy'),
}

FP_STYLE = """
<style id="fp-style">
.fp-top{position:sticky;top:0;z-index:50;display:flex;align-items:center;justify-content:space-between;padding:16px 40px;background:rgba(255,255,255,.9);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);border-bottom:1px solid var(--line-faint)}
.fp-logo{font:600 16px/1 var(--serif);color:var(--ink);text-decoration:none;letter-spacing:-.01em}
.fp-back{font:500 13px/1 var(--sans);color:var(--muted);text-decoration:none;transition:color .15s}
.fp-back:hover{color:var(--ink)}
#features{padding-top:54px!important;padding-bottom:80px!important}
#features .feat .frame-label{display:block!important;font:600 11px/1 var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:14px!important}
@media(max-width:640px){.fp-top{padding:14px 20px}}
</style>
"""

def slugify(t):
    s=re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
    return '-'.join(s.split('-')[:5]) or 'feature'

def supp_sub_css(s):
    # add .supp-sub rule right after the .supp-h{...} declaration if missing
    if '.supp-sub{' in s: return s
    m=re.search(r'(\.supp-h\{[^}]*\})', s)
    rule='.supp-sub{margin:7px 0 0;font:400 14.5px/1.55 var(--sans);color:var(--muted)}'
    return s[:m.end()]+rule+s[m.end():] if m else s

for name,(path,base,title) in PROJ.items():
    s=open(path,encoding='utf-8').read()
    head=s[:s.index('</head>')]            # everything up to (not incl) </head>
    # section bounds
    ms=re.search(r'<section class="features" id="more-system">',s)
    start=ms.start(); end=s.index('</section>',start)+len('</section>')
    block=s[start:end]
    # wrap heading parts
    lbl=re.search(r'<div class="sec-label">([^<]+)</div>',block).group(1)
    h2 =re.search(r'<h2 class="sec-h">([^<]+)</h2>',block).group(1)
    sub=re.search(r'<p class="sec-sub">(.*?)</p>',block,re.S).group(1).strip()
    # articles
    arts=re.findall(r'<article class="feat.*?</article>',block,re.S)
    cards=[]
    used=set()
    for art in arts:
        sl=re.search(r'fx-[a-z]+-feature-([a-z0-9-]+)',art)
        fh=re.search(r'class="frame-heading">([^<]+)<',art)
        heading=fh.group(1).strip() if fh else 'Feature'
        fsm=re.search(r'class="frame-sub">(.*?)</div>',art,re.S)
        fsub=re.sub(r'\s+',' ',fsm.group(1)).strip() if fsm else ''
        slug=sl.group(1) if sl else slugify(heading)
        b=slug; i=2
        while slug in used: slug=f'{b}-{i}'; i+=1
        used.add(slug)
        # ---- standalone feature page ----
        fhead=head
        fhead=re.sub(r'<title>.*?</title>', f'<title>{heading} | {title}</title>', fhead, count=1, flags=re.S)
        page=(fhead+FP_STYLE+'</head>\n'
              f'<body>\n<header class="fp-top"><a class="fp-logo" href="{base}">{title}</a>'
              f'<a class="fp-back" href="{base}#more-system">Back to all features</a></header>\n'
              '<main><section class="features" id="features"><div class="feat-stream">\n'
              f'{art}\n</div></section></main>\n</body>\n</html>')
        fp=os.path.join(os.path.dirname(path), f'feature-{slug}.html')
        open(fp,'w',encoding='utf-8').write(page)
        # ---- card ----
        cards.append(
          f'    <a class="supp-card" href="feature-{slug}.html">\n'
          f'      <div class="supp-thumb"><iframe loading="lazy" tabindex="-1" title="{heading}" src="feature-{slug}.html"></iframe></div>\n'
          f'      <div class="supp-body"><div class="supp-h">{heading}</div><p class="supp-sub">{fsub}</p></div>\n'
          f'    </a>')
    new_section=(
      '<section class="features" id="more-system">\n'
      '  <div class="wrap">\n'
      f'    <div class="sec-label">{lbl}</div>\n'
      f'    <h2 class="sec-h">{h2}</h2>\n'
      f'    <p class="sec-sub">{sub}</p>\n'
      '  </div>\n'
      '  <div class="supp-grid">\n'+'\n'.join(cards)+'\n  </div>\n'
      '</section>')
    s2=s[:start]+new_section+s[end:]
    s2=supp_sub_css(s2)
    open(path,'w',encoding='utf-8').write(s2)
    print(f'{name:8} pages={len(arts)} slugs={sorted(used)}')
print('DONE')
