# Website for the documentation: https://pandoc.org/installing.html

import argparse
import sys
import re
import html
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
import shutil
import markdown

# ----------------------------
# Configuration
# ----------------------------
MD_DIR = Path(".")         # Current folder with command execution base path
CSS_FILE = "style.css"     # CSS file name at repo root
SITE_TITLE = "The Scholar’s Tome"
AUTHOR = "vanessaariascasillas"
GITHUB_PROFILE = "https://github.com/vanessaariascasillas"

# ----------------------------
# Helpers
# ----------------------------

def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if text.startswith("---\n"):
        end_block = text.find("\n---", 4)
        if end_block != -1:
            block_text = text[4:end_block].strip()
            body = text[end_block + 4 :].lstrip("\n")
            meta: dict[str, str] = {}
            for line in block_text.splitlines():
                if not line.strip() or line.strip().startswith("#"):
                    continue
                if ":" in line:
                    key, value = line.split(":", 1)
                    normalized = key.strip().lower().replace(" ", "_")
                    meta[normalized] = value.strip()
            return meta, body
    return {}, text


def format_author(author_value: str, author_url: str | None = None) -> str:
    author_value = author_value.strip()
    if author_url:
        return f"<a href=\"{html.escape(author_url)}\" target=\"_blank\" rel=\"noopener noreferrer\">{html.escape(author_value)}</a>"
    if re.match(r"^[A-Za-z0-9_-]+$", author_value):
        return f"<a href=\"https://github.com/{html.escape(author_value)}\" target=\"_blank\" rel=\"noopener noreferrer\">{html.escape(author_value)}</a>"
    return html.escape(author_value)


def get_file_times(path: Path) -> tuple[str, str]:
    stats = path.stat()
    created = stats.st_ctime
    modified = stats.st_mtime
    created_str = datetime.fromtimestamp(created).strftime("%Y-%m-%d")
    modified_str = datetime.fromtimestamp(modified).strftime("%Y-%m-%d")
    return created_str, modified_str


def estimate_reading_time(text: str) -> str:
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


# ----------------------------
# Parse arguments
# ----------------------------
parser = argparse.ArgumentParser(
    description="Convert Markdown files to how-to HTML pages and add metadata like created/updated dates."
)
parser.add_argument(
    "md_files",
    nargs="*",
    help="Paths to Markdown files to convert. If omitted, all *.md files in the current folder or current folder/md are processed."
)
args = parser.parse_args()

if args.md_files:
    md_files = [Path(file) for file in args.md_files]
    missing = [str(f) for f in md_files if not f.is_file()]
    if missing:
        print("Markdown files not found:")
        for missing_file in missing:
            print(f"  - {missing_file}")
        sys.exit(1)
else:
    candidate_dir = Path("howtos") / "md" if (Path("howtos") / "md").is_dir() else Path("md") if Path("md").is_dir() else Path(".")
    md_files = sorted(candidate_dir.glob("*.md"))

if not md_files:
    print("No Markdown files found to convert.")
    sys.exit(0)

print(f"Markdown files found: {[f.as_posix() for f in md_files]}")

# ----------------------------
# Convert Markdown → HTML using Python markdown
# ----------------------------
converted_htmls = []
for md_file in md_files:
    output_dir = md_file.parent.parent if md_file.parent.name == "md" else md_file.parent
    html_file = output_dir / f"{md_file.stem}.html"
    converted_htmls.append(html_file)
    print(f"Converting {md_file.as_posix()} → {html_file.as_posix()}")

    with open(md_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    frontmatter, md_text = parse_frontmatter(md_text)
    created_date, updated_date = get_file_times(md_file)
    reading_time = estimate_reading_time(md_text)
    author = frontmatter.get("author", AUTHOR)
    author_url = frontmatter.get("author_url", GITHUB_PROFILE if author == AUTHOR else None)
    author_html = format_author(author, author_url)
    tags = frontmatter.get("tags", "Not specified")
    category = frontmatter.get("category", "Not specified")
    difficulty = frontmatter.get("difficulty", "Not specified")
    estimated_effort = frontmatter.get("estimated_effort", frontmatter.get("estimated effort", "Not specified"))
    version = frontmatter.get("version", "Not specified")
    meta_block_top = f"""
<div class=\"page-meta-top\">
  <span><strong>Type:</strong> How-To</span>
  <span><strong>Author:</strong> {author_html}</span>
  <span><strong>Reading time:</strong> {reading_time}</span>
  <span><strong>Tags:</strong> {tags}</span>
  <span><strong>Category:</strong> {category}</span>
</div>
"""
    meta_block_bottom = f"""
<div class=\"page-meta-bottom\">
  <span><strong>Created:</strong> {created_date}</span>
  <span><strong>Last edited:</strong> {updated_date}</span>
  <span><strong>Difficulty:</strong> {difficulty}</span>
  <span><strong>Estimated effort:</strong> {estimated_effort}</span>
  <span><strong>Version:</strong> {version}</span>
</div>
"""

    html_body = markdown.markdown(
        md_text,
        extensions=["extra", "tables", "fenced_code", "toc"],
        output_format="html5"
    )

    css_href = f"../{CSS_FILE}" if output_dir != Path(".") else CSS_FILE
    html_content = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\"/>
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"/>
<title>{md_file.stem} | {SITE_TITLE}</title>
<link rel=\"stylesheet\" href=\"{css_href}\"/>
</head>
<body>
<header>
    <h1>{SITE_TITLE}</h1>
    <nav>
        <ul>
            <li><a href=\"../index.html\">Home</a></li>
            <li><a href=\"../data.html\">Data</a></li>
            <li><a href=\"../howtos.html\" class=\"active\">How-Tos</a></li>
            <li><a href=\"../about.html\">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <section>
{meta_block_top}
{html_body}
{meta_block_bottom}
    </section>
</main>

<footer style=\"text-align:center; font-size:0.9em; padding:1em 0; border-top:1px solid #ccc;\">
  <p>
    &copy; <span id=\"year\"></span> {SITE_TITLE}.
    Content on this site is licensed under
    <a href=\"https://creativecommons.org/licenses/by-nc/4.0/\" target=\"_blank\" rel=\"noopener noreferrer\">
      Creative Commons Attribution-NonCommercial 4.0 International
    </a>.
  </p>
</footer>
<script>
document.getElementById(\"year\").textContent = new Date().getFullYear();
</script>
</body>
</html>"""

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

# ----------------------------
# Fix <img> paths in converted HTML files
# ----------------------------
for html_file in converted_htmls:
    if not html_file.exists():
        continue
    print(f"Fixing image paths in {html_file.name}...")
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for img in soup.find_all("img"):
        src = img.get("src", "")
        if src.startswith("howtos/"):
            img["src"] = src[len("howtos/"):]
            print(f"  Updated src: {src} -> {img['src']}")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

# ----------------------------
# Move processed Markdown files into "md" folder if needed
# ----------------------------
for md_file in md_files:
    if md_file.parent.name == "md":
        continue
    md_folder = md_file.parent / "md"
    md_folder.mkdir(exist_ok=True)
    dest = md_folder / md_file.name
    if md_file.resolve() != dest.resolve():
        shutil.move(str(md_file), str(dest))
        print(f"Moved {md_file.name} → {md_folder}/")

print("✅ Conversion complete. Processed Markdown files are in the md/ folder.")
