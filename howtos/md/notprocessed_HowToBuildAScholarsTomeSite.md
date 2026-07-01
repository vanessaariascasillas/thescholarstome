---
type: Guide
author: vanessaariascasillas
author_url: https://github.com/vanessaariascasillas
tags: static site, GitHub Pages, HTML, CSS, Python, markdown
category: Meta / Site Building
difficulty: Beginner
estimated effort: 45 min
version: 1.0
---

# How to Build a Site Like The Scholar's Tome

A guide to setting up your own lightweight, static, no-framework personal archive site — the same pattern used to build this one — and hosting it for free on GitHub Pages.

## Why This Approach

No build step, no framework, no hosting bill. Plain HTML files, one shared stylesheet, and a Python script that turns Markdown into HTML pages when you want a lower-friction way to write content. It's slower to add interactive features later, but it's close to impossible to break and costs nothing to run.

## Step 1: Create the Repository

1. Create a new GitHub repository (public, so GitHub Pages can serve it for free).
2. Clone it locally.
3. Add a `README.md` with the repo's purpose and the eventual live URL (`https://<username>.github.io/<repo-name>/`).

## Step 2: Set Up the Shared Layout

Every page on the site repeats the same structure: a `<header>` with the site title and nav, a `<main>` with the page content, and a `<footer>` with the copyright/license line. Keeping this identical across pages (down to the exact HTML) is what makes the site feel like one coherent thing instead of a pile of unrelated documents.

Root-level page skeleton (`index.html`, `about.html`, etc.):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Page Title | Your Site Name</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <header>
    <h1>Your Site Name</h1>
    <nav>
      <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="about.html">About</a></li>
        <!-- one <li> per top-level section -->
      </ul>
    </nav>
  </header>

  <main>
    <section>
      <h2>Section Heading</h2>
      <p>Content goes here.</p>
    </section>
  </main>

  <footer style="text-align:center; font-size:0.9em; padding:1em 0; border-top:1px solid #ccc;">
    <p>
      &copy; <span id="year"></span> Your Site Name.
      Content on this site is licensed under
      <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noopener noreferrer">
        Creative Commons Attribution-NonCommercial 4.0 International
      </a>.
    </p>
  </footer>

  <script>
    document.getElementById("year").textContent = new Date().getFullYear();
  </script>
</body>
</html>
```

The active page's nav link gets `class="active"` so the visitor can see where they are:

```html
<li><a href="about.html" class="active">About</a></li>
```

Pages that live in a subfolder (like this site's `howtos/`) use the same block but with `../` in front of every href (`../index.html`, `../style.css`, etc.).

## Step 3: Write One Shared Stylesheet

A single `style.css` at the repo root keeps every page visually consistent. Keep it small and generic:

- Body font, background color, base text color
- `header` / `nav` styling, including a `nav a.active` rule so the current tab is visibly highlighted
- `main` with a `max-width` so text doesn't stretch edge-to-edge on wide screens
- `footer` styling
- A couple of reusable utility classes, e.g. a `.resource-list` for the plain link lists used on hub pages

Reference this repo's `style.css` for a working example — it's under 140 lines and handles everything above.

## Step 4: Decide Your Taxonomy Before You Build Hub Pages

Before creating nav tabs, decide what *kinds* of content the site will actually hold. A single catch-all tab (e.g. a generic "How-Tos" page) tends to flatten very different content into one bucket. This site settled on:

- **Learn** — concepts and background theory
- **Guides** — polished, step-by-step instructions for accomplishing a task
- **Journeys** — chronological, first-person logs of a real project (the messy version, not the cleaned-up tutorial)
- **Reference** — cheat sheets, commands, links, configs
- **Archive** — older material (in this case, digitized school notes) kept for the record, not framed as a guide or a lesson

Each category gets its own root-level hub page (`learn.html`, `guides.html`, etc.) with the same header/nav/footer skeleton from Step 2, plus a short intro paragraph explaining what belongs there and one `<ul class="resource-list">` section per topic/category, e.g.:

```html
<section>
    <h3>GIS</h3>
    <ul class="resource-list">
        <li><a href="howtos/HowtoforDotDensMap.html">How to Dot Density and Swipe Two Maps</a></li>
    </ul>
