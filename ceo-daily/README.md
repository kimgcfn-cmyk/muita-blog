# 법인대표 데일리 브리핑

매일 아침 7시(KST), 법인 대표에게 의미 있는 이슈 **최대 3건**을 Discord로 받는다.
같은 내용이 블로그용 마크다운으로 `archive/` 에 쌓인다.

```
sources.yaml ──> collect.py ──> judge.py ──> deliver.py ──> Discord
   (소스)          (수집)      (Claude 선별)   (배포)      + archive/*.md
```

---

## 세팅 5단계

### 1. Discord 웹훅 발급
채널 우클릭 → **채널 편집 → 연동 → 웹후크 → 새 웹후크** → URL 복사

### 2. 리포지토리 준비
```bash
git init && git add . && git commit -m "init"
gh repo create ceo-daily --private --source=. --push
```
> ⚠️ **반드시 Private.** 웹훅·아카이브가 들어갑니다.

### 3. Secrets 등록
GitHub 리포 → Settings → Secrets and variables → **Actions** → New secret

| 이름 | 값 |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com 에서 발급 |
| `DISCORD_WEBHOOK_URL` | 1단계에서 복사한 URL |

### 4. 소스 검증 (최초 1회, 로컬)
```bash
pip install -r requirements.txt
python verify_sources.py
```
`OK`가 아닌 항목은 `sources.yaml`에서 **삭제하거나 URL 수정**.
정부 사이트 RSS 경로는 자주 바뀌므로 이 단계는 건너뛰지 말 것.

### 5. 시험 발송
```bash
export ANTHROPIC_API_KEY=sk-...
python main.py --dry-run     # Discord 전송 없이 결과만 확인
python main.py               # 실제 전송
```
결과가 마음에 들면 GitHub Actions 탭 → **Run workflow** 로 클라우드에서도 1회 확인.

---

## 운영 팁

| 상황 | 조치 |
|---|---|
| 노이즈가 많다 | `sources.yaml` 의 B티어(언론) 소스를 줄인다 |
| 건수가 너무 적다 | `keywords` 를 넓히거나 `collect(days=2)` → `days=3` |
| 톤이 마음에 안 든다 | `prompts/system.md` 만 고친다 (코드 수정 불필요) |
| 발송 시간 변경 | `.github/workflows/daily.yml` 의 cron (UTC 기준, KST −9시간) |
| 비용 | 하루 1회 · 소량 입력 → 월 수백 원 수준. `MODEL` 환경변수로 모델 교체 가능 |

## 안전장치
- 확정 세액·절세액 생성 금지 (시스템 프롬프트)
- 세율·요건 언급 시 "(시행시점 확인 필요)" 강제
- 금지 표현 감지 시 해당 카드 자동 폐기 (`judge.py` BANNED)
- 모든 카드 하단 고정 문구: *실제 적용 전 세무사·법무 검토 필요*
- Discord 전송 성공 후에만 중복목록 갱신 → 실패한 날은 다음날 재시도
