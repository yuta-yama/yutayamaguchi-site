#!/usr/bin/env python3
"""Export Squarespace portfolio pages → Markdown + stills for Astro."""

from __future__ import annotations

import html as html_lib
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "src" / "content" / "projects"
STILLS = ROOT / "public" / "stills"
SITE = "https://www.yutayamaguchi.com"
UA = "Mozilla/5.0 (compatible; yutayamaguchi-migrate/1.0)"

SKIP_SLUGS = {"template", "films"}  # films becomes homepage; template is junk

# Homepage order (from live nav/grid) — used as sort order
HOMEPAGE_ORDER = [
    "dpreel2016",
    "maude",  # may 404 as slug — resolve from homepage if needed
    "thesecolorsdontrun",
    "until-we-could",
    "jazz-abroad",
    "dell-venue-tablets",
    "dell-mike-shinoda",
    "dell-prodeploy-enterprise-suite",
    "mcdonalds-coffee",
    "nurturme",
    "caring-for-cambodia",
    "echosmith-cool-kids",
    "art-can",
    "adobebecky",
    "ut-campaign-for-texas",
    "tda",
    "shangri-la",
    "cloudy-all-day",
    "casimiro",
    "slacker-2011",
    "shiner-bock",
    "snap-kitchen",
    "holyholy",
    "dawn",
    "matsuri",
    "nuiorganics",
    "midnight-motel",
    "amateur",
    "wolf",
    "katrinasson",
]


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8", "replace")


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def strip_tags(s: str) -> str:
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>", "\n\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html_lib.unescape(s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def sitemap_slugs() -> list[str]:
    xml = fetch(f"{SITE}/sitemap.xml")
    locs = re.findall(r"<loc>(.*?)</loc>", xml)
    slugs = []
    for loc in locs:
        path = re.sub(r"^https?://[^/]+", "", loc).strip("/")
        if not path or path in ("contact", "bio"):
            continue
        if path in SKIP_SLUGS:
            continue
        slugs.append(path)
    return slugs


def resolve_maude_slug(homepage_html: str) -> str | None:
    # Find link whose caption/text mentions Maude
    for m in re.finditer(r'href="(/[^"#]+)"[^>]*>[\s\S]{0,200}?Maude', homepage_html, re.I):
        return m.group(1).strip("/")
    for m in re.finditer(r'Maude[\s\S]{0,200}?href="(/[^"#]+)"', homepage_html, re.I):
        return m.group(1).strip("/")
    # gallery item JSON sometimes embeds fullUrl
    m = re.search(r'"fullUrl"\s*:\s*"(/(?:[^"]*maude[^"]*))"', homepage_html, re.I)
    if m:
        return m.group(1).strip("/")
    return None


def extract_images(html: str) -> list[str]:
    urls = re.findall(
        r"https://images\.squarespace-cdn\.com/content/[^\"'\s\\]+",
        html,
    )
    # Prefer original/full size — strip query format params for download base
    cleaned = []
    seen = set()
    for u in urls:
        # Drop tiny formats / favicon-ish
        if "favicon" in u.lower():
            continue
        base = u.split("?")[0]
        # Prefer format=2500w or original when downloading; keep unique bases
        if base in seen:
            continue
        seen.add(base)
        cleaned.append(base)
    return cleaned


def extract_page(html: str, slug: str) -> dict:
    if "couldn't find the page" in html.lower():
        return {"missing": True, "slug": slug}

    title_m = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    title = html_lib.unescape(re.sub(r"<[^>]+>", "", title_m.group(1) if title_m else slug))
    title = title.split("—")[0].split("&mdash;")[0].strip()
    title = re.sub(r"\s+", " ", title)
    # Prefer h1 content when available
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    for h in h1s:
        t = strip_tags(h)
        if t and t.lower() != "yuta yamaguchi":
            title = t
            break

    vimeo = sorted(set(re.findall(r"vimeo[^0-9]{0,40}([0-9]{6,12})", html, re.I)))
    youtube = sorted(
        set(
            re.findall(
                r"(?:youtube\.com/(?:embed/|watch\?v=)|youtu\.be/)([A-Za-z0-9_-]{6,})",
                html,
            )
        )
    )

    # Body: sqs-block-html / entry-content paragraphs
    body_chunks = []
    for block in re.findall(
        r'<div[^>]+class="[^"]*(?:sqs-block-html|sqs-html-content)[^"]*"[^>]*>(.*?)</div>',
        html,
        re.I | re.S,
    ):
        text = strip_tags(block)
        if text and text not in body_chunks and len(text) > 15:
            # skip sitewide boilerplate
            if "Portfolio Website of Films" in text:
                continue
            body_chunks.append(text)

    images = extract_images(html)

    # External links that look like watch/credit links
    ext = []
    for href in re.findall(r'href="(https?://[^"]+)"', html):
        skip = (
            "squarespace",
            "yutayamaguchi",
            "googletagmanager",
            "google-analytics",
            "pagead2",
            "facebook.com",
            "instagram.com/yutay",
            "twitter.com/yutay",
            "linkedin.com/in/yuta",
            "definitions.sqspcdn",
            "fonts.",
        )
        if any(s in href for s in skip):
            continue
        if href not in ext:
            ext.append(href)

    return {
        "missing": False,
        "slug": slug,
        "title": title,
        "vimeo": vimeo,
        "youtube": youtube,
        "body": "\n\n".join(body_chunks).strip(),
        "images": images,
        "links": ext,
    }


def download_stills(slug: str, images: list[str], max_images: int = 24) -> list[str]:
    out_dir = STILLS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    local_paths = []
    for i, url in enumerate(images[:max_images]):
        # Request a large format
        dl = f"{url}?format=2500w"
        ext = ".jpg"
        if ".png" in url.lower():
            ext = ".png"
        elif ".jpeg" in url.lower():
            ext = ".jpg"
        elif ".webp" in url.lower():
            ext = ".webp"
        elif ".gif" in url.lower():
            ext = ".gif"
        name = f"{i+1:02d}{ext}"
        dest = out_dir / name
        if not dest.exists() or dest.stat().st_size < 1000:
            try:
                data = fetch_bytes(dl)
                dest.write_bytes(data)
                time.sleep(0.15)
            except Exception as e:
                print(f"  ! image fail {slug} {i+1}: {e}")
                continue
        local_paths.append(f"/stills/{slug}/{name}")
    return local_paths


def yaml_escape(s: str) -> str:
    if s is None:
        return '""'
    if any(c in s for c in ':#{}[]&*!|>\'"%@`'):
        return json.dumps(s)
    return s


def write_markdown(data: dict, order: int, cover: str | None, stills: list[str]) -> None:
    fm = {
        "title": data["title"],
        "slug": data["slug"],
        "order": order,
        "cover": cover or (stills[0] if stills else ""),
        "stills": stills,
        "vimeo": data["vimeo"][0] if data["vimeo"] else "",
        "youtube": data["youtube"][0] if data["youtube"] else "",
        "links": data["links"][:12],
        "draft": False,
    }
    lines = ["---"]
    lines.append(f"title: {yaml_escape(fm['title'])}")
    lines.append(f"description: \"\"")
    lines.append(f"order: {fm['order']}")
    lines.append(f"cover: {yaml_escape(fm['cover'] or '')}")
    lines.append("stills:")
    if fm["stills"]:
        for s in fm["stills"]:
            lines.append(f"  - {s}")
    else:
        lines.append("  []")
    if fm["vimeo"]:
        lines.append(f"vimeo: \"{fm['vimeo']}\"")
    if fm["youtube"]:
        lines.append(f"youtube: \"{fm['youtube']}\"")
    if fm["links"]:
        lines.append("links:")
        for link in fm["links"]:
            lines.append(f"  - {link}")
    lines.append("---")
    lines.append("")
    if data["body"]:
        lines.append(data["body"])
        lines.append("")
    path = CONTENT / f"{data['slug']}.md"
    path.write_text("\n".join(lines), encoding="utf-8")


def extract_static_page(slug: str) -> tuple[str, str]:
    html = fetch(f"{SITE}/{slug}")
    title = slug.title()
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.S)
    for h in h1s:
        t = strip_tags(h)
        if t and t.lower() != "yuta yamaguchi":
            title = t
            break
    chunks = []
    for block in re.findall(
        r'<div[^>]+class="[^"]*(?:sqs-block-html|sqs-html-content)[^"]*"[^>]*>(.*?)</div>',
        html,
        re.I | re.S,
    ):
        text = strip_tags(block)
        if text and "Portfolio Website of Films" not in text and len(text) > 10:
            chunks.append(text)
    # Contact page has mailto
    mailto = re.findall(r"mailto:([^\"'\s]+)", html)
    body = "\n\n".join(chunks)
    if mailto and slug == "contact":
        email = mailto[0]
        if email not in body:
            body = (body + f"\n\n[{email}](mailto:{email})").strip()
    return title, body


