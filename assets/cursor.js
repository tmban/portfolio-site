/* Site cursor — brand arrow that morphs to the drawn hand trio on clickables */
(function () {
  if (!matchMedia('(pointer: fine)').matches) return;
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const HAND = 'M13 4.5a2 2 0 0 1 4 0V15h1.2V7.5a2 2 0 0 1 4 0V15h1.2V10a2 2 0 0 1 4 0v8.2c0 6-3.6 9.8-9.4 9.8-4.4 0-6.8-2-8.6-5.3l-3-5.4c-.55-1-.2-2.2.8-2.75.95-.55 2.15-.25 2.75.65l2.05 3V4.5z';
  const ARROW = 'M6 3v17.6l4.3-3.9 2.8 6.5 3.3-1.4-2.8-6.4 6-.5z';
  const make = (size, cls) => {
    const d = document.createElement('div');
    d.className = 'cursor-hand ' + cls;
    d.innerHTML = `<svg width="${size}" height="${size}" viewBox="0 0 32 32"><path d="${HAND}" fill="#c2410c" stroke="#fff" stroke-width="1.6"/></svg>`;
    document.body.append(d);
    return d;
  };
  const main = document.createElement('div');
  main.className = 'cursor-hand cursor-hand--main';
  main.innerHTML =
    `<svg class="icon-arrow" width="24" height="24" viewBox="0 0 26 26"><path d="${ARROW}" fill="#c2410c" stroke="#fff" stroke-width="1.5"/></svg>` +
    `<svg class="icon-hand" width="26" height="26" viewBox="0 0 32 32"><path d="${HAND}" fill="#c2410c" stroke="#fff" stroke-width="1.6"/></svg>`;
  document.body.append(main);
  const mid = reduced ? null : make(17, 'cursor-hand--m');
  const small = reduced ? null : make(12, 'cursor-hand--s');
  const root = document.documentElement;
  let mx = -100, my = -100, over = false, seen = false;
  const p1 = [-100, -100], p2 = [-100, -100];
  addEventListener('mousemove', e => {
    mx = e.clientX; my = e.clientY;
    if (!seen) { seen = true; root.classList.add('cur-live'); }
    main.style.transform = `translate3d(${mx - 5}px,${my - 3}px,0)`;
  }, { passive: true });
  if (!reduced) {
    const loop = () => {
      p1[0] += (mx - p1[0]) * 0.14; p1[1] += (my - p1[1]) * 0.14;
      p2[0] += (p1[0] - p2[0]) * 0.14; p2[1] += (p1[1] - p2[1]) * 0.14;
      mid.style.transform = `translate3d(${p1[0] - 2}px,${p1[1] + 8}px,0)`;
      small.style.transform = `translate3d(${p2[0] - 1}px,${p2[1] + 14}px,0)`;
      requestAnimationFrame(loop);
    };
    requestAnimationFrame(loop);
  }
  document.addEventListener('mouseover', e => {
    const hit = !!e.target.closest('a,button,[role="button"]');
    if (hit && !over) {
      // the small hands assemble under the lead hand, then trail
      p1[0] = mx; p1[1] = my; p2[0] = mx; p2[1] = my;
    }
    over = hit;
    root.classList.toggle('cur-on', hit);
  });
  document.addEventListener('focusin', e => {
    if (e.target.closest('input,textarea,select')) root.classList.add('cur-hidden');
  });
  document.addEventListener('focusout', () => root.classList.remove('cur-hidden'));
  document.addEventListener('mouseleave', () => root.classList.remove('cur-on', 'cur-live'));
  document.addEventListener('mouseenter', () => { if (seen) root.classList.add('cur-live'); });
})();
