"""Rebuild the README, the folder pages and the star map from the solution files.

Run from anywhere:

    python scripts/build.py

A problem counts as solved when its folder holds a file named
<leetcode-number, 4 digits>_<anything>.py, e.g. 01-arrays-hashing/0217_contains_duplicate.py.
Nothing here needs editing by hand after a new solution is added.
"""

import math
import random
from html import escape
from pathlib import Path

from problems import CATEGORIES, SHORT_NAMES

ROOT = Path(__file__).resolve().parent.parent

# One palette for both graphics: a printed star atlas.
FIELD = "#17264d"      # the night-blue sheet
GRID = "#2c3f74"       # coordinate lines, borders
DIM = "#6577a8"        # unlit stars and their lines
PALE = "#c5cfe8"       # secondary text
CREAM = "#f6ecd0"      # lit stars, main text
GOLD = "#e9c46a"       # a finished constellation
SERIF = "Georgia, 'Times New Roman', 'DejaVu Serif', serif"

# Like a real atlas, a bigger dot is a brighter star. Here: a harder problem.
RADIUS = {"Easy": 2.3, "Medium": 3.5, "Hard": 5.0}


def load():
    """Return the categories with folder names and solved files filled in."""
    cats = []
    for i, (name, slug, problems) in enumerate(CATEGORIES, 1):
        folder = f"{i:02d}-{slug}"
        rows = []
        for num, title, diff in problems:
            hits = sorted((ROOT / folder).glob(f"{num:04d}_*.py"))
            rows.append({"num": num, "title": title, "diff": diff,
                         "file": hits[0].name if hits else None})
        cats.append({"name": name, "folder": folder, "rows": rows,
                     "done": sum(1 for r in rows if r["file"])})
    return cats


# ---------------------------------------------------------------- graphics

def banner_svg():
    w, h = 880, 210
    rng = random.Random("neetcode-150")
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="NeetCode 150. 150 problems, 18 patterns, one Python solution at a time.">',
        "<style>"
        ".tw{animation:tw 5s ease-in-out infinite}"
        ".tw.b{animation-delay:1.7s}.tw.c{animation-delay:3.1s}"
        "@keyframes tw{0%,100%{opacity:.95}50%{opacity:.25}}"
        "@media (prefers-reduced-motion:reduce){.tw{animation:none}}"
        "</style>",
        f'<defs><clipPath id="sheet"><rect width="{w}" height="{h}" rx="14"/></clipPath>'
        f'<radialGradient id="halo"><stop offset="0" stop-color="{CREAM}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient></defs>',
        f'<g clip-path="url(#sheet)"><rect width="{w}" height="{h}" fill="{FIELD}"/>',
    ]

    # Coordinate lines of a polar chart whose pole sits above the top-right corner.
    px, py = 770, -330
    out.append(f'<g fill="none" stroke="{GRID}" stroke-width="1">')
    for r in range(380, 1000, 62):
        out.append(f'<circle cx="{px}" cy="{py}" r="{r}"/>')
    for deg in range(20, 170, 10):
        a = math.radians(deg)
        out.append(f'<line x1="{px + 380 * math.cos(a):.1f}" y1="{py + 380 * math.sin(a):.1f}" '
                   f'x2="{px + 1300 * math.cos(a):.1f}" y2="{py + 1300 * math.sin(a):.1f}"/>')
    out.append("</g>")

    # Faint field stars, kept clear of the title.
    twinkle = ["tw", "tw b", "tw c"]
    for _ in range(70):
        x, y = rng.uniform(10, w - 10), rng.uniform(10, h - 10)
        if 30 < x < 590 and 50 < y < 160:
            continue
        r = rng.choice([0.6, 0.6, 0.8, 0.8, 1.0, 1.3])
        cls = f' class="{twinkle.pop()}"' if twinkle and r >= 1.0 else ""
        out.append(f'<circle{cls} cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{CREAM}" opacity="{rng.uniform(.35, .8):.2f}"/>')

    # One constellation, drawn as a binary tree.
    tree = [(722, 44, 5.0), (672, 86, 3.5), (780, 80, 3.5),
            (642, 140, 2.3), (700, 150, 3.5), (752, 132, 2.3), (826, 126, 3.5)]
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)]
    for a, b in edges:
        out.append(f'<line x1="{tree[a][0]}" y1="{tree[a][1]}" x2="{tree[b][0]}" y2="{tree[b][1]}" '
                   f'stroke="{CREAM}" stroke-width="1" opacity=".55"/>')
    for x, y, r in tree:
        out.append(f'<circle cx="{x}" cy="{y}" r="{r * 3.2:.1f}" fill="url(#halo)"/>')
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/>')

    out.append(f'<text x="48" y="104" font-family="{SERIF}" font-size="56" font-weight="bold" '
               f'fill="{CREAM}" letter-spacing=".5">NeetCode 150</text>')
    out.append(f'<text x="50" y="140" font-family="{SERIF}" font-size="18" font-style="italic" '
               f'fill="{PALE}">150 problems, 18 patterns, one Python solution at a time.</text>')
    out.append(f'</g><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{GRID}"/></svg>')
    return "\n".join(out) + "\n"


