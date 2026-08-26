"""배포층 — Discord 전송 + 블로그용 마크다운 저장."""
import os
from datetime import datetime, timedelta, timezone

import requests

KST = timezone(timedelta(hours=9))
FOOTER = "※ 일반적 원칙이며, 실제 적용 전 세무사·법무 검토 필요"
COLOR = {"🔴": 0xD64545, "🟡": 0xE0A73C, "🟢": 0x4C9A5F}


def to_discord(cards: list, webhook: str) -> None:
    today = datetime.now(KST).strftime("%Y.%m.%d (%a)")

    if not cards:
        requests.post(webhook, json={
            "content": f"**법인대표 데일리 · {today}**\n오늘은 전달할 만한 이슈가 없습니다."
        }, timeout=20).raise_for_status()
        return

    embeds = []
    for c in cards:
        embeds.append({
            "title": f"{c['level']} [{c['area']}] {c['title']}"[:250],
            "url": c["url"],
            "color": COLOR.get(c["level"], 0x777777),
            "fields": [
                {"name": "무슨 일", "value": c["what"][:900]},
                {"name": "대표님께 쓸 한마디", "value": c["ceo_line"][:900]},
                {"name": "오늘의 액션", "value": c["action"][:900]},
                {"name": "원문", "value": f"[기사 보기]({c['url']})"[:900]},
            ],
            "footer": {"text": f"{c.get('source', '')} · {FOOTER}"[:2000]},
        })

    requests.post(webhook, json={
        "content": f"**법인대표 데일리 · {today}**  ({len(cards)}건)",
        "embeds": embeds,
    }, timeout=20).raise_for_status()


def to_markdown(cards: list) -> str:
    """블로그에 그대로 붙여넣는 용도."""
    d = datetime.now(KST)
    lines = [f"# 법인대표 데일리 — {d.strftime('%Y년 %m월 %d일')}", ""]

    if not cards:
        lines.append("오늘은 전달할 만한 이슈가 없습니다.")
    for c in cards:
        lines += [
            f"## {c['level']} {c['title']}",
            f"**영역**: {c['area']}　|　**출처**: {c.get('source', '')}",
            "",
            f"{c['what']}",
            "",
            f"> {c['ceo_line']}",
            "",
            f"- 컨설턴트 액션: {c['action']}",
            f"- 원문: {c['url']}",
            "",
            "---",
            "",
        ]
    lines.append(f"*{FOOTER}*")
    return "\n".join(lines)


def save_archive(cards: list) -> str:
    os.makedirs("archive", exist_ok=True)
    path = f"archive/{datetime.now(KST).strftime('%Y-%m-%d')}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(to_markdown(cards))
    return path