def main() -> None:
    CONTENT.mkdir(parents=True, exist_ok=True)
    STILLS.mkdir(parents=True, exist_ok=True)

    print("Fetching sitemap + homepage…")
    slugs = sitemap_slugs()
    home = fetch(f"{SITE}/")
    maude = resolve_maude_slug(home)
    print("Maude slug:", maude)

    # Build ordered unique slug list
    ordered = []
    for s in HOMEPAGE_ORDER:
        if s == "maude" and maude:
            ordered.append(maude)
        elif s != "maude":
            ordered.append(s)
    for s in slugs:
        if s not in ordered:
            ordered.append(s)
    # de-dupe
    seen = set()
    final = []
    for s in ordered:
        if s in seen or s in SKIP_SLUGS:
            continue
        seen.add(s)
        final.append(s)

    print(f"Projects to export: {len(final)}")
    manifest = []
    for i, slug in enumerate(final):
        print(f"[{i+1}/{len(final)}] {slug}")
        try:
            html = fetch(f"{SITE}/{slug}")
        except urllib.error.HTTPError as e:
            print(f"  HTTP {e.code}")
            continue
        data = extract_page(html, slug)
        if data.get("missing"):
            print("  missing/404")
            continue
        stills = download_stills(slug, data["images"])
        cover = stills[0] if stills else ""
        write_markdown(data, order=i + 1, cover=cover, stills=stills)
        manifest.append(
            {
                "slug": slug,
                "title": data["title"],
                "stills": len(stills),
                "vimeo": data["vimeo"],
                "youtube": data["youtube"],
            }
        )
        time.sleep(0.2)

    # Static pages
    pages_dir = ROOT / "src" / "content" / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    for slug in ("contact", "bio"):
        print(f"Page {slug}")
        title, body = extract_static_page(slug)
        images = extract_images(fetch(f"{SITE}/{slug}"))
        stills = download_stills(f"_page-{slug}", images, max_images=8)
        (pages_dir / f"{slug}.md").write_text(
            "\n".join(
                [
                    "---",
                    f"title: {yaml_escape(title)}",
                    f"cover: {yaml_escape(stills[0] if stills else '')}",
                    "---",
                    "",
                    body,
                    "",
                ]
            ),
            encoding="utf-8",
        )

    (ROOT / "scripts" / "export-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    print("Done.", len(manifest), "projects")


if __name__ == "__main__":
    main()
