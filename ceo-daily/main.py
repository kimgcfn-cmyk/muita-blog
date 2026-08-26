"""매일 1회 실행되는 오케스트레이터."""
import os
import sys

import collect
import deliver
import judge


def main() -> int:
    dry = "--dry-run" in sys.argv

    print("[1/3] 수집")
    items = collect.collect(days=2)
    if not items:
        print("  신규 항목 없음 → 종료")
        return 0

    print("[2/3] 판정")
    cards = judge.judge(items)
    print(f"  채택 {len(cards)}건")

    print("[3/3] 배포")
    path = deliver.save_archive(cards)
    print(f"  아카이브 저장: {path}")

    if dry:
        print("\n--- DRY RUN 미리보기 ---\n")
        print(deliver.to_markdown(cards))
        return 0

    webhook = os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        print("  [error] DISCORD_WEBHOOK_URL 미설정")
        return 1
    deliver.to_discord(cards, webhook)
    print("  Discord 전송 완료")

    # 전송 성공한 뒤에만 seen 갱신 (실패 시 다음날 재시도되게)
    seen = collect.load_seen()
    seen.update(it["hash"] for it in items)
    collect.save_seen(seen)
    print(f"  중복목록 갱신: {len(seen)}건")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
