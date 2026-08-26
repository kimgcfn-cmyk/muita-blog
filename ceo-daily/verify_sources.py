"""최초 1회 실행 — 어떤 소스가 살아있는지 점검한다."""
import feedparser
import requests
import yaml

UA = {"User-Agent": "Mozilla/5.0 (compatible; ceo-daily/1.0)"}

with open("sources.yaml", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

print(f"{'상태':<6}{'건수':<6}{'소스'}")
print("-" * 60)

for src in cfg["sources"]:
    try:
        if src["type"] == "rss":
            feed = feedparser.parse(src["url"])
            n = len(feed.entries)
            ok = "OK" if n > 0 else "빈응답"
            sample = feed.entries[0].title[:40] if n else ""
        else:
            r = requests.get(src["url"], headers=UA, timeout=20)
            n = r.status_code
            ok = "OK" if r.ok else "실패"
            sample = f"HTTP {r.status_code}"
        print(f"{ok:<6}{str(n):<6}{src['name']}  | {sample}")
    except Exception as exc:  # noqa: BLE001
        print(f"{'에러':<6}{'-':<6}{src['name']}  | {exc}")

print("\n→ 'OK'가 아닌 항목은 sources.yaml에서 지우거나 URL을 고치세요.")
