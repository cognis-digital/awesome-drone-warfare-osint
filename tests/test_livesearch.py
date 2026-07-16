"""Tests for the keyless live-search / feed-ingestion module.

Network access is never used: ``livesearch._get`` is monkeypatched to return
canned bytes so the RSS/Atom parsing, DuckDuckGo scrape, recency filtering and
de-duplication logic can be exercised deterministically.
"""

from __future__ import annotations

import urllib.parse
from datetime import datetime, timezone

import pytest

import livesearch as ls


RSS_SAMPLE = b"""<?xml version="1.0"?>
<rss version="2.0"><channel>
  <title>Example Feed</title>
  <item>
    <title>First &amp; foremost</title>
    <link>https://example.com/a</link>
    <pubDate>Mon, 06 Jul 2026 12:00:00 GMT</pubDate>
  </item>
  <item>
    <title>Second story</title>
    <link>https://example.com/b</link>
    <pubDate>Tue, 07 Jul 2026 08:30:00 +0000</pubDate>
  </item>
</channel></rss>"""

ATOM_SAMPLE = b"""<?xml version="1.0"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Atom Example</title>
  <entry>
    <title>Atom item</title>
    <link href="https://atom.example/x"/>
    <updated>2026-07-05T09:00:00Z</updated>
  </entry>
</feed>"""


# --------------------------------------------------------------------------- #
# URL construction + tiny helpers
# --------------------------------------------------------------------------- #
def test_google_news_rss_encodes_query_and_when():
    url = ls.google_news_rss("iran drone parts", when="7d")
    parsed = urllib.parse.urlparse(url)
    qs = urllib.parse.parse_qs(parsed.query)
    assert parsed.netloc == "news.google.com"
    assert qs["q"] == ["iran drone parts when:7d"]
    assert qs["hl"] == ["en-US"]


def test_google_news_rss_when_blank_omits_suffix():
    url = ls.google_news_rss("shahed", when="")
    qs = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    assert qs["q"] == ["shahed"]


def test_tag_strips_namespace():
    class E:
        tag = "{http://www.w3.org/2005/Atom}entry"
    assert ls._tag(E()) == "entry"


@pytest.mark.parametrize(
    "value",
    [
        "Mon, 06 Jul 2026 12:00:00 GMT",   # RFC-822
        "2026-07-06T12:00:00Z",            # ISO-8601 w/ Z
        "2026-07-06T12:00:00+00:00",       # ISO-8601 w/ offset
    ],
)
def test_parse_dt_accepts_common_formats(value):
    dt = ls._parse_dt(value)
    assert isinstance(dt, datetime)
    assert dt.tzinfo is not None


def test_parse_dt_naive_iso_gets_utc():
    dt = ls._parse_dt("2026-07-06T12:00:00")
    assert dt.tzinfo == timezone.utc


def test_parse_dt_none_and_garbage():
    assert ls._parse_dt(None) is None
    assert ls._parse_dt("") is None
    assert ls._parse_dt("not-a-date") is None


# --------------------------------------------------------------------------- #
# fetch_feed (RSS + Atom) via monkeypatched _get
# --------------------------------------------------------------------------- #
def test_fetch_feed_parses_rss(monkeypatch):
    monkeypatch.setattr(ls, "_get", lambda url: RSS_SAMPLE)
    items = ls.fetch_feed("https://example.com/feed")
    assert len(items) == 2
    first = items[0]
    assert first["title"] == "First & foremost"      # HTML entity decoded
    assert first["link"] == "https://example.com/a"
    assert first["published"].startswith("2026-07-06T12:00:00")
    assert first["source"] == "Example Feed"


def test_fetch_feed_parses_atom_link_href(monkeypatch):
    monkeypatch.setattr(ls, "_get", lambda url: ATOM_SAMPLE)
    items = ls.fetch_feed("https://atom.example/feed")
    assert len(items) == 1
    assert items[0]["link"] == "https://atom.example/x"
    assert items[0]["published"] == "2026-07-05T09:00:00Z"


