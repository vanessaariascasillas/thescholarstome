# The Scholar's Tome

🔗 **Live site:** https://vanessaariascasillas.github.io/thescholarstome/

The Scholar's Tome is an open-access digital archive of resources, guides, and personal notes — a static site with no build step and no framework, hosted for free on GitHub Pages.

It began as a personal collection of research tools and evolved into a public commons for data, learning, and documented experience.

## What's Here

| Section | URL | What it holds |
|---|---|---|
| Home | `index.html` | Landing page and site intro |
| Data | `data.html` | Curated open data sources, maps, and repositories |
| Learn | `learn.html` | Concepts, theory, and background |
| Guides | `guides.html` | Polished, step-by-step how-tos |
| Journeys | `journeys.html` | Chronological, first-person project logs — the confusion and troubleshooting, not just the clean result |
| Reference | `reference.html` | Cheat sheets, commands, links, configs |
| Archive | `archive.html` | Older material kept for the record (e.g. digitized school notes) |
| About | `about.html` | About this project |

## Structure

```
index.html, data.html, learn.html, guides.html,
journeys.html, reference.html, archive.html, about.html   # top-level pages
style.css                                                  # shared stylesheet for every page
howtos/                                                     # individual Guide/Journey/Archive pages
howtos/md/                                                  # Markdown source for the pages above
scripts/                                                    # Markdown → HTML conversion scripts
```

Content pages can be hand-written HTML or authored in Markdown (with a small YAML-style frontmatter block for author/tags/category/type) and converted with `scripts/convert_md_to_html.py`.

## License

Content on this site is licensed under [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/).
