# Portfolio 2026 Enhancement Brief
> Claude Code implementation guide — read this before touching any file.

## What this codebase is

Static HTML/CSS/JS portfolio at `thomasmbanefo.com`. No build step, no bundler, no framework — every page is a self-contained `.html` file. Assets live in `/assets/`. Case study folders (`/kova/`, `/plio/`, etc.) each have their own `.html` and a `/motion/` subfolder of embedded HTML animations.

---

## Step 0 — Colour system overhaul (do this first, before any enhancement)

The existing colour system used `#c2410c` (orange-red) as the accent and had three theme switcher options (cream, green, purple). Both are being replaced. This is a **global change** — update every file that contains these values.

### New CSS custom property defaults

Replace the `:root` block on **every HTML file in the repo** (index, about, and all case study pages):

```css
:root {
  --p: #fafaf9;   /* page background — warm off-white */
  --s: #4338CA;   /* accent — deep indigo */
  --c: #1a1a1a;   /* content / text — rich near-black */
  --ease:     cubic-bezier(.16, 1, .3, 1);
  --ease-out: cubic-bezier(.22, .61, .36, 1);
}
```

### New theme switcher — three themes replacing the old three

The `.picker` currently has swatches for cream, green, and purple. Replace with **light**, **dark**, and **warm**:

```html
<!-- Replace existing .swatch elements with these three -->
<div class="swatch" data-theme="light"  data-p="#fafaf9" data-s="#4338CA" data-c="#1a1a1a" style="--si:0"></div>
<div class="swatch" data-theme="dark"   data-p="#0f0f11" data-s="#818CF8" data-c="#e8e8f0" style="--si:1"></div>
<div class="swatch" data-theme="warm"   data-p="#f5ede0" data-s="#B45309" data-c="#1a1611" style="--si:2"></div>
```

Update the `localStorage` theme-persistence script at the top of `<head>` to handle the new theme names. The existing logic reads `tm_theme` from localStorage and sets `--p`, `--s`, `--c` — the mechanism stays identical, only the values change.

Update the swatch CSS colour dots to match the new themes:
```css
.swatch[data-theme="light"] { background: #4338CA }  /* show the accent, not the bg */
.swatch[data-theme="dark"]  { background: #0f0f11 }
.swatch[data-theme="warm"]  { background: #B45309 }
```

### Frosted glass nav — theme-aware

The `.topnav` uses a hardcoded `background: #fff` in `#topnav-css`. Replace with `background: var(--p)` so it inherits the theme background. The `.scrolled` state (added in Enhancement 2 below) should use `rgba` derived from `--p`:

```css
/* These values must account for all three themes */
[data-theme="dark"]  .topnav.scrolled { background: rgba(15,15,17,0.80); }
[data-theme="warm"]  .topnav.scrolled { background: rgba(245,237,224,0.80); }
/* default (light) handled by the base rule */
```

### Dark theme body background

When `data-theme="dark"` is set on `<html>`, ensure `body { background: var(--p) }` already handles it — it does via the existing CSS var system. No additional rules needed unless a component has a hardcoded `background: #fff` — audit and replace those with `var(--p)` or `var(--p, #fafaf9)`.

### Contrast verification — do not skip

Before moving to enhancements, verify these contrast ratios pass WCAG AA (4.5:1 for normal text, 3:1 for large):

| Theme | Foreground (`--c`) | Background (`--p`) | Ratio |
|-------|--------------------|--------------------|-------|
| Light | `#1a1a1a` | `#fafaf9` | ~19:1 ✓ |
| Dark  | `#e8e8f0` | `#0f0f11` | ~15:1 ✓ |
| Warm  | `#1a1611` | `#f5ede0` | ~16:1 ✓ |

Accent on background:
| Theme | Accent (`--s`) | Background (`--p`) | Ratio |
|-------|----------------|--------------------|-------|
| Light | `#4338CA` | `#fafaf9` | ~6.8:1 ✓ |
| Dark  | `#818CF8` | `#0f0f11` | ~8.2:1 ✓ |
| Warm  | `#B45309` | `#f5ede0` | ~5.5:1 ✓ |

---

## Design system rules — enforce throughout

Every colour decision on this site runs through three CSS custom properties:

```css
--p  /* page background */
--s  /* accent */
--c  /* content / text */
```

**All additions must use `var(--p)`, `var(--s)`, `var(--c)` — no hardcoded hex values for anything visible.** The only exception is `rgba(0,0,0,…)` for shadows, which is neutral. This ensures the three themes all work without additional overrides.

Typography is Fira Sans (headings, labels) + Inter (body, UI). Do not add any new font.

