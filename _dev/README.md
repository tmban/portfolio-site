# Portfolio repo

Thomas Mbanefo's case-study portfolio. Each project lives in its own subfolder but
all of them follow the same design rules (see "Design preferences" at the bottom).

## Layout

```
portfolio repo/
  README.md                       <- this file (the rules of the system)
  kova/
    index.html                    <- Kova case study (open this)
    motion/                       <- iframe motion graphics + _motion-anim.css
    assets/                       <- Kova research diagrams + UI screenshots
    feature-*.html                <- standalone feature deep-dives
    process-wireframes.html       <- full interactive process wireframes
    _base.css                     <- shared styles used by the feature pages
  arbor/
    arbor.html                    <- Arbor case study (open this)
    motion/                       <- arbor iframe motion graphics + _arbor-anim.css
    assets/                       <- Arbor research diagrams + UI screenshots
    arbor-feature-*.html          <- standalone feature deep-dives
    arbor-process-wireframes.html <- full interactive process wireframes
  verde/                          <- (next project, when it lands)
```

## Run locally

Serve the whole repo from its root so the cross-project sibling links resolve:

```bash
cd "portfolio repo"
python3 -m http.server 8000
```

Open `http://localhost:8000/kova/index.html` or `http://localhost:8000/arbor/arbor.html`.

## Design preferences (carry into every case-study page)

These rules apply to every project page in this folder (`index.html`, `arbor.html`,
and any future case studies like `verde.html`). The project colour and the project
specific imagery vary — everything else stays consistent so it reads as one author.

### Typography hierarchy

- **One font family across all projects.** Bricolage Grotesque (serif) for headings,
  DM Sans (sans) for body, DM Mono (mono) for eyebrows and small labels. Caveat is
  only used inside wireframe boards.
- **Heading sizes are fixed, not by project.** Hero h1 = 600 / 62 / -.035em.
  Section h2 = 600 / 38 / -.03em. r-h sub-titles inside research+discovery = 600 / 22.
  pwf-h (wireframe section panel titles) = 600 / 22. Feature frame-heading = 600 / 30.
  Impact h2 = 600 / 38. Sibling h3 = 600 / 30. Supp-card h-name = 600 / 17.
- **Body lede** = 400 / 17 sans. Body paragraph = 400 / 16 sans.
- **Eyebrows** = 500 / 11px mono, .16em letter-spacing, uppercase, colour: `var(--muted)`.
  Section labels (PROBLEM / RESEARCH / DISCOVERY / FINAL UI / IMPACT) all use this.
- **Frame-label / feature eyebrow** = 500 / 11px mono in `var(--accent)`.

### Headline rules

- **One sentence per title.** Every heading is a single human sentence. No
  period-separated fragments. Subtitles and body copy may run multiple sentences.
- **No em dashes in titles.** Replace with commas or rewrite. Em dashes inside body
  copy are allowed but discouraged.
- **No italic accent words.** Headings are black ink, no `<em>` colour pop. The eyebrow
  above the heading carries the project accent colour; the heading itself does not.
- **No trailing period on feature/frame-headings.** Section-level h2's may end in a
  period when they're statements; feature card headings (frame-heading style) do not.
- **No "The X." stutter eyebrows.** "The problem" → "Problem", "The impact" → "Impact".

### What we don't show

- **No tag/pill chips on the hero.** Category labels ("Data Visualisation", "B2B SaaS",
  "0→1 Intelligence") are removed. The case study sells itself through the work.
- **No "Open the full process" links.** Wireframes live in-page under the Discovery
  section, in tabs. Don't bury them behind a click-through.
- **No version stamps on tabs.** Discovery / Key decision / 4 passes / etc. are not
  displayed in the tab section heads — only the title and supporting paragraph.

### Sibling colours (More case studies cards)

The Arbor card uses `--sib: #1f5b66` (teal). The Kova card uses `--sib: #b85c38`
(orange). The Verde card uses `--sib: #2a7a5a` (green). Each card's `--sib` value
matches the accent colour of the project it links to.

### Wireframe section layout

- Wireframes sit inside the Discovery section, directly under the discovery sec-sub
  paragraph and above the rest of the Discovery r-blocks.
- The wireframes heading itself ("Wireframes" h3) is not rendered. The tab strip
  starts the block.
- Tabs use `font:500 14px sans`, active gets `var(--accent)` border-bottom.
- Per-tab `s-title` matches `r-h`: 600 / 22 serif, no `<em>` colour, no `<br>` breaks.

### Feature pages

- Each supporting-grid card links to a self-contained `*-feature-name.html` page.
- That page uses the figure layout: `.figure { width: 1240px; grid: 1fr 300px }`.
- Three callouts in the right gutter, each with a `.cnum` + `.ctext` (`<b>` lead-in).
- Back-link pill is fixed top-left, but body padding-top must be ≥ 96px so the pill
  doesn't overlap the frame-label eyebrow.

### Floating section nav

- `.sectnav` is `position: fixed; right: 32px; top: 50%`, vertical column of dots,
  `gap: 2px`. The label slides in only on hover or `.active`. Active dot grows to
  11px with the project accent colour.
