# 떨사오팔 자동매매 봇

## 전략 설명
- **떨**어지면 **사**고
- **오**르면 **팔**고

## 설치 방법

```bash
pip install -r requirements.txt
```

## 설정 방법

1. `.env.example` 파일을 복사하여 `.env` 파일 생성
2. API 키 입력
3. 전략 설정 변경

```bash
cp .env.example .env
```

## 실행 방법

```bash
# 자동매매 봇 실행
python coin_trading.py

# 백테스트 실행
python backtest.py
```

## 전략 파라미터

| 변수 | 설명 | 기본값 |
|------|------|--------|
| BUY_THRESHOLD | 매수 임계값 (%) | -3.0% |
| SELL_THRESHOLD | 매도 임계값 (%) | 5.0% |
| INVEST_AMOUNT | 매수 금액 (원) | 10,000원 |
| INTERVAL_MINUTES | 체크 간격 (분) | 5분 |

## 주의사항

- API 키는 절대 공개하지 마세요
- 실제 투자 전에 백테스트를 실행하세요
- 손절선은 -10%로 설정되어 있습니다
- 시장 상황에 따라 전략을 조정하세요