---

## Enhancements — implement in this order (after Step 0)

### 1. Three.js hero background (`index.html` only)

Add a Three.js particle field as the hero backdrop. Load Three.js from CDN (`https://unpkg.com/three@0.160.1/build/three.module.js`) as an ES module — do not use a global script tag.

**Behaviour:**
- A canvas sits behind the `.hero` section (`z-index: 0`, `position: absolute`, `inset: 0`, `pointer-events: none`)
- ~140 particles drawn as small dots, colour `var(--c)` at 18% opacity — they should feel like graph paper or data points, not a screensaver
- Particles drift very slowly (speed ~0.15 units/s), no physics, no collisions
- On `mousemove` over the hero, particles within ~180px of the cursor shift slightly toward it (attraction strength 0.04) — ties into the existing magnetic hero-image effect
- Colour is read at runtime from `getComputedStyle(document.documentElement).getPropertyValue('--c')` so it reacts to the theme switcher
- Re-read colour whenever a `.swatch` is clicked (hook into the existing swatch click handler — find it in the inline `<script>` near the bottom of `index.html`)
- Respect `prefers-reduced-motion: reduce` — if set, render particles statically with no drift or attraction
- Canvas resizes with `ResizeObserver` on the hero element

**What it should NOT be:** Abstract colourful blobs, animated gradient meshes, glowing rings. This is a data/enterprise designer's portfolio — the Three.js element should feel like it belongs in a product dashboard. Think: faint node graph, not a music visualiser.

**Placement in file:** Add the `<canvas id="heroCanvas">` as the first child of `.hero`. Add the ES module `<script type="module">` just before `</body>`. Do not alter any existing JS.

---

### 2. Frosted glass nav on scroll (`index.html` + `about.html`)

The `.topnav` element currently has a hardcoded `background: #fff` in `#topnav-css`. 

First, replace `background: #fff` with `background: var(--p)` so it inherits the active theme.

When the user scrolls more than 12px, the existing JS adds a `.scrolled` class (check `assets/site-nav.js` — if the toggle is already there, do not duplicate it). Update the `.topnav.scrolled` CSS rule to:

```css
.topnav.scrolled {
  background: rgba(250, 250, 249, 0.76);  /* light theme default */
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border-bottom: 1px solid rgba(26, 26, 26, 0.08);
  box-shadow: 0 1px 0 rgba(26,26,26,0.05);
}
[data-theme="dark"] .topnav.scrolled {
  background: rgba(15, 15, 17, 0.82);
  border-bottom-color: rgba(232,232,240,0.10);
}
[data-theme="warm"] .topnav.scrolled {
  background: rgba(245, 237, 224, 0.80);
  border-bottom-color: rgba(26,22,17,0.08);
}
```

Apply the same CSS changes to `about.html`.

---

### 3. Custom cursor (`index.html` only to start)

A two-part cursor: a 6px filled dot that tracks the mouse directly, and a 28px hollow ring that follows with ~80ms lag (lerp factor 0.12 per frame).

**Colours — must use CSS vars, read at runtime:**
- Dot: `var(--s)` (the indigo accent) — picks up theme changes
- Ring: `var(--c)` at 35% opacity — picks up theme changes
- Both are `position: fixed`, `pointer-events: none`, `z-index: 9999`

**State changes (add CSS classes, not inline style overrides):**
- On `.f-card` hover → ring scales to 52px, dot hides, ring gets a semi-transparent fill of `var(--s)` at 12% opacity and shows text "VIEW" centred — 9px Fira Sans 700 uppercase, colour `var(--s)`
- On `.topnav__cta` or `.btn-primary` hover → dot scales to 10px
- On text `<p>`, `<h1>`–`<h6>` hover → ring shrinks to 18px (text-reading mode)
- On `<input>` focus → hide both elements entirely

Hide the native cursor on `body`: **only on `pointer: fine` devices**:
```css
@media (pointer: fine) { body { cursor: none } }
```
Touch and tablet users are unaffected.

Re-read `--s` and `--c` colours from `getComputedStyle` on every swatch click so the cursor updates with the theme.

**Dark theme note:** On the dark theme, `--s` is `#818CF8` (light indigo) and `--c` is `#e8e8f0` — both are light colours against a dark background, so contrast is fine. The cursor uses CSS vars so this is automatic.

---

### 4. Bento grid for Featured Work (`index.html`)

Replace the current equal 3×2 grid (`#fgrid`) with a bento layout that gives Arbor and Kova (the two flagship enterprise case studies) a wider slot.