def chain(n, seed, width=108):
    """Lay n stars out as a wandering chain inside a width x 70 box.

    Up to 8 stars form one line. More than 8 run out along the top and come
    back along the bottom, so the stars never crowd each other.
    """
    rng = random.Random(seed)

    def row(k, cy, amp, reverse=False):
        span = min(width, (k - 1) * 22)
        x0 = (width - span) / 2
        phase, freq = rng.uniform(0, 6.28), rng.uniform(0.9, 1.6)
        pts = []
        for i in range(k):
            x = x0 + (span * i / (k - 1) if k > 1 else 0) + rng.uniform(-2.5, 2.5)
            y = cy + amp * math.sin(phase + i * freq) + rng.uniform(-3, 3)
            pts.append((x, y))
        return pts[::-1] if reverse else pts

    if n <= 8:
        return row(n, 35, 17)
    top = math.ceil(n / 2)
    return row(top, 18, 8) + row(n - top, 55, 8, reverse=True)


def star_map_svg(cats):
    w, cols, cell_w, cell_h, top = 880, 6, 140, 146, 104
    h = top + cell_h * math.ceil(len(cats) / cols) + 10
    solved = sum(c["done"] for c in cats)
    total = sum(len(c["rows"]) for c in cats)
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="Star map: {solved} of {total} problems solved.">',
        f'<defs><radialGradient id="halo"><stop offset="0" stop-color="{CREAM}" stop-opacity=".4"/>'
        f'<stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient></defs>',
        f'<rect width="{w}" height="{h}" rx="14" fill="{FIELD}"/>',
        f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{GRID}"/>',
        f'<text x="36" y="52" font-family="{SERIF}" font-size="26" fill="{CREAM}">'
        f'{solved} of {total} stars lit</text>',
        f'<text x="36" y="76" font-family="{SERIF}" font-size="13.5" font-style="italic" fill="{PALE}">'
        f'Each star is one problem. Solving it lights it up.</text>',
    ]

    # Legend: size is difficulty, fill is solved or not.
    lx, ly = 596, 46
    out.append(f'<g font-family="{SERIF}" font-size="13" fill="{PALE}">')
    for label, dx in (("Easy", 0), ("Medium", 62), ("Hard", 146)):
        r = RADIUS[label]
        out.append(f'<circle cx="{lx + dx}" cy="{ly - 4}" r="{r}" fill="{CREAM}"/>')
        out.append(f'<text x="{lx + dx + 10}" y="{ly}">{label.lower()}</text>')
    out.append(f'<circle cx="{lx}" cy="{ly + 20}" r="3.5" fill="{CREAM}"/>')
    out.append(f'<text x="{lx + 10}" y="{ly + 24}">solved</text>')
    out.append(f'<circle cx="{lx + 62}" cy="{ly + 20}" r="3.5" fill="{FIELD}" stroke="{DIM}" stroke-width="1.2"/>')
    out.append(f'<text x="{lx + 72}" y="{ly + 24}">not yet</text>')
    out.append("</g>")
    out.append(f'<line x1="36" y1="92" x2="{w - 36}" y2="92" stroke="{GRID}"/>')

    for i, c in enumerate(cats):
        ox = 20 + (i % cols) * cell_w + 16
        oy = top + (i // cols) * cell_h + 12
        rows = c["rows"]
        pts = [(ox + x, oy + y) for x, y in chain(len(rows), c["folder"])]
        complete = c["done"] == len(rows)
        lit_color = GOLD if complete else CREAM

        for (x1, y1), (x2, y2), a, b in zip(pts, pts[1:], rows, rows[1:]):
            lit = a["file"] and b["file"]
            out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                       f'stroke="{lit_color if lit else DIM}" stroke-width="1" opacity="{".8" if lit else ".5"}"/>')
        for (x, y), row in zip(pts, rows):
            r = RADIUS[row["diff"]]
            if row["file"]:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 3:.1f}" fill="url(#halo)"/>')
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{lit_color}"/>')
            else:
                out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{FIELD}" stroke="{DIM}" stroke-width="1.2"/>')

        cx = 20 + (i % cols) * cell_w + cell_w / 2
        name = escape(SHORT_NAMES.get(c["name"], c["name"]))
        out.append(f'<text x="{cx}" y="{oy + 96}" text-anchor="middle" font-family="{SERIF}" font-size="13" '
                   f'font-style="italic" fill="{GOLD if complete else CREAM}">{name}</text>')
        out.append(f'<text x="{cx}" y="{oy + 114}" text-anchor="middle" font-family="{SERIF}" font-size="12.5" '
                   f'fill="{GOLD if complete else PALE}">{c["done"]} of {len(rows)}</text>')

    out.append("</svg>")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- markdown

def table(rows, link_prefix=""):
    lines = ["| | # | Problem | Difficulty |", "|:-:|--:|---|---|"]
    for r in rows:
        title = f'[{r["title"]}]({link_prefix}{r["file"]})' if r["file"] else r["title"]
        lines.append(f'| {"★" if r["file"] else "☆"} | {r["num"]} | {title} | {r["diff"]} |')
    return "\n".join(lines)


EXAMPLE = '''"""
LeetCode 1. Two Sum
https://leetcode.com/problems/two-sum/
Difficulty: Easy

Intuition:
    For every number, I need its partner: target - n.
    Searching the list again for it is slow.
    So I remember every number I've seen in a dict (number -> index).
    If the partner is already in the dict, that's the pair.

Complexity:
    Time:  O(n)  - one pass
    Space: O(n)  - the dict
"""'''


def readme(cats):
    solved = sum(c["done"] for c in cats)
    total = sum(len(c["rows"]) for c in cats)
    by_diff = []
    for d in ("Easy", "Medium", "Hard"):
        rows = [r for c in cats for r in c["rows"] if r["diff"] == d]
        by_diff.append(f'{d} {sum(1 for r in rows if r["file"])} of {len(rows)}')

    out = [
        "<!-- Generated by scripts/build.py. Edit that file, not this one. -->",
        "",
        '<p align="center">',
        '  <img src="assets/banner.svg" width="100%" alt="NeetCode 150. 150 problems, 18 patterns, one Python solution at a time.">',
        "</p>",
        "",
        "My Python solutions to the [NeetCode 150](https://neetcode.io/practice). "
        "Every solution starts with a short note, in plain words, on why it works.",
        "",
        "## The star map",
        "",
        "Every problem is a star, and every category is a constellation. "
        "A solved problem lights its star. A bigger star is a harder problem.",
        "",
        '<p align="center">',
        f'  <img src="assets/star-map.svg" width="100%" alt="Star map: {solved} of {total} problems solved. {", ".join(by_diff)}.">',
        "</p>",
        "",
        f'**{solved} of {total} solved.** {", ".join(by_diff)}.',
        "",
        "## What a solution looks like",
        "",
        "Each file opens with the idea behind the solution and its cost, then the code, then a few tests. "
        "Run any file on its own to check it:",
        "",
        "```bash",
        "python 01-arrays-hashing/0001_two_sum.py",
        "```",
        "",
        "```python",
        EXAMPLE,
        "```",
        "",
        "## The problems",
        "",
        "★ is solved and links to the solution. ☆ is still dark.",
        "",
    ]
    for c in cats:
        n = len(c["rows"])
        mark = " ★" if c["done"] == n else ""
        out += [
            "<details>",
            f'<summary><b>{escape(c["name"])}</b> &nbsp;·&nbsp; {c["done"]} of {n}{mark}</summary>',
            "",
            f'Folder: [`{c["folder"]}`]({c["folder"]}/)',
            "",
            table(c["rows"], link_prefix=c["folder"] + "/"),
            "",
            "</details>",
            "",
        ]
    out += [
        "## How the repo is laid out",
        "",
        "```",
        "01-arrays-hashing/        one folder per category, in NeetCode's roadmap order",
        "    0001_two_sum.py       one file per problem: <LeetCode number>_<title>.py",
        "assets/                   the banner and the star map",
        "scripts/build.py          redraws the star map and rewrites the READMEs",
        "TEMPLATE.py               the starting point for a new solution",
        "```",
        "",
        "Nothing is ticked by hand. After adding a solution, run `python scripts/build.py` "
        "and the star map, this page and the folder pages update themselves.",
        "",
    ]
    return "\n".join(out)


def folder_readme(c):
    n = len(c["rows"])
    done = "All of them are solved." if c["done"] == n else f'{c["done"]} of {n} solved.'
    return "\n".join([
        "<!-- Generated by scripts/build.py. Edit that file, not this one. -->",
        "",
        f'# {c["name"]}',
        "",
        f'{done} ★ is solved and links to the solution. ☆ is still dark.',
        "",
        table(c["rows"]),
        "",
        "[Back to the star map](../README.md)",
        "",
    ])


def main():
    cats = load()
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "banner.svg").write_text(banner_svg(), encoding="utf-8")
    (ROOT / "assets" / "star-map.svg").write_text(star_map_svg(cats), encoding="utf-8")
    (ROOT / "README.md").write_text(readme(cats), encoding="utf-8")
    for c in cats:
        (ROOT / c["folder"]).mkdir(exist_ok=True)
        (ROOT / c["folder"] / "README.md").write_text(folder_readme(c), encoding="utf-8")
    print(f'{sum(c["done"] for c in cats)} of {sum(len(c["rows"]) for c in cats)} solved')


if __name__ == "__main__":
    main()
