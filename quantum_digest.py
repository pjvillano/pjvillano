#!/usr/bin/env python3
"""
quantum_digest.py — Daily digest of publicly available information on quantum
technologies in government and national security contexts.

Usage:
    python3 quantum_digest.py            # Run once, print digest
    python3 quantum_digest.py --save     # Also save digest to a dated file
    python3 quantum_digest.py --schedule # Run every day at 07:00 local time

No API keys required. Sources: Google News RSS, Phys.org, Breaking Defense,
Defense.gov, Federal News Network, ArXiv, and quantum.gov.
"""

import argparse
import html
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console(width=120)

# ---------------------------------------------------------------------------
# Sources
# Each source is a dict with:
#   name     – display name
#   url      – RSS/Atom URL (may include {query} placeholder)
#   category – tag shown in the digest
# ---------------------------------------------------------------------------

GOOGLE_NEWS_QUERIES = [
    ("Quantum Computing Government Policy", "Policy & Governance"),
    ("Quantum National Security Defense", "Defense & Intelligence"),
    ("Quantum Cryptography Government", "Cryptography & PQC"),
    ("Quantum Networking Infrastructure Government", "Infrastructure"),
    ("Quantum Supremacy Military", "Military Technology"),
    ("IonQ IBM quantum government contract", "Industry & Contracts"),
    ("NIST post-quantum cryptography standard", "Cryptography & PQC"),
    ("quantum satellite communication government", "Space & Communications"),
    # China
    ("China quantum computing military national security", "China"),
    ("China PLA quantum technology surveillance", "China"),
    ("China quantum satellite network Micius", "China"),
    ("China post-quantum cryptography standards", "China"),
    # NATO
    ("NATO quantum technology defense alliance", "NATO"),
    ("NATO post-quantum cryptography communication", "NATO"),
    ("NATO quantum sensing intelligence", "NATO"),
    # Russia
    ("Russia quantum computing military defense", "Russia"),
    ("Russia quantum technology national security Rosatom", "Russia"),
    ("Russia quantum cryptography communications", "Russia"),
    # Europe
    ("European Union Quantum Flagship program", "Europe"),
    ("Europe quantum technology national security defense", "Europe"),
    ("UK Germany France quantum computing government", "Europe"),
    ("EuroQCI European quantum communication infrastructure", "Europe"),
]