**Target layout (desktop ≥ 900px):**
```
[ Arbor — wide 2/3 ] [ Finning — 1/3 ]
[ Kova — wide 2/3  ] [ OnBuy — 1/3  ]
[ Plio — 1/2       ] [ Design System — 1/2 ]
```

Use `grid-template-areas` — do not use JS for layout. The grid wrapper already has `max-width: 1320px`.

Wide cards (`Arbor`, `Kova`) get `aspect-ratio: 16/9` instead of `1/1`. The image inside should `object-fit: cover`. Everything else stays `aspect-ratio: 1`.

On tablet (≤ 900px): collapse to `grid-template-columns: 1fr 1fr`, all cards equal, `aspect-ratio: 1`. On mobile (≤ 560px): single column.

**The card hover** — replace the existing minimal `translateY(-4px)` with a subtle 3D tilt using `perspective` + `rotateX` / `rotateY` driven by mouse position within the card. Max tilt ±6deg. Transition back on `mouseleave` with `transition: transform 0.5s var(--ease-out)`. Keep the existing box-shadow change.

---

### 5. Scroll-driven metric counters

The project labels already contain metric strings like `"66.7% faster onboarding"`, `"−23% checkout abandonment"`, `"86% parsing accuracy"`. These are in `.proj-label__metric` spans. The metric text colour is currently hardcoded as `#c2410c` in `.proj-label__metric` — **update this to `var(--s)`** so it uses the new indigo accent and responds to theme changes.

When each `.proj` enters the viewport (the `IntersectionObserver` already fires `inview`), parse the numeric value from the metric text, animate it counting up from 0 over 900ms using `requestAnimationFrame` with an ease-out curve, then snap to the final value. Preserve the `%`, `−`, `+` and surrounding text exactly — only the number animates.

Do not alter the DOM structure. Write a small utility function `animateMetric(el)` called inside the existing `io` observer callback.

---

### 6. Logo strip marquee (`index.html` + `about.html`)

The `.logo-strip__marks` `<ul>` currently sits static. Convert it to an infinite CSS marquee:

- Duplicate the `<li>` items once in JS (so the loop is seamless) — do not change the HTML source
- Animate with `@keyframes marquee { from { transform: translateX(0) } to { transform: translateX(-50%) } }` at 28s linear infinite on the inner flex container
- Pause on hover (`animation-play-state: paused`)
- Respect `prefers-reduced-motion` — if set, display static, no animation
- No new colours needed — logos are already `grayscale(1)` at 58% opacity

---

### 7. Hero featured motion frame (update hero section)

Replace the four fanned hero screenshot images with a single centred featured frame — one of the motion prototypes playing as a live `<iframe>`, treated as a large device/screen. This becomes the visual proof-of-work in the hero itself.

**Which prototype to feature:** `kova/motion/variance.html` is the recommended choice — it has the most visual density and reads as a sophisticated data product immediately. If it doesn't render well at the target size, fall back to `plio/motion/03-confidence.html`.

**Layout:**
- Remove the four `.hero-img` elements and the `.hero-images` container
- Insert a new `.hero-screen` div between H1 and H2
- The iframe sits inside `.hero-screen`, centered, with a subtle dark device-frame border (`border-radius: 12px`, `box-shadow: 0 32px 80px rgba(0,0,0,0.28)`)
- Size: `clamp(480px, 52vw, 760px)` wide, `aspect-ratio: 16/9`
- `pointer-events: none` on the iframe — it's display only
- `opacity: 0` on load, fades to `1` after 600ms (matches existing hero entrance timing)
- The Three.js particle canvas from Enhancement 1 sits behind it — particles float around the screen frame

**Mobile (≤ 700px):** Hide `.hero-screen` entirely, show nothing in its place — the headline and strapline stack cleanly without it.

**Also update the hero strapline (H2):**
Change from `"Designer who ships exceptional experiences"` to:
```
"Lead designer. Enterprise SaaS,<br>AI systems, and the design<br>infrastructure underneath them."
```
This reflects senior/lead positioning for the hiring audience.

---

### 8. Higgsfield video loops for project cards (implement last)

**This step requires the Higgsfield MCP** (`https://higgsfield.ai/mcp`) to be connected. Do not attempt without it.

**The approach:** Use Higgsfield's image-to-video generation. Screenshot keyframes from the existing motion prototypes first, upload those as reference images, then generate cinematic video *from* the actual UI rather than from text prompts alone. This grounds the output in the real design work.

#### Step 8a — Capture reference screenshots

Use Playwright (headless Chromium, already installed in this environment) to screenshot one representative frame from each motion prototype. Save to `/assets/video/ref/`:

