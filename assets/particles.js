/*
  Background particles, on every page. A fixed canvas behind the content: faint dots in the
  text colour (--c at 18%) drift slowly, and move away from the cursor when it comes close.
  Follows the theme picker. With reduced motion the dots are drawn once and stay still.
*/
(function () {
  const COUNT = 840;          // dots for a 1440x900 screen, scaled by screen area
  const RADIUS = 130;         // how close the cursor has to be to push a dot
  const PUSH = 900;           // push strength (px/s at the cursor)
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const canvas = document.createElement('canvas');
  canvas.id = 'bgParticles';
  canvas.setAttribute('aria-hidden', 'true');
  canvas.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:-1;pointer-events:none';
  document.body.prepend(canvas);
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  let W = 0, H = 0, dpr = 1, dots = [], colour = '#2c2c2c';
  const mouse = { x: -1e4, y: -1e4 };

  function readColour() {
    colour = getComputedStyle(document.documentElement).getPropertyValue('--c').trim() || colour;
    if (reduced) draw();
  }

  function target() {
    return Math.round(COUNT * Math.min(1.6, Math.max(0.4, (W * H) / (1440 * 900))));
  }
  function dot() {
    const a = Math.random() * Math.PI * 2, sp = 5 + Math.random() * 9;
    return { x: Math.random() * W, y: Math.random() * H, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, ox: 0, oy: 0 };
  }

  // Keep the dots spread over the whole window: on every resize, stretch their positions to the
  // new size and add or remove dots so the density stays even.
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, window.innerWidth), h = Math.max(1, window.innerHeight);
    if (!dots.length || W < 50 || H < 50) {
      W = w; H = h;
      dots = Array.from({ length: target() }, dot);
    } else if (w !== W || h !== H) {
      const sx = w / W, sy = h / H;
      for (const d of dots) { d.x *= sx; d.y *= sy; }
      W = w; H = h;
      const n = target();
      while (dots.length < n) dots.push(dot());
      if (dots.length > n) dots.length = n;
    }
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (reduced) draw();
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = colour;
    ctx.globalAlpha = 0.18;
    ctx.beginPath();
    for (const d of dots) {
      ctx.moveTo(d.x + d.ox + 1.2, d.y + d.oy);
      ctx.arc(d.x + d.ox, d.y + d.oy, 1.2, 0, Math.PI * 2);
    }
    ctx.fill();
    ctx.globalAlpha = 1;
  }

  let last = performance.now();
  function step(now) {
    const dt = Math.min(0.05, (now - last) / 1000);
    last = now;
    for (const d of dots) {
      d.x += d.vx * dt;
      d.y += d.vy * dt;
      // push away from the cursor, then ease back to the drifting path
      const px = d.x + d.ox, py = d.y + d.oy;
      const dx = px - mouse.x, dy = py - mouse.y, dist = Math.hypot(dx, dy);
      if (dist < RADIUS && dist > 0.01) {
        const f = PUSH * (1 - dist / RADIUS) * dt / dist;
        d.ox += dx * f;
        d.oy += dy * f;
      }
      d.ox *= 1 - Math.min(1, 1.6 * dt);
      d.oy *= 1 - Math.min(1, 1.6 * dt);
      if (d.x < -10) d.x = W + 10; else if (d.x > W + 10) d.x = -10;
      if (d.y < -10) d.y = H + 10; else if (d.y > H + 10) d.y = -10;
    }
    draw();
    requestAnimationFrame(step);
  }

  window.addEventListener('resize', resize);
  if (!reduced) {
    window.addEventListener('pointermove', e => { mouse.x = e.clientX; mouse.y = e.clientY; }, { passive: true });
    document.addEventListener('pointerleave', () => { mouse.x = -1e4; mouse.y = -1e4; });
  }
  // the theme picker changes --c on <html>
  new MutationObserver(readColour).observe(document.documentElement, { attributes: true, attributeFilter: ['style', 'class', 'data-theme'] });
  document.addEventListener('click', e => { if (e.target.closest && e.target.closest('.swatch')) setTimeout(readColour, 50); });

  readColour();
  resize();
  if (reduced) draw(); else requestAnimationFrame(step);
})();