STATIC_FEEDS = [
    {
        "name": "Breaking Defense",
        "url": "https://breakingdefense.com/feed/",
        "category": "Defense & Intelligence",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "Defense One",
        "url": "https://www.defenseone.com/rss/all/",
        "category": "Defense & Intelligence",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "Federal News Network",
        "url": "https://federalnewsnetwork.com/feed/",
        "category": "Policy & Governance",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "Phys.org – Quantum Physics",
        "url": "https://phys.org/rss-feed/physics-news/quantum-physics/",
        "category": "Science & Research",
        "filter_keywords": ["government", "military", "defense", "national", "security",
                            "agency", "department", "contract", "pentagon", "nato",
                            "DoD", "DARPA", "NSA", "CIA", "DHS", "intelligence",
                            "policy", "federal", "ministry", "strategic"],
    },
    {
        "name": "ArXiv – Quantum Physics (new)",
        # ArXiv exposes per-subject RSS at export.arxiv.org (mirrors, more stable)
        "url": "https://export.arxiv.org/rss/quant-ph",
        "category": "Science & Research",
        "filter_keywords": ["government", "military", "defense", "national security",
                            "cryptograph", "post-quantum", "PQC", "NIST",
                            "quantum key distribution", "QKD", "satellite", "network"],
    },
    {
        "name": "The Quantum Insider",
        "url": "https://thequantuminsider.com/feed/",
        "category": "Industry & Contracts",
        "filter_keywords": ["government", "defense", "military", "national security",
                            "contract", "DoD", "federal", "agency", "policy"],
    },
    {
        "name": "Next Gov (Defense/Tech)",
        "url": "https://www.nextgov.com/rss/all/",
        "category": "Policy & Governance",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "Military Times",
        "url": "https://www.militarytimes.com/arc/outboundfeeds/rss/",
        "category": "Defense & Intelligence",
        "filter_keywords": ["quantum"],
    },
    # --- China ---
    {
        # Nikkei Asia covers China tech extensively and allows RSS
        "name": "Nikkei Asia",
        "url": "https://asia.nikkei.com/rss/feed/nar",
        "category": "China",
        "filter_keywords": ["quantum", "China", "PLA", "Beijing", "Huawei"],
    },
    {
        # The Diplomat covers Asia-Pacific security / tech policy
        "name": "The Diplomat",
        "url": "https://thediplomat.com/feed/",
        "category": "China",
        "filter_keywords": ["quantum", "China", "PLA", "Beijing"],
    },
    # --- NATO ---
    # NATO-specific news is covered by the three Google News queries above.
    # Add static feeds here if your network can reach nato.int or defensenews.com.
    # --- Russia ---
    {
        "name": "TASS (English)",
        "url": "https://tass.com/rss/v2.xml",
        "category": "Russia",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "The Moscow Times – Tech",
        "url": "https://www.themoscowtimes.com/rss/news",
        "category": "Russia",
        "filter_keywords": ["quantum"],
    },
    # --- Europe ---
    {
        "name": "Politico Europe",
        "url": "https://www.politico.eu/feed/",
        "category": "Europe",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "EurActiv",
        "url": "https://www.euractiv.com/feed/",
        "category": "Europe",
        "filter_keywords": ["quantum"],
    },
    {
        "name": "The Quantum Insider – Europe",
        "url": "https://thequantuminsider.com/feed/",
        "category": "Europe",
        "filter_keywords": ["Europe", "EU", "European", "EuroQCI", "Quantum Flagship",
                            "UK", "Germany", "France", "Netherlands", "Finland",
                            "Sweden", "Denmark", "NATO"],
    },
]


# ---------------------------------------------------------------------------
# RSS / Atom parsing (no feedparser — pure stdlib)
# ---------------------------------------------------------------------------

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
    "dc": "http://purl.org/dc/elements/1.1/",
}


def _text(element, tag, ns_prefix=None):
    """Safely get element text."""
    if ns_prefix:
        child = element.find(f"{{{NS[ns_prefix]}}}{tag}")
    else:
        child = element.find(tag)
    if child is not None and child.text:
        return html.unescape(child.text.strip())
    return ""


