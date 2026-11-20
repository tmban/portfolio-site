/*
  Full process: the long case study lives in <details id="process">, folded by default.
  Opens it when the URL ends in #process, when a link points at #process, or when a link
  points at a section inside it. Marks <html> so the section dots show only while it is open.
*/
(() => {
  const proc = document.getElementById('process');
  if (!proc) return;
  const root = document.documentElement;
  const sync = () => root.classList.toggle('process-open', proc.open);

  const openFor = (hash) => {
    if (!hash || hash === '#') return false;
    let target = null;
    try { target = document.querySelector(hash); } catch (e) { return false; }
    if (!target || !(target === proc || proc.contains(target))) return false;
    proc.open = true;
    sync();
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
    return true;
  };

  proc.addEventListener('toggle', sync);
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="#"]');
    if (a && openFor(a.getAttribute('href'))) {
      e.preventDefault();
      history.replaceState(null, '', a.getAttribute('href'));
    }
  });
  window.addEventListener('hashchange', () => openFor(location.hash));
  openFor(location.hash);
  sync();
})();

/* Gallery and Full process: click a picture to see it full size. Arrows or the keyboard move through the set; Esc or a click outside closes. */
(() => {
  const imgs = [...document.querySelectorAll('.cs-gallery img, .fp-fig img')];
  if (!imgs.length) return;
  const box = document.createElement('div');
  box.className = 'cs-lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Gallery image');
  box.innerHTML = '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button class="cs-lightbox__close" type="button" aria-label="Close">&times;</button>' +
    '<button class="cs-lightbox__prev" type="button" aria-label="Previous image">&#8249;</button>' +
    '<button class="cs-lightbox__next" type="button" aria-label="Next image">&#8250;</button>';
  document.body.append(box);
  const big = box.querySelector('img'), cap = box.querySelector('figcaption');
  let i = 0, opener = null;
  const show = (n) => {
    i = (n + imgs.length) % imgs.length;
    big.src = imgs[i].currentSrc || imgs[i].src;
    big.alt = imgs[i].alt;
    const c = imgs[i].closest('figure')?.querySelector('figcaption');
    cap.textContent = c ? c.textContent : '';
  };
  const open = (n) => { opener = document.activeElement; show(n); box.classList.add('open'); document.documentElement.style.overflow = 'hidden'; box.querySelector('.cs-lightbox__close').focus(); };
  const close = () => { box.classList.remove('open'); document.documentElement.style.overflow = ''; opener && opener.focus && opener.focus(); };
  imgs.forEach((img, n) => {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.addEventListener('click', () => open(n));
    img.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(n); } });
  });
  box.addEventListener('click', (e) => { if (e.target === box || e.target.closest('figure') === null && !e.target.closest('button')) close(); });
  box.querySelector('.cs-lightbox__close').addEventListener('click', close);
  box.querySelector('.cs-lightbox__prev').addEventListener('click', () => show(i - 1));
  box.querySelector('.cs-lightbox__next').addEventListener('click', () => show(i + 1));
  document.addEventListener('keydown', (e) => {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(i - 1);
    else if (e.key === 'ArrowRight') show(i + 1);
  });
})();
