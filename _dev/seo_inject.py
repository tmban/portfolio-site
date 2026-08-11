# -*- coding: utf-8 -*-
import re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

pages = {
 'index.html': dict(
   url='https://thomasmbanefo.com/',
   title='Thomas Mbanefo: Product designer for data-heavy enterprise and AI software',
   desc='Product designer specialising in data-heavy enterprise software and AI products. Selected case studies across analytics, fintech, marketplace and ESG.',
   img='https://thomasmbanefo.com/assets/tiles/kv10-solid.webp'),
 'about.html': dict(
   url='https://thomasmbanefo.com/about.html',
   title='About: Thomas Mbanefo, product designer (Birmingham, UK)',
   desc='Thomas Mbanefo is a product designer based in Birmingham, UK, working in complex enterprise products, data platforms and AI pipelines.',
   img='https://thomasmbanefo.com/assets/tiles/kv10-solid.webp'),
 'kova/index.html': dict(
   url='https://thomasmbanefo.com/kova/',
   title='Kova: Analytics and data-quality intelligence · Thomas Mbanefo',
   desc='How fund managers stopped exporting to Power BI: an analytics and data-quality platform turning raw portfolio data into the answers they were asking.',
   img='https://thomasmbanefo.com/assets/tiles/kv10-solid.webp'),
 'arbor/arbor.html': dict(
   url='https://thomasmbanefo.com/arbor/arbor.html',
   title='Arbor: Asset-platform data-model rebuild · Thomas Mbanefo',
   desc='Rebuilding the entity data foundation an entire asset platform stands on, from the data model up through onboarding and the interface.',
   img='https://thomasmbanefo.com/assets/tiles/ar13-solid.webp'),
 'verde/verde.html': dict(
   url='https://thomasmbanefo.com/verde/verde.html',
   title='Verde: Governed ESG reporting workspace · Thomas Mbanefo',
   desc='A live, governed, traceable ESG reporting workspace, from raw portfolio data to filed disclosure, with a paper trail on every number.',
   img='https://thomasmbanefo.com/assets/tiles/vd13-solid.webp'),
 'plio/plio.html': dict(
   url='https://thomasmbanefo.com/plio/plio.html',
   title='Plio: AI invoice pipeline, human-in-the-loop · Thomas Mbanefo',
   desc='AI-assisted invoice ingestion with guardrails, not a black box: confidence-graded and human-in-the-loop across a multi-country portfolio.',
   img='https://thomasmbanefo.com/assets/tiles/pl8-solid.webp'),
 'onbuy/onbuy.html': dict(
   url='https://thomasmbanefo.com/onbuy/onbuy.html',
   title='OnBuy: Checkout and discovery redesign · Thomas Mbanefo',
   desc="Redesigning checkout and product discovery for one of the UK's largest marketplaces, cutting checkout abandonment across millions of listings.",
   img='https://thomasmbanefo.com/assets/tiles/ob5.webp'),
 'finning/finning.html': dict(
   url='https://thomasmbanefo.com/finning/finning.html',
   title='Finning: Self-serve finance calculator and dealer portal · Thomas Mbanefo',
   desc='The first self-serve finance calculator and dealer portal Finning shipped on mobile, turning sales-gated quotes into a self-serve estimate.',
   img='https://thomasmbanefo.com/assets/tiles/fn1.webp'),
}

def esc(s):
    return s.replace('&', '&amp;')

BLOCK = """<title>{t}</title>
<!--SEO_START-->
<meta name="description" content="{d}">
<link rel="canonical" href="{u}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Thomas Mbanefo">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{u}">
<meta property="og:image" content="{i}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{i}">
<!--SEO_END-->"""

for rel, p in pages.items():
    fp = os.path.join(BASE, rel)
    with open(fp, 'r', encoding='utf-8') as f:
        html = f.read()
    # strip any prior SEO block (idempotent)
    html = re.sub(r'\n?<!--SEO_START-->.*?<!--SEO_END-->', '', html, flags=re.DOTALL)
    block = BLOCK.format(t=esc(p['title']), d=esc(p['desc']), u=p['url'], i=p['img'])
    new, n = re.subn(r'<title>.*?</title>', lambda m: block, html, count=1, flags=re.DOTALL)
    if n != 1:
        print('WARN no <title> in', rel); continue
    with open(fp, 'w', encoding='utf-8') as f:
        f.write(new)
    print('SEO ok:', rel)
