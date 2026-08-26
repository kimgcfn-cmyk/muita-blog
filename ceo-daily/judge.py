"""판정층 — Claude가 선별·태깅·CEO화법 변환을 한다."""
import json
import os
import re

from anthropic import Anthropic

MODEL = os.environ.get("MODEL", "claude-sonnet-5")
BANNED = ["무조건", "확실히 줄여", "큰일 납니다", "보장합니다"]


def _load_system() -> str:
    with open("prompts/system.md", encoding="utf-8") as f:
        return f.read()


def _extract_json(text: str) -> list:
    """백틱·잡담이 섞여 와도 배열만 뽑아낸다."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.MULTILINE).strip()
    start, end = text.find("["), text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"JSON 배열을 찾지 못함: {text[:200]}")
    return json.loads(text[start:end + 1])


def _sanitize(cards: list) -> list:
    """금지 표현이 섞이면 그 카드는 버린다."""
    clean = []
    for c in cards:
        blob = f"{c.get('what', '')} {c.get('ceo_line', '')}"
        if any(b in blob for b in BANNED):
            print(f"  [drop] 금지 표현 감지: {c.get('title')}")
            continue
        if not c.get("url"):
            continue
        clean.append(c)
    return clean[:3]


def judge(items: list) -> list:
    if not items:
        return []

    payload = "\n\n".join(
        f"[{i+1}] ({it['tier']}티어 / {it['source']})\n"
        f"제목: {it['title']}\n"
        f"요약: {it['summary'][:400]}\n"
        f"링크: {it['url']}"
        for i, it in enumerate(items)
    )

    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=4000,
            system=_load_system(),
            messages=[{
                "role": "user",
                "content": f"오늘 수집된 항목 {len(items)}건이다. 기준에 맞는 것만 최대 3건 골라 "
                           f"JSON 배열로만 출력하라.\n\n{payload}"
            }],
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  [error] API 호출 자체가 실패함: {type(exc).__name__}: {exc}")
        return []

    text = "".join(b.text for b in resp.content if b.type == "text")

    try:
        cards = _extract_json(text)
    except Exception as exc:  # noqa: BLE001
        # stop_reason이 "max_tokens"면 응답이 잘려서 파싱이 실패한 것 — 늘려야 할 신호.
        print(f"  [error] 파싱 실패 → 오늘은 건너뜀: {exc}")
        print(f"  [debug] stop_reason={resp.stop_reason}, 응답 길이={len(text)}자")
        return []

    return _sanitize(cards)
