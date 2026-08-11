# -*- coding: utf-8 -*-
import re, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = ['index.html','about.html','kova/index.html','arbor/arbor.html',
         'verde/verde.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html']

SKIP_CSS = ('<style id="a11y-skip">'
            '.skip-link{position:absolute;left:-9999px;top:0;z-index:1000;'
            'background:#2c2c2c;color:#fff;padding:10px 18px;border-radius:0 0 8px 0;'
            'font:600 14px/1 \'Inter\',sans-serif;text-decoration:none}'
            '.skip-link:focus{left:0}#main:focus{outline:none}'
            '</style>')

for rel in pages:
    fp = os.path.join(BASE, rel)
    with open(fp,'r',encoding='utf-8') as f: html=f.read()
    if 'id="main"' in html:
        print('skip (already done):', rel); continue

    # 1) skip-link CSS into <head> (before </head>)
    if 'id="a11y-skip"' not in html:
        html = html.replace('</head>', SKIP_CSS + '\n</head>', 1)

    # 2) skip-link anchor right after <body ...>
    html = re.sub(r'(<body[^>]*>)',
                  r'\1\n<a class="skip-link" href="#main">Skip to content</a>',
                  html, count=1)

    # 3) open <main> before first hero section
    if '<section class="hero"' in html:
        html = html.replace('<section class="hero"',
                            '<main id="main" tabindex="-1">\n<section class="hero"', 1)
    elif '<section class="about-hero"' in html:
        html = html.replace('<section class="about-hero"',
                            '<main id="main" tabindex="-1">\n<section class="about-hero"', 1)
    else:
        print('WARN no hero anchor:', rel); continue

    # 4) close </main> before first <footer
    html = re.sub(r'(<footer)', r'</main>\n\1', html, count=1)

    with open(fp,'w',encoding='utf-8') as f: f.write(html)
    print('landmarks ok:', rel)