def _clean(text: str) -> str:
    """Strip HTML tags and collapse whitespace."""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_feed(url: str, timeout: int = 15) -> list[dict]:
    """Fetch an RSS/Atom feed and return a list of article dicts."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; QuantumDigestBot/1.0; "
            "+https://github.com/pjvillano)"
        ),
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml",
    }
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except (URLError, HTTPError, OSError) as exc:
        console.print(f"  [dim red]  ✗ Fetch failed: {url} — {exc}[/]")
        return []

    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        # Some feeds return BOM or broken encoding — try stripping
        try:
            raw = raw.lstrip(b"\xef\xbb\xbf")
            root = ET.fromstring(raw)
        except ET.ParseError as exc:
            console.print(f"  [dim red]  ✗ XML parse error: {url} — {exc}[/]")
            return []

    tag = root.tag.lower()
    if "feed" in tag:
        return _parse_atom(root)
    else:
        return _parse_rss(root)


def _parse_rss(root: ET.Element) -> list[dict]:
    items = []
    for item in root.iter("item"):
        title = _clean(_text(item, "title"))
        link = _text(item, "link") or _text(item, "guid")
        desc = _clean(_text(item, "description"))
        pub = _text(item, "pubDate") or _text(item, "dc:date", "dc")
        if title:
            items.append({"title": title, "link": link, "summary": desc[:300], "published": pub})
    return items


def _parse_atom(root: ET.Element) -> list[dict]:
    items = []
    ns_a = NS["atom"]
    for entry in root.iter(f"{{{ns_a}}}entry"):
        title_el = entry.find(f"{{{ns_a}}}title")
        title = _clean(title_el.text or "") if title_el is not None else ""
        link_el = entry.find(f"{{{ns_a}}}link")
        link = link_el.get("href", "") if link_el is not None else ""
        summary_el = entry.find(f"{{{ns_a}}}summary") or entry.find(f"{{{ns_a}}}content")
        summary = _clean(summary_el.text or "") if summary_el is not None else ""
        pub_el = entry.find(f"{{{ns_a}}}published") or entry.find(f"{{{ns_a}}}updated")
        pub = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
        if title:
            items.append({"title": title, "link": link, "summary": summary[:300], "published": pub})
    return items


# ---------------------------------------------------------------------------
# Google News RSS
# ---------------------------------------------------------------------------

GNEWS_BASE = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"


def fetch_google_news(query: str) -> list[dict]:
    url = GNEWS_BASE.format(query=quote_plus(query))
    return fetch_feed(url)


# ---------------------------------------------------------------------------
# Keyword filtering
# ---------------------------------------------------------------------------

def passes_filter(article: dict, keywords: list[str]) -> bool:
    """Return True if any keyword appears in the title or summary (case-insensitive)."""
    haystack = (article["title"] + " " + article["summary"]).lower()
    return any(kw.lower() in haystack for kw in keywords)


def is_quantum_relevant(article: dict) -> bool:
    """Minimal quantum relevance check (for Google News results)."""
    return passes_filter(article, ["quantum"])


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _normalise_title(title: str) -> str:
    return re.sub(r"\W+", " ", title.lower()).strip()


def deduplicate(articles: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out = []
    for a in articles:
        key = _normalise_title(a["title"])[:80]
        if key not in seen:
            seen.add(key)
            out.append(a)
    return out


# ---------------------------------------------------------------------------
# Digest assembly
# ---------------------------------------------------------------------------

CATEGORY_ORDER = [
    "Policy & Governance",
    "Defense & Intelligence",
    "Cryptography & PQC",
    "Infrastructure",
    "Military Technology",
    "Industry & Contracts",
    "Space & Communications",
    "Science & Research",
    "China",
    "NATO",
    "Russia",
    "Europe",
]


def collect_all() -> dict[str, list[dict]]:
    """Fetch all sources and return articles bucketed by category."""
    by_category: dict[str, list[dict]] = {c: [] for c in CATEGORY_ORDER}

    # --- Google News ---
    console.print("[bold cyan]Fetching Google News...[/]")
    for query, category in GOOGLE_NEWS_QUERIES:
        console.print(f"  [dim]→ {query}[/]")
        articles = fetch_google_news(query)
        filtered = [a for a in articles if is_quantum_relevant(a)]
        by_category.setdefault(category, []).extend(filtered)
        time.sleep(0.4)  # polite delay

    # --- Static feeds ---
    console.print("[bold cyan]Fetching curated feeds...[/]")
    for src in STATIC_FEEDS:
        console.print(f"  [dim]→ {src['name']}[/]")
        articles = fetch_feed(src["url"])
        keywords = src.get("filter_keywords", ["quantum"])
        filtered = [a for a in articles if passes_filter(a, keywords)]
        by_category.setdefault(src["category"], []).extend(filtered)
        time.sleep(0.4)

    # Deduplicate within each category, cap at 15 items per category
    for cat in by_category:
        by_category[cat] = deduplicate(by_category[cat])[:15]

    return by_category


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    "Policy & Governance":    "bright_blue",
    "Defense & Intelligence": "bright_red",
    "Cryptography & PQC":     "bright_green",
    "Infrastructure":         "bright_yellow",
    "Military Technology":    "red",
    "Industry & Contracts":   "bright_magenta",
    "Space & Communications": "bright_cyan",
    "Science & Research":     "cyan",
    "China":                  "red1",
    "NATO":                   "deep_sky_blue1",
    "Russia":                 "dark_orange",
    "Europe":                 "steel_blue1",
}


def render_digest(by_category: dict[str, list[dict]], save_path: str | None = None):
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%A, %B %-d, %Y")
    time_str = now.strftime("%H:%M UTC")

    lines_plain: list[str] = []  # for file output

    def plain(text: str):
        if save_path:
            lines_plain.append(_clean(text))

    console.print()
    console.print(Panel(
        f"[bold white]Quantum Technologies: Government & National Security[/]\n"
        f"[dim]{date_str}  ·  {time_str}[/]",
        border_style="bright_blue",
        padding=(1, 4),
    ))
    plain(f"QUANTUM TECHNOLOGIES: GOVERNMENT & NATIONAL SECURITY")
    plain(f"{date_str}  ·  {time_str}")
    plain("")

    total = 0
    for category in CATEGORY_ORDER:
        articles = by_category.get(category, [])
        if not articles:
            continue

        color = CATEGORY_COLORS.get(category, "white")
        console.print(Rule(f"[bold {color}]{category}[/]", style=color))
        plain(f"\n{'='*60}")
        plain(f"  {category.upper()}")
        plain(f"{'='*60}")

        for i, art in enumerate(articles, 1):
            total += 1
            title = art["title"]
            link = art["link"]
            summary = art["summary"]
            pub = art["published"]

            # Title line
            console.print(f"  [bold]{i}. {title}[/]")
            plain(f"\n  {i}. {title}")

            # Summary (truncated at 180 chars)
            if summary:
                short = summary[:180] + ("…" if len(summary) > 180 else "")
                console.print(f"     [dim]{short}[/]")
                plain(f"     {short}")

            # Link + date
            meta_parts = []
            if pub:
                meta_parts.append(pub[:25])
            if link:
                console.print(f"     [link={link}][blue]{link}[/][/]")
                plain(f"     {link}")
            if meta_parts:
                console.print(f"     [dim italic]{' · '.join(meta_parts)}[/]")
                plain(f"     {' · '.join(meta_parts)}")

            console.print()

    # Footer
    console.print(Rule(style="bright_blue"))
    console.print(f"  [dim]{total} articles collected from {len(STATIC_FEEDS) + len(GOOGLE_NEWS_QUERIES)} sources[/]")
    console.print(f"  [dim]Generated {now.strftime('%Y-%m-%dT%H:%M:%SZ')}[/]")
    console.print()

    if save_path and lines_plain:
        with open(save_path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines_plain))
        console.print(f"[green]Digest saved to:[/] {save_path}")


# ---------------------------------------------------------------------------
# Scheduling
# ---------------------------------------------------------------------------

def run_once(save: bool):
    by_category = collect_all()
    save_path = None
    if save:
        date_tag = datetime.now().strftime("%Y-%m-%d")
        save_path = f"quantum_digest_{date_tag}.txt"
    render_digest(by_category, save_path=save_path)


def run_scheduled(run_time: str = "07:00", save: bool = True):
    """Block forever, running the digest once per day at run_time (HH:MM local)."""
    try:
        import schedule
    except ImportError:
        console.print("[red]Install schedule: pip install schedule[/]")
        sys.exit(1)

    console.print(f"[bold green]Scheduler active — digest will run daily at {run_time} local time.[/]")
    console.print("[dim]Press Ctrl+C to stop.[/]\n")

    def _job():
        console.print(f"\n[bold]Running scheduled digest — {datetime.now().strftime('%Y-%m-%d %H:%M')}[/]")
        run_once(save=save)

    schedule.every().day.at(run_time).do(_job)

    # Run immediately on first start so you don't wait until tomorrow
    _job()

    while True:
        schedule.run_pending()
        time.sleep(30)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Daily digest: quantum technologies in government & national security."
    )
    parser.add_argument(
        "--save", action="store_true",
        help="Save the digest to a dated .txt file in the current directory.",
    )
    parser.add_argument(
        "--schedule", action="store_true",
        help="Run as a daily scheduler (default 07:00 local). Implies --save.",
    )
    parser.add_argument(
        "--time", default="07:00", metavar="HH:MM",
        help="Time for daily scheduled run (24h local, default 07:00).",
    )
    args = parser.parse_args()

    if args.schedule:
        run_scheduled(run_time=args.time, save=True)
    else:
        run_once(save=args.save)


if __name__ == "__main__":
    main()