def test_fetch_feed_limit(monkeypatch):
    monkeypatch.setattr(ls, "_get", lambda url: RSS_SAMPLE)
    assert len(ls.fetch_feed("u", limit=1)) == 1


def test_fetch_feed_bad_xml_returns_empty(monkeypatch):
    monkeypatch.setattr(ls, "_get", lambda url: b"<<<not xml>>>")
    assert ls.fetch_feed("u") == []


def test_web_search_stamps_query(monkeypatch):
    monkeypatch.setattr(ls, "_get", lambda url: RSS_SAMPLE)
    items = ls.web_search("drone components", when="7d")
    assert items and all(it["query"] == "drone components" for it in items)


# --------------------------------------------------------------------------- #
# ddg_search HTML scrape
# --------------------------------------------------------------------------- #
def test_ddg_search_extracts_real_target(monkeypatch):
    html = (
        '<a rel="nofollow" class="result__a" '
        'href="/l/?uddg=https%3A%2F%2Ftarget.example%2Fpage">Result &amp; Title</a>'
    )
    monkeypatch.setattr(ls, "_get", lambda url: html.encode("utf-8"))
    out = ls.ddg_search("query here")
    assert out == [{
        "title": "Result & Title",
        "link": "https://target.example/page",
        "published": "",
        "source": "duckduckgo",
        "query": "query here",
    }]


def test_ddg_search_network_error_returns_empty(monkeypatch):
    def boom(url):
        raise OSError("no network")
    monkeypatch.setattr(ls, "_get", boom)
    assert ls.ddg_search("q") == []


# --------------------------------------------------------------------------- #
# harvest: mixing, recency filter, de-dup, sort
# --------------------------------------------------------------------------- #
def test_harvest_dedups_and_sorts(monkeypatch):
    feed_a = [
        {"title": "old", "link": "https://x/1", "published": "2026-07-01T00:00:00Z",
         "source": "s", "query": ""},
        {"title": "new", "link": "https://x/2", "published": "2026-07-10T00:00:00Z",
         "source": "s", "query": ""},
    ]
    # second source repeats link /2 (dup) and adds /3
    feed_b = [
        {"title": "dup", "link": "https://x/2", "published": "2026-07-10T00:00:00Z",
         "source": "s", "query": ""},
        {"title": "mid", "link": "https://x/3", "published": "2026-07-05T00:00:00Z",
         "source": "s", "query": ""},
    ]
    calls = iter([feed_a, feed_b])
    monkeypatch.setattr(ls, "fetch_feed",
                        lambda *a, **k: next(calls))
    out = ls.harvest(["https://feed-a", "https://feed-b"],
                     since_days=0, min_year=2026)
    links = [it["link"] for it in out]
    assert links == ["https://x/2", "https://x/3", "https://x/1"]  # newest first, deduped
    assert len(links) == len(set(links))


def test_harvest_drops_items_before_min_year(monkeypatch):
    items = [
        {"title": "stale", "link": "https://y/1", "published": "2019-01-01T00:00:00Z",
         "source": "s", "query": ""},
        {"title": "fresh", "link": "https://y/2", "published": "2026-07-01T00:00:00Z",
         "source": "s", "query": ""},
    ]
    monkeypatch.setattr(ls, "fetch_feed", lambda *a, **k: list(items))
    out = ls.harvest(["https://feed"], since_days=0, min_year=2026)
    assert [it["link"] for it in out] == ["https://y/2"]


def test_harvest_runs_query_sources(monkeypatch):
    monkeypatch.setattr(ls, "web_search",
                        lambda q, when="7d", limit=30: [
                            {"title": q, "link": f"https://s/{q}", "published": "",
                             "source": "google-news", "query": q}])
    out = ls.harvest([{"query": "sanctions"}], since_days=0)
    assert out and out[0]["query"] == "sanctions"
