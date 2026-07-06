#!/usr/bin/env python3
"""Mirror public WordPress page content into a local JSON data file.

The static site keeps a custom homepage, but the other public pages should use
the same body content, images, downloads, and internal links as the official
Ackermann website.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote, unquote, urljoin, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://ackermann-spuelmaschinen.de"
OFFICIAL_UPLOAD_HOSTS = {
    "ackermann-spuelmaschinen.de",
    "www.ackermann-spuelmaschinen.de",
    "test.ackermann-spuelmaschinen.de",
}
OFFICIAL_ASSET_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".svg",
    ".pdf",
}
ASSET_DIR = ROOT / "assets" / "official"
OUT = ROOT / "official_pages.json"
TITLE_OVERRIDES = {
    "/produkte/spuelchemie/": "Spülchemie",
    "/produkte/spuelmaschinen/": "Spülmaschinen",
    "/karriere/": "Karriere",
    "/kontakt/": "Kontakt",
    "/news/": "News",
}

EXTRA_URLS = [
    f"{SITE}/die-andersmacher/",
    f"{SITE}/impressum/",
    f"{SITE}/datenschutz/",
    f"{SITE}/cookie-richtlinie-eu/",
    f"{SITE}/produkte/",
    f"{SITE}/unsere-werte/",
]


def curl(url: str, *, binary: bool = False) -> bytes | str:
    result = subprocess.run(
        [
            "curl",
            "-L",
            "--fail",
            "--silent",
            "--show-error",
            "--connect-timeout",
            "10",
            "--max-time",
            "45",
            url,
        ],
        check=True,
        stdout=subprocess.PIPE,
    )
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8", errors="replace")


def abs_url(url: str) -> str:
    url = deep_unescape(url.strip())
    if not url:
        return url
    if url.startswith("//"):
        return "https:" + url
    return urljoin(SITE + "/", url)


def deep_unescape(value: str) -> str:
    previous = value
    for _ in range(6):
        current = html.unescape(previous)
        if current == previous:
            return current
        previous = current
    return previous


def page_urls() -> list[str]:
    sitemap_index = curl(f"{SITE}/sitemap_index.xml")
    sitemap_urls = re.findall(r"<loc>\s*([^<]+page-sitemap[^<]+)\s*</loc>", sitemap_index)
    if not sitemap_urls:
        sitemap_urls = [f"{SITE}/page-sitemap.xml"]

    urls: list[str] = []
    for sitemap in sitemap_urls:
        xml = curl(sitemap)
        urls.extend(re.findall(r"<loc>\s*([^<]+)\s*</loc>", xml))

    urls.extend(EXTRA_URLS)
    seen: set[str] = set()
    out: list[str] = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc not in OFFICIAL_UPLOAD_HOSTS:
            continue
        normalized = f"{SITE}{parsed.path}"
        if not normalized.endswith("/"):
            normalized += "/"
        if normalized not in seen:
            out.append(normalized)
            seen.add(normalized)
    return out


def text_length(content: str) -> int:
    text = re.sub(r"<[^>]+>", " ", content)
    text = deep_unescape(re.sub(r"\s+", " ", text)).strip()
    return len(text)


def rest_page_content() -> dict[str, str]:
    api_url = (
        f"{SITE}/wp-json/wp/v2/pages?per_page=100"
        "&_fields=link,content"
    )
    try:
        rows = json.loads(curl(api_url))
    except Exception as exc:  # pragma: no cover - operator visibility
        print(f"REST fallback unavailable: {exc}", file=sys.stderr)
        return {}

    pages: dict[str, str] = {}
    for row in rows:
        link = row.get("link", "")
        rendered = row.get("content", {}).get("rendered", "")
        if not link or text_length(rendered) < 80:
            continue
        pages[relative_page_path(link)] = rendered
    return pages


def extract_between(source: str, start: int, end: int) -> str:
    if start == -1 or end == -1 or end <= start:
        return ""
    return source[start:end].strip()


def extract_main(source: str) -> str:
    content_start = source.find('<div id="Content"')
    if content_start == -1:
        content_start = source.find("<main")

    builder_marker = source.find("mfn-builder-content", max(content_start, 0))
    if builder_marker != -1:
        start = source.rfind("<div", 0, builder_marker)
        end = source.find('<section class="section mcb-section the_content', builder_marker)
        if end == -1:
            end = source.find("<footer", builder_marker)
        extracted = extract_between(source, start, end)
        if extracted:
            return extracted

    if content_start != -1:
        end = source.find("<footer", content_start)
        extracted = extract_between(source, content_start, end)
        if extracted:
            return extracted

    body = re.search(r"<body[^>]*>(.*?)</body>", source, re.S | re.I)
    return body.group(1).strip() if body else source


def page_title(source: str, url: str) -> str:
    og_title = re.search(
        r'<meta\s+property=["\']og:title["\']\s+content=["\']([^"\']+)["\']',
        source,
        re.I,
    )
    title = og_title.group(1) if og_title else ""
    if not title:
        title_tag = re.search(r"<title[^>]*>(.*?)</title>", source, re.S | re.I)
        title = title_tag.group(1) if title_tag else ""
    title = html.unescape(re.sub(r"\s+", " ", title)).strip()
    title = re.split(r"\s+[–|-]\s+Ackermann", title)[0].strip()
    if title:
        return title
    slug = urlparse(url).path.strip("/").split("/")[-1] or "Willkommen"
    return slug.replace("-", " ").title()


def page_description(source: str) -> str:
    meta = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
        source,
        re.I,
    )
    return html.unescape(meta.group(1)).strip() if meta else ""


def local_asset_url(remote_url: str) -> str:
    parsed = urlparse(abs_url(remote_url))
    if parsed.netloc not in OFFICIAL_UPLOAD_HOSTS:
        return remote_url
    if not parsed.path.startswith("/wp-content/"):
        return remote_url
    if Path(parsed.path).suffix.lower() not in OFFICIAL_ASSET_EXTENSIONS:
        return remote_url

    # Keep the WordPress upload path intact so duplicate filenames cannot clash.
    rel_path = unquote(parsed.path.lstrip("/"))
    rel_path = "/".join(quote(part) for part in rel_path.split("/"))
    destination = ASSET_DIR / unquote(parsed.path.lstrip("/"))
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not destination.exists() or destination.stat().st_size == 0:
        candidates = [
            f"{SITE}{parsed.path}",
            remote_url,
        ]
        last_error = None
        for candidate in candidates:
            try:
                print(f"  asset {parsed.path}", flush=True)
                data = curl(candidate, binary=True)
                destination.write_bytes(data)
                last_error = None
                break
            except Exception as exc:  # pragma: no cover - operator visibility
                last_error = exc
        if last_error:
            print(f"asset failed: {remote_url} ({last_error})", file=sys.stderr)
            return remote_url

    return f"/assets/official/{rel_path}"


def rewrite_url(url: str) -> str:
    value = deep_unescape(url.strip())
    if not value or value.startswith(("tel:", "mailto:", "#", "javascript:", "data:")):
        return value

    absolute = abs_url(value)
    parsed = urlparse(absolute)
    if parsed.netloc in OFFICIAL_UPLOAD_HOSTS and parsed.path.startswith("/wp-content/"):
        return local_asset_url(absolute)

    if parsed.netloc in OFFICIAL_UPLOAD_HOSTS:
        path = parsed.path or "/"
        if path == "/wp-content/uploads":
            return value
        if parsed.query:
            return f"{path}?{parsed.query}"
        return path

    return value


def clean_content(content: str) -> str:
    content = re.sub(r"<!--.*?-->", "", content, flags=re.S)
    content = re.sub(r"<script\b[^>]*>.*?</script>", "", content, flags=re.S | re.I)
    content = re.sub(r"<style\b[^>]*>.*?</style>", "", content, flags=re.S | re.I)
    content = re.sub(r"<noscript\b[^>]*>.*?</noscript>", "", content, flags=re.S | re.I)

    def iframe_src_repl(match: re.Match[str]) -> str:
        iframe = match.group(0)
        src = re.search(r'\sdata-src-cmplz=(["\'])(.*?)\1', iframe, re.S | re.I)
        if not src:
            return iframe
        real_src = html.escape(src.group(2), quote=True)
        if re.search(r'\ssrc=(["\'])about:blank\1', iframe, re.I):
            return re.sub(r'\ssrc=(["\'])about:blank\1', f' src="{real_src}"', iframe, flags=re.I)
        return iframe

    content = re.sub(r"<iframe\b[^>]*>", iframe_src_repl, content, flags=re.S | re.I)

    # Main src/href is enough locally; dropping srcset avoids dozens of scaled
    # duplicates and keeps the intended image visible.
    content = re.sub(r"\s(?:srcset|data-srcset|sizes)=([\"']).*?\1", "", content, flags=re.S | re.I)

    def url_repl(match: re.Match[str]) -> str:
        quote_char = match.group(1) or ""
        value = match.group(2)
        rewritten = rewrite_url(value)
        return f"url({quote_char}{rewritten}{quote_char})"

    content = re.sub(r"url\(([\"']?)(.*?)(\1)\)", url_repl, content)

    content = re.sub(r"\sdata-(?:mfn|id|uid|desktop|tablet|mobile|position|scroll)[^=]*=(['\"]).*?\1", "", content, flags=re.I | re.S)
    content = re.sub(r"\s+", " ", content)
    content = re.sub(r">\s+<", "><", content)
    return content.strip()


def fix_attribute_rewrites(content: str) -> str:
    # The first attribute rewrite intentionally avoids a full HTML parser, but
    # still needs to preserve attr names exactly and escape values safely.
    attr_pattern = re.compile(r'\b(src|href|data-src|data-placeholder-image)=(["\'])(.*?)(\2)', re.S | re.I)

    def repl(match: re.Match[str]) -> str:
        attr, quote_char, value, _ = match.groups()
        rewritten = rewrite_url(value)
        if attr.lower() == "data-src":
            attr = "src"
        return f'{attr}={quote_char}{html.escape(rewritten, quote=True)}{quote_char}'

    return attr_pattern.sub(repl, content)


def relative_page_path(url: str) -> str:
    path = urlparse(url).path
    if not path.endswith("/"):
        path += "/"
    return path


def main() -> None:
    pages: dict[str, dict[str, str]] = {}
    urls = page_urls()
    rest_content = rest_page_content()
    print(f"found {len(urls)} official urls")
    for url in urls:
        path = relative_page_path(url)
        if path == "/":
            print("skip homepage /")
            continue
        print(f"fetch {path}")
        source = curl(url)
        content = extract_main(source)
        if text_length(content) < 80 and path in rest_content:
            content = rest_content[path]
        content = fix_attribute_rewrites(clean_content(content))
        pages[path] = {
            "title": TITLE_OVERRIDES.get(path, page_title(source, url)),
            "description": page_description(source),
            "content_html": content,
            "source": url,
        }

    OUT.write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} with {len(pages)} pages")


if __name__ == "__main__":
    main()