</section>
```

It's fine for a hub page to start out empty with a placeholder line like *"No entries yet."* — add the tab when you're sure of the category, not only once you have content for it.

## Step 5: Write Content Pages by Hand, or Generate Them from Markdown

For a handful of pages, hand-writing HTML is fine. Once you're writing more than a few, converting from Markdown is much less friction. This site uses a small Python script (`scripts/convert_md_to_html.py`) that:

1. Reads every `.md` file in `howtos/md/`
2. Parses a YAML-ish frontmatter block for metadata
3. Converts the Markdown body to HTML with the `markdown` package
4. Wraps it in the shared header/nav/footer template
5. Writes the result to `howtos/<name>.html`

Frontmatter format used by this pipeline:

```markdown
---
type: Guide
author: yourusername
author_url: https://github.com/yourusername
tags: comma, separated, tags
category: Topic Name
difficulty: Beginner
estimated effort: 15 min
version: 1.0
---

# Your Title

Your content, in normal Markdown.
```

The `type` field drives which hub page the nav marks active (`Guide` → `guides.html`, `Journey` → `journeys.html`, etc.) and what shows in the page's `Type:` metadata line — see `TYPE_HUBS` near the top of the script.

Run it from the repo root:

```bash
python scripts/convert_md_to_html.py
```

Run it with no arguments and it picks up every `.md` file in `howtos/md/` — which means anything sitting in that folder gets published the next time you run it. If you have a draft you don't want live yet, keep it out of `howtos/md/`, or pass the specific files you *do* want converted as arguments instead of running it bare.

## Step 6: Add the Metadata Block Styling (Optional but Nice)

Each generated page in this site shows a metadata strip above and below the content (author, reading time, tags, category, created/edited dates, difficulty). This is entirely cosmetic — a `<div class="page-meta-top">` / `<div class="page-meta-bottom">` with a handful of `<span>`s, styled as a light grid in `style.css`. Skip it if you don't want the overhead of filling out frontmatter for every page.

## Step 7: Host on GitHub Pages

1. Push the repo to GitHub.
2. Go to **Settings → Pages**.
3. Under "Build and deployment," set the source to **Deploy from a branch**, branch `main`, folder `/ (root)`.
4. Save. GitHub serves the site at `https://<username>.github.io/<repo-name>/` within a minute or two of each push.

No build step is required because there's nothing to build — the HTML files in the repo *are* the site.

## Step 8: Keep the Nav in Sync

The one recurring maintenance cost of this pattern: every page's `<nav>` block is a literal copy, so adding or renaming a tab means updating it everywhere — every hub page, every content page, and the nav template inside `convert_md_to_html.py` (and any other conversion scripts) so future generated pages match. It's mechanical, not hard, but easy to miss a file if you do it by hand. Search the whole repo for the old link text before considering a rename done.

## Lessons Learned

- Decide the content taxonomy (Learn/Guides/Journeys/etc., or whatever fits your material) before building hub pages — restructuring later means touching every page's nav.
- A shared, literal HTML header/nav/footer block is simple to reason about, but it means "add a nav tab" is a repo-wide find-and-replace, not a one-file change. That's an acceptable tradeoff for a small site; it wouldn't be for a large one.
- Keep placeholders honest: an empty hub page with "no entries yet" is fine; a nav tab that quietly 404s is not.
- Draft content shouldn't sit in the same folder a generator script sweeps by default — a `notprocessed_` prefix is a visual reminder for a human, not something the tooling itself respects, so treat it as a note-to-self rather than a safeguard.
