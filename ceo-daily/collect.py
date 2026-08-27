"""수집층 — 소스에서 신규 항목만 긁어온다."""
import hashlib
import json
import os
import re
from datetime import datetime, timedelta, timezone

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup

KST = timezone(timedelta(hours=9))
SEEN_PATH = "state/seen.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; ceo-daily/1.0)"}


def url_hash(url: str) -> str:
    return hashlib.sha256(url.strip().encode()).hexdigest()[:16]


def load_seen() -> set:
    if not os.path.exists(SEEN_PATH):
        return set()
    with open(SEEN_PATH, encoding="utf-8") as f:
        return set(json.load(f))


def save_seen(seen: set, limit: int = 3000) -> None:
    os.makedirs("state", exist_ok=True)
    trimmed = list(seen)[-limit:]
    with open(SEEN_PATH, "w", encoding="utf-8") as f:
        json.dump(trimmed, f, ensure_ascii=False, indent=0)


def load_config(path: str = "sources.yaml") -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _recent(entry, days: int) -> bool:
    """발행일이 없으면 통과시킨다(중복 필터가 막아줌)."""
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed:
        return True
    published = datetime(*parsed[:6], tzinfo=timezone.utc)
    return published >= datetime.now(timezone.utc) - timedelta(days=days)


def fetch_rss(src: dict, days: int) -> list:
    # feedparser.parse(url) 은 자체 타임아웃이 없어 죽은 서버를 만나면
    # 무한정 대기할 수 있다. requests로 먼저 받아 타임아웃을 강제한다.
    # 국내 정부 사이트는 해외 러너(GitHub Actions)에서 접속 시 TLS 핸드셰이크에만
    # 8초 넘게 걸리는 경우가 있어(2026-08-27 실제 타임아웃 확인) 15초로 여유를 둔다.
    try:
        r = requests.get(src["url"], headers=UA, timeout=15)
        r.raise_for_status()
        feed = feedparser.parse(r.content)
    except Exception as exc:  # noqa: BLE001
        print(f"  [warn] {src['name']} RSS 수집 실패: {exc}")
        return []

    items = []
    for e in feed.entries:
        if not _recent(e, days):
            continue
        items.append({
            "source": src["name"],
            "tier": src["tier"],
            "title": (e.get("title") or "").strip(),
            "summary": BeautifulSoup(e.get("summary", ""), "html.parser").get_text(" ", strip=True)[:600],
            "url": e.get("link", "").strip(),
        })
    return items


def _resolve_link(el, src: dict) -> str:
    """목록이 실제 href 없이 JS onclick으로만 상세페이지를 여는 사이트용 대안 경로.

    sources.yaml에 link_template("...{id}...")이 있으면 아래 순서로 ID를 찾아 채운다.
      - id_attr : 요소 속성에 ID가 그대로 있는 경우 (예: 국세청 data-id="1354418")
      - id_regex: onclick 문자열에서 정규식 첫 캡처그룹으로 뽑는 경우 (예: 중기부 doBbsFView('86','1070729',...))
    link_template이 없는 소스는 기존처럼 href를 그대로 쓴다(법제처 등).
    """
    template = src.get("link_template")
    if not template:
        return el.get("href", "")
    item_id = ""
    if src.get("id_attr"):
        item_id = el.get(src["id_attr"], "")
    elif src.get("id_regex"):
        m = re.search(src["id_regex"], el.get("onclick", "") or "")
        item_id = m.group(1) if m else ""
    return template.format(id=item_id) if item_id else ""


def fetch_html(src: dict, days: int) -> list:
    try:
        r = requests.get(src["url"], headers=UA, timeout=15)
        r.raise_for_status()
    except Exception as exc:  # noqa: BLE001
        print(f"  [warn] {src['name']} HTML 수집 실패: {exc}")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    base = src.get("base", "")
    items = []
    for el in soup.select(src.get("selector", "a"))[:40]:
        href = _resolve_link(el, src)
        if not href or href.startswith("#"):
            continue
        # title 속성이 있으면 우선 사용(줄바꿈·공백 없는 깔끔한 제목), 없으면 텍스트에서 뽑는다.
        title = (el.get("title") or el.get_text(" ", strip=True))[:200]
        items.append({
            "source": src["name"],
            "tier": src["tier"],
            "title": title,
            "summary": "",
            "url": href if href.startswith("http") else base + href,
        })
    return items


def keyword_hit(item: dict, keywords: list) -> bool:
    blob = f"{item['title']} {item['summary']}"
    return any(k in blob for k in keywords)


def collect(days: int = 2) -> list:
    cfg = load_config()
    keywords = cfg["keywords"]
    seen = load_seen()

    raw = []
    for src in cfg["sources"]:
        try:
            got = fetch_rss(src, days) if src["type"] == "rss" else fetch_html(src, days)
            print(f"  {src['name']}: {len(got)}건")
            raw.extend(got)
        except Exception as exc:  # noqa: BLE001
            print(f"  [warn] {src['name']} 수집 실패: {exc}")

    out, batch_seen = [], set()
    for it in raw:
        if not it["url"] or not it["title"]:
            continue
        h = url_hash(it["url"])
        if h in seen or h in batch_seen:
            continue
        if not keyword_hit(it, keywords):
            continue
        batch_seen.add(h)
        it["hash"] = h
        out.append(it)

    # A티어 우선, 그다음 최신순 유지
    out.sort(key=lambda x: (x["tier"] != "A",))
    print(f"  → 키워드·중복 필터 통과: {len(out)}건")
    return out[:40]   # API에 넘기는 상한
