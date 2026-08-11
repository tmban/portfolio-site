# adds an accessible pause/play control to the hero carousel (WCAG 2.2.2)
pages=['kova/index.html','verde/verde.html','arbor/arbor.html','plio/plio.html','onbuy/onbuy.html','finning/finning.html']

CSS=(".hcs-playpause{position:absolute;bottom:16px;right:14px;z-index:7;width:30px;height:30px;"
     "border-radius:50%;border:1px solid var(--border,#e0e0e0);background:rgba(255,255,255,.86);"
     "color:#333;font:700 10px/1 system-ui,sans-serif;cursor:pointer;display:flex;align-items:center;"
     "justify-content:center;padding:0;-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px)}"
     ".hcs-playpause:hover{color:#000}@media(max-width:600px){.hcs-playpause{display:none}}\n")

SLIDES_ANCHOR="var slides = Array.prototype.slice.call(track.querySelectorAll('.hcs-slide'));"
JS_INJECT=("\n  var paused=false, playBtn=document.createElement('button');"
  "\n  playBtn.type='button'; playBtn.className='hcs-playpause';"
  "\n  playBtn.setAttribute('aria-pressed','false'); playBtn.setAttribute('aria-label','Pause slideshow');"
  "\n  playBtn.textContent='❚❚';"
  "\n  function setPaused(p){ paused=p; playBtn.setAttribute('aria-pressed',p?'true':'false');"
  " playBtn.setAttribute('aria-label',p?'Play slideshow':'Pause slideshow');"
  " playBtn.textContent=p?'▶':'❚❚';"
  " if(p){ if(timer){clearTimeout(timer);clearInterval(timer);timer=null;} } else { schedule(); } }"
  "\n  playBtn.addEventListener('click', function(){ setPaused(!paused); });"
  "\n  carousel.appendChild(playBtn);")

SCHED_ANCHOR="if(timer){ clearTimeout(timer); clearInterval(timer); timer = null; }"
SCHED_INJECT=SCHED_ANCHOR+"\n    if(paused){ return; }"

for p in pages:
    s=open(p,encoding='utf-8').read(); orig=s
    assert s.count('<style id="a11y-fixes">')==1, p+" a11y block"
    assert s.count(SLIDES_ANCHOR)==1, p+" slides anchor"
    assert s.count(SCHED_ANCHOR)==1, p+" sched anchor"
    s=s.replace('<style id="a11y-fixes">','<style id="a11y-fixes">\n'+CSS,1)
    s=s.replace(SLIDES_ANCHOR, SLIDES_ANCHOR+JS_INJECT,1)
    s=s.replace(SCHED_ANCHOR, SCHED_INJECT,1)
    open(p,'w',encoding='utf-8').write(s)
    print("OK",p)
print("done")
