(function(){
  var nav=document.getElementById('topnav'); if(!nav) return;
  function onScroll(){ nav.classList.toggle('scrolled', window.scrollY>20); }
  window.addEventListener('scroll',onScroll,{passive:true}); onScroll();
  var work=nav.querySelector('.topnav__work'), wbtn=work&&work.querySelector('.topnav__work-btn');
  if(wbtn){ wbtn.addEventListener('click',function(e){e.stopPropagation();var o=work.classList.toggle('open');wbtn.setAttribute('aria-expanded',o);}); }
  document.addEventListener('click',function(){ if(work){work.classList.remove('open');wbtn&&wbtn.setAttribute('aria-expanded','false');} });
  var burger=document.getElementById('topnavBurger'), mob=document.getElementById('topnavMobile');
  if(burger&&mob){ burger.addEventListener('click',function(){ var o=mob.classList.toggle('open'); burger.classList.toggle('active',o); }); }
})();
