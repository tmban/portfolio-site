(function(){
  var nav=document.getElementById('topnav'); if(!nav) return;
  var footer=document.getElementById('footerBody')||document.querySelector('.footer__body');
  function onScroll(){
    nav.classList.toggle('scrolled', window.scrollY>20);
    // once the footer reaches the nav, the nav takes the footer's colour
    nav.classList.toggle('on-footer', !!footer && footer.getBoundingClientRect().top <= nav.offsetHeight);
  }
  window.addEventListener('scroll',onScroll,{passive:true}); window.addEventListener('resize',onScroll); onScroll();
  var work=nav.querySelector('.topnav__work'), wbtn=work&&work.querySelector('.topnav__work-btn');
  if(wbtn){ wbtn.addEventListener('click',function(e){e.stopPropagation();var o=work.classList.toggle('open');wbtn.setAttribute('aria-expanded',o);}); }
  // hovering a project name fans out its screens beside the menu
  var dd=nav.querySelector('.topnav__dropdown');
  if(dd){ [].forEach.call(dd.querySelectorAll('.topnav__dd-item[data-tiles]'),function(a){
    a.addEventListener('mouseenter',function(){ dd.setAttribute('data-hover',a.getAttribute('data-tiles')); });
    a.addEventListener('focus',function(){ dd.setAttribute('data-hover',a.getAttribute('data-tiles')); });
    a.addEventListener('mouseleave',function(){ dd.removeAttribute('data-hover'); });
    a.addEventListener('blur',function(){ dd.removeAttribute('data-hover'); });
  }); }
  document.addEventListener('click',function(){ if(work){work.classList.remove('open');wbtn&&wbtn.setAttribute('aria-expanded','false');} });
  var burger=document.getElementById('topnavBurger'), mob=document.getElementById('topnavMobile');
  if(burger&&mob){ burger.addEventListener('click',function(){ var o=mob.classList.toggle('open'); burger.classList.toggle('active',o); }); }
  // mobile and tablet menu: Work opens the project list
  var mwork=mob&&mob.querySelector('.topnav__mwork');
  if(mwork){ mwork.addEventListener('click',function(){ var o=mob.classList.toggle('work-open'); mwork.setAttribute('aria-expanded',o); }); }
})();