```
kova/motion/variance.html     → /assets/video/ref/kova-ref.png    (capture at t=1500ms)
plio/motion/03-confidence.html → /assets/video/ref/plio-ref.png   (capture at t=2000ms)
arbor/motion/tree.html         → /assets/video/ref/arbor-ref.png  (capture at t=1800ms)
finning/motion/02-detail.html  → /assets/video/ref/finning-ref.png (capture at t=1000ms)
```

Capture at viewport `1280×720`. Wait for the specified delay after page load to catch the animation mid-flow — not the start state.

#### Step 8b — Generate videos via Higgsfield MCP

For each project, upload the reference screenshot via `media_upload`, then call `generate_video` with the reference image and the prompt below. Request 3–4 seconds, loop-friendly (first and last frame should be similar in composition).

**Kova prompt:**
> A polished enterprise analytics dashboard UI animates smoothly on a dark-mode screen. Line charts draw themselves, data cards tick up with numbers, subtle indigo highlights pulse on key metrics. The camera holds steady — no pan, no zoom. Studio lighting, shallow depth of field, shot on a high-resolution monitor. Cinematic product marketing aesthetic. 4 seconds, seamless loop.

**Plio prompt:**
> A clean AI document processing interface on a light-mode screen. Invoice documents appear in a review queue, confidence score bars fill from left to right alongside extracted text fields, a subtle green checkmark confirms each item. Calm, methodical, professional. Studio lighting, monitor shot, no camera movement. Cinematic product demo aesthetic. 4 seconds, seamless loop.

**Arbor prompt:**
> A minimal entity relationship graph assembles on screen — nodes appear one by one, thin lines draw between them forming a hierarchy tree. Dark background, indigo node highlights, white connecting lines. The motion is slow, deliberate, like a living org chart or knowledge graph. No camera movement. Clean, data-forward, enterprise aesthetic. 4 seconds, seamless loop.

**Finning prompt:**
> A heavy-equipment dealer portal UI on a light-mode screen. A product catalogue scrolls smoothly, a finance calculator populates with repayment figures, a clean quote summary appears. Muted industrial tones — slate, warm white. Shot on a large-format monitor, studio lighting, no camera movement. Professional B2B product aesthetic. 4 seconds, seamless loop.

#### Step 8c — Implement in cards

- Save generated videos to `/assets/video/kova-loop.mp4`, `/assets/video/plio-loop.mp4`, `/assets/video/arbor-loop.mp4`, `/assets/video/finning-loop.mp4`
- OnBuy and Design System cards keep static images — no video needed
- In the `.proj-inner` for the four cards above, add `<video autoplay muted loop playsinline>` as a sibling to the existing `<img>`. The `<img>` is the poster/fallback
- Video plays on hover only (`video.play()` / `video.pause()` on mouseenter/mouseleave) — never autoplay on page load
- On hover, cross-fade from `<img>` to `<video>` using opacity transition (0.3s) rather than a hard swap
- Respect `prefers-reduced-motion` — if set, never call `video.play()`

---

## Files to touch (and which to leave alone)

| File | Changes |
|------|---------|
| `index.html` | Step 0 colour vars + all 8 enhancements |
| `about.html` | Step 0 colour vars, nav glass (#2), logo marquee (#6) |
| All case study `*.html` files | Step 0 colour vars only — update `:root` block |
| `assets/site-nav.js` | Scroll class toggle check (#2) |
| `assets/site-nav.css` | Nav glass CSS (#2) |
| `/assets/video/ref/` | Reference screenshots captured by Playwright (#8a) |
| `/assets/video/` | Higgsfield-generated MP4 loops (#8c) |

**Do not touch:** Any file inside `/kova/motion/`, `/plio/motion/`, `/arbor/motion/`, `/finning/motion/`, `/onbuy/motion/`, `/verde/motion/`. Do not touch `_dev/`. Do not alter the theme-switcher picker mechanic, the footer scroll-grow animation, or the hero magnetic parallax — these work correctly.

---

## Code conventions to follow

- No jQuery, no Lodash, no new dependencies beyond Three.js (CDN ES module)
- Keep all new CSS as `<style id="…">` blocks at the bottom of `<head>`, after existing style blocks — do not rewrite existing styles inline
- Keep new JS as `<script type="module">` just before `</body>` — after existing scripts
- Use `const` / `let`, arrow functions, no `var`
- Comment each enhancement block with `/* ENHANCEMENT: [name] */`
- After all changes, manually verify the theme switcher cycles correctly through light → dark → warm and that Three.js particles and the cursor both update colour on each switch
